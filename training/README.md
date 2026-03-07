# Model Maker — Fine-Tuning & Shipping Guide

## Overview

This guide covers the complete pipeline from training dataset → fine-tuned model → customer delivery.

### Architecture

```
training/
├── medical_qa_dataset.jsonl    ← 69 Q&A pairs (Arabic + English + multilingual)
├── splits/
│   ├── train.jsonl             ← 55 examples (80%)
│   ├── valid.jsonl             ← 7 examples (10%)
│   └── test.jsonl              ← 7 examples (10%)
└── validate_dataset.py         ← Dataset validation script

tools/
├── finetune.py                 ← Fine-tuning pipeline (download → train → fuse → GGUF)
├── build_version.py            ← Versioning & shipping tool
├── test_medical_accuracy.py    ← Automated quality testing (36 questions, 6 languages)
└── ...

models/
├── mlx/
│   ├── Qwen2.5-7B-Instruct/       ← Base model (MLX format, ~14GB)
│   └── Qwen2.5-7B-Medical-v1/     ← Fused fine-tuned model
├── adapters/
│   └── medical-v1/                 ← LoRA adapters
└── Qwen2.5-7B-Medical-v1-Q4_K_M.gguf  ← Final deployable model (~4.5GB)
```

---

## Step-by-Step Pipeline

### 1. Prepare Training Data

The training dataset is at `training/medical_qa_dataset.jsonl`. Each line is a JSON object:

```json
{
  "messages": [
    {"role": "system", "content": "You are an emergency medical..."},
    {"role": "user", "content": "My hand got burned. What should I do?"},
    {"role": "assistant", "content": "Act immediately:\n\n1. Cool the burn..."}
  ]
}
```

**To add more training data:** Edit `medical_qa_dataset.jsonl` and add new JSONL lines.

**To validate:**
```bash
python3 training/validate_dataset.py
```

**To split:**
```bash
python3 tools/finetune.py prepare
```

### 2. Download Base Model

Downloads Qwen2.5-7B-Instruct in MLX format (~14GB, requires internet):

```bash
python3 tools/finetune.py download
```

### 3. Fine-Tune with QLoRA

Runs on Apple Silicon using MLX (native Metal GPU acceleration):

```bash
# Default settings (1000 iterations, rank 16)
python3 tools/finetune.py train

# Custom settings
python3 tools/finetune.py train --iters 2000 --lr 2e-5 --lora-rank 32
```

**Hyperparameters:**

| Parameter | Default | Notes |
|-----------|---------|-------|
| LoRA Rank | 16 | Higher = more capacity, more memory |
| LoRA Layers | 16 | Number of transformer layers to adapt |
| Learning Rate | 1e-5 | Lower for stability |
| Batch Size | 1 | Increase if RAM > 32GB |
| Iterations | 1000 | Monitor loss plateaus |
| Max Seq Length | 2048 | Covers most medical responses |

**Expected training time:** ~30-60 minutes on M1/M2 Pro (16GB RAM)

**Memory requirements:**
- 16GB RAM: Works with batch_size=1, grad_checkpoint=True
- 32GB RAM: Can use batch_size=2-4
- 64GB RAM: Can use batch_size=8+

### 4. Test Fine-Tuned Model

```bash
python3 tools/finetune.py test
```

Runs 5 test prompts (English + Arabic) and shows the model's responses.

### 5. Fuse Adapters

Merges LoRA weights into the base model:

```bash
python3 tools/finetune.py fuse
```

### 6. Convert to GGUF

Converts the fused model to GGUF Q4_K_M format for deployment:

```bash
python3 tools/finetune.py convert
```

This produces `models/Qwen2.5-7B-Medical-v1-Q4_K_M.gguf` (~4.5GB).

### 7. Full Pipeline (All Steps)

```bash
python3 tools/finetune.py all
```

---

## Building & Shipping Versions

### Build a Version

```bash
python3 tools/build_version.py build \
    --version medical-v1 \
    --model models/Qwen2.5-7B-Medical-v1-Q4_K_M.gguf
```

This creates `builds/medical-v1/` containing:
- `app/` — Complete application (backend + frontend)
- `model/` — Model manifest (actual GGUF goes here)
- `install.py` — Customer installation script
- `README.md` — Setup instructions

### Prepare for Customer

```bash
python3 tools/build_version.py customer \
    --version medical-v1 \
    --customer customer-001 \
    --hardware-id "abc123..."
```

### List Versions

```bash
python3 tools/build_version.py list
```

### Shipping Checklist

1. Build version: `python3 tools/build_version.py build --version medical-v1 --model <path>`
2. Copy `builds/medical-v1/` to USB drive
3. Copy the GGUF model file to `builds/medical-v1/model/`
4. On customer device:
   - Run `python3 install.py`
   - Copy model file to `model/` folder
   - Run `cd app && python3 run.py`

---

## Creating New Product Versions

### Example: Medical v2 (More Training Data)

1. Add more Q&A pairs to `training/medical_qa_dataset.jsonl`
2. Run `python3 tools/finetune.py prepare`
3. Run `python3 tools/finetune.py train --iters 2000`
4. Test: `python3 tools/finetune.py test`
5. Fuse: `python3 tools/finetune.py fuse`
6. Convert: `python3 tools/finetune.py convert`
7. Build: `python3 tools/build_version.py build --version medical-v2 --model models/Qwen2.5-7B-Medical-v2-Q4_K_M.gguf`

### Example: Survival Field (Different Product)

1. Create `training/survival_qa_dataset.jsonl` (focus on shelter, navigation, fire)
2. Modify paths in `tools/finetune.py` or create a variant
3. Fine-tune a survival-focused model
4. Build: `--version survival-v1 --field survival`

### Example: 14B Premium Tier

1. Change `BASE_MODEL_HF = "Qwen/Qwen2.5-14B-Instruct"` in finetune.py
2. Requires 32GB+ RAM for fine-tuning
3. Produces ~8.5GB GGUF for customers with 16GB+ RAM

---

## Training Data Guidelines

### Good Training Examples

- Direct, actionable medical/survival instructions
- No disclaimers ("consult a doctor", "this is not medical advice")
- Step-by-step numbered instructions
- Explicit DO NOT / NEVER warnings for myths
- Arabic (Gulf dialect) + English pairs
- Edge cases: myth correction, dangerous remedies to reject

### Format

```json
{"messages":[
  {"role":"system","content":"You are an emergency medical and survival assistant..."},
  {"role":"user","content":"<question>"},
  {"role":"assistant","content":"<ideal response>"}
]}
```

### Quality Checklist

- [ ] Medically accurate (verified against reliable sources)
- [ ] No disclaimers or hedging
- [ ] Clear numbered steps
- [ ] Dangerous myths explicitly warned against
- [ ] Works without internet/hospital context
- [ ] Arabic responses use Gulf dialect
- [ ] Response length: 200-600 words (enough detail without rambling)

---

## Quality Testing

After fine-tuning, run the automated test suite:

```bash
# Start the server with the new model
cd base && python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000

# In another terminal:
python3 tools/test_medical_accuracy.py
```

This runs 36 medical questions across 6 languages and auto-grades responses.

Target: **Grade A (95%+)** after fine-tuning.
