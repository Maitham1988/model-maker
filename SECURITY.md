# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability in Model Maker, please report it responsibly.

**DO NOT** open a public GitHub issue for security vulnerabilities.

### How to Report

Email: **maitham@flexsell.com**

Include:
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

We will acknowledge your report within 48 hours and provide a timeline for a fix.

## Security Design Principles

Model Maker is designed with security as a core principle:

### Data Privacy
- **Zero telemetry** — The app collects no usage data
- **Zero network calls** — The app makes no outbound connections
- **Local storage only** — All data stays in SQLite on the user's device
- **No cloud sync** — Conversations never leave the device

### Model Security
- Models are downloaded from verified sources (Hugging Face) with checksum verification
- No remote code execution in models (GGUF format is data-only)
- Model files are never modified after download

### Website Security
- Static site served via CloudFront with HTTPS
- Content Security Policy headers
- No server-side code on the website
- Download links point to GitHub Releases (verified checksums)

### License System
- Device-locked HMAC-SHA256 licensing (for commercial builds)
- License verification is local-only — no license server

## Supported Versions

| Version | Supported          |
|---------|--------------------|
| Latest  | ✅ Yes             |
| < 1.0   | ⚠️ Best effort     |

## Responsible Disclosure

We follow a 90-day responsible disclosure timeline. We will:
1. Acknowledge your report within 48 hours
2. Investigate and confirm the vulnerability
3. Develop and test a fix
4. Release the fix and credit you (unless you prefer anonymity)
