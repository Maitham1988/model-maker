"""
Offline Voice Engine — Whisper STT + Piper TTS
100% local, no internet required.
"""

from __future__ import annotations

import io
import struct
import time
from pathlib import Path

import numpy as np


class VoiceEngine:
    """Handles speech-to-text and text-to-speech using local models."""

    def __init__(
        self,
        whisper_model: str = "base",
        piper_voice_path: str | None = None,
    ):
        self.whisper_model_name = whisper_model
        self.piper_voice_path = piper_voice_path
        self._whisper = None
        self._piper = None
        self._piper_sample_rate = 22050
        self._ready = False

    def load(self) -> None:
        """Load both STT and TTS models."""
        start = time.time()

        # Load Whisper STT
        print(f"🎤 Loading Whisper ({self.whisper_model_name})...")
        from faster_whisper import WhisperModel

        self._whisper = WhisperModel(
            self.whisper_model_name,
            device="cpu",
            compute_type="int8",
        )
        print(f"   ✅ Whisper loaded ({time.time() - start:.1f}s)")

        # Load Piper TTS
        if self.piper_voice_path and Path(self.piper_voice_path).exists():
            t = time.time()
            print(f"🔊 Loading Piper TTS voice...")
            from piper import PiperVoice

            self._piper = PiperVoice.load(self.piper_voice_path)
            # Get sample rate from config
            config_path = Path(self.piper_voice_path + ".json")
            if config_path.exists():
                import json

                with open(config_path) as f:
                    voice_config = json.load(f)
                    self._piper_sample_rate = voice_config.get("audio", {}).get(
                        "sample_rate", 22050
                    )
            print(f"   ✅ Piper TTS loaded ({time.time() - t:.1f}s)")
        else:
            print(f"⚠️  Piper voice not found at: {self.piper_voice_path}")
            print("   TTS will not be available.")

        self._ready = True
        print(f"🎙️  Voice engine ready ({time.time() - start:.1f}s total)")

    @property
    def is_ready(self) -> bool:
        return self._ready

    @property
    def has_stt(self) -> bool:
        return self._whisper is not None

    @property
    def has_tts(self) -> bool:
        return self._piper is not None

    def transcribe(self, audio_bytes: bytes, sample_rate: int = 16000) -> str:
        """Convert speech audio to text.

        Args:
            audio_bytes: Raw PCM audio bytes (16-bit signed, mono)
                         or WAV file bytes.
            sample_rate: Sample rate of the audio (default 16000).

        Returns:
            Transcribed text string.
        """
        if not self._whisper:
            raise RuntimeError("Whisper STT not loaded")

        # Convert bytes to numpy array
        audio_array = self._bytes_to_numpy(audio_bytes, sample_rate)

        # Transcribe
        segments, info = self._whisper.transcribe(
            audio_array,
            language="en",
            beam_size=5,
            vad_filter=True,
            vad_parameters=dict(
                min_speech_duration_ms=250,
                min_silence_duration_ms=500,
            ),
        )

        # Collect text from all segments
        text = " ".join(segment.text.strip() for segment in segments)
        return text.strip()

    def synthesize(self, text: str) -> tuple[bytes, int]:
        """Convert text to speech audio.

        Args:
            text: Text to synthesize.

        Returns:
            Tuple of (WAV file bytes, sample rate).
        """
        if not self._piper:
            raise RuntimeError("Piper TTS not loaded")

        import wave

        # Use synthesize_wav which writes to a wave.Wave_write object
        wav_buffer = io.BytesIO()
        wav_file = wave.open(wav_buffer, "wb")
        self._piper.synthesize_wav(text=text, wav_file=wav_file)
        wav_file.close()

        wav_bytes = wav_buffer.getvalue()
        return wav_bytes, self._piper_sample_rate

    def _bytes_to_numpy(
        self, audio_bytes: bytes, sample_rate: int
    ) -> np.ndarray:
        """Convert audio bytes to numpy float32 array.

        Handles both raw PCM and WAV formats.
        """
        # Check if it's a WAV file (starts with RIFF)
        if audio_bytes[:4] == b"RIFF":
            return self._wav_to_numpy(audio_bytes)

        # Check if it's a WebM/Opus blob (from browser MediaRecorder)
        if audio_bytes[:4] == b"\x1a\x45\xdf\xa3" or b"webm" in audio_bytes[:32]:
            return self._webm_to_numpy(audio_bytes)

        # Raw PCM 16-bit signed little-endian
        audio_array = np.frombuffer(audio_bytes, dtype=np.int16).astype(np.float32)
        audio_array /= 32768.0  # Normalize to [-1, 1]

        # Resample to 16kHz if needed (Whisper expects 16kHz)
        if sample_rate != 16000:
            audio_array = self._resample(audio_array, sample_rate, 16000)

        return audio_array

    def _wav_to_numpy(self, wav_bytes: bytes) -> np.ndarray:
        """Parse WAV file bytes to numpy float32 array at 16kHz."""
        import wave

        wav_buffer = io.BytesIO(wav_bytes)
        with wave.open(wav_buffer, "rb") as wav:
            sample_rate = wav.getframerate()
            n_channels = wav.getnchannels()
            sample_width = wav.getsampwidth()
            n_frames = wav.getnframes()
            raw_data = wav.readframes(n_frames)

        # Convert to numpy
        if sample_width == 2:
            audio = np.frombuffer(raw_data, dtype=np.int16).astype(np.float32)
            audio /= 32768.0
        elif sample_width == 4:
            audio = np.frombuffer(raw_data, dtype=np.int32).astype(np.float32)
            audio /= 2147483648.0
        else:
            audio = np.frombuffer(raw_data, dtype=np.uint8).astype(np.float32)
            audio = (audio - 128.0) / 128.0

        # Convert stereo to mono
        if n_channels > 1:
            audio = audio.reshape(-1, n_channels).mean(axis=1)

        # Resample to 16kHz if needed
        if sample_rate != 16000:
            audio = self._resample(audio, sample_rate, 16000)

        return audio

    def _webm_to_numpy(self, webm_bytes: bytes) -> np.ndarray:
        """Convert WebM/Opus audio to numpy float32 array at 16kHz using av."""
        import av

        container = av.open(io.BytesIO(webm_bytes))
        audio_frames = []

        for frame in container.decode(audio=0):
            # Convert to numpy float32
            arr = frame.to_ndarray()
            if arr.ndim > 1:
                arr = arr.mean(axis=0)  # stereo to mono
            audio_frames.append(arr)

        container.close()

        if not audio_frames:
            return np.array([], dtype=np.float32)

        audio = np.concatenate(audio_frames).astype(np.float32)

        # Get sample rate from the stream
        stream = list(container.streams.audio)[0] if hasattr(container, 'streams') else None
        src_rate = 48000  # WebM default

        # Normalize if integer format
        if audio.max() > 1.0 or audio.min() < -1.0:
            max_val = max(abs(audio.max()), abs(audio.min()))
            if max_val > 0:
                audio /= max_val

        # Resample to 16kHz
        if src_rate != 16000:
            audio = self._resample(audio, src_rate, 16000)

        return audio

    def _resample(
        self, audio: np.ndarray, src_rate: int, dst_rate: int
    ) -> np.ndarray:
        """Simple linear resampling."""
        if src_rate == dst_rate:
            return audio
        ratio = dst_rate / src_rate
        n_samples = int(len(audio) * ratio)
        indices = np.linspace(0, len(audio) - 1, n_samples)
        return np.interp(indices, np.arange(len(audio)), audio).astype(np.float32)
