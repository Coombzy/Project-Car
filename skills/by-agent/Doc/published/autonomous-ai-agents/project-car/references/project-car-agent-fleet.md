# Project Car Agent Fleet

## Overview
The Project Car Agent Fleet consists of three dedicated hardware pieces, each running its own Hermes agent. Together they form a coordinated, self-improving AI system that works in partnership with Grok.

### Porsche (M4 Pro MacBook Pro - 24GB RAM)
**Role**: Primary coordinator and light AI workhorse.
- Handles cron jobs, audits, filing, task delegation, and most interactions with Grok.
- Acts as the 'brain' and orchestrator of the fleet.

**Recommended local models (July 2026)**:
1. Llama 3.2 3B / 8B (highly efficient)
2. Gemma 2 9B
3. Phi-4 14B (optimized for speed)
4. Qwen2.5 14B
5. Mistral Small 3

### Lightning McKing (Home Lab Server)
**Role**: Heavy compute workhorse.
- Runs larger inference tasks, training/fine-tuning, data processing, and high-load jobs.

**Recommended local models (July 2026)**:
1. Llama 3.1 70B (quantized)
2. Mixtral 8x22B
3. Command-R Plus
4. DeepSeek R1 671B (if VRAM allows)
5. Newer 2026 models such as Llama 4 variants or equivalent

### Doc Hakosuka (M1 Max MacBook Pro - 64GB RAM)
**Role**: Heavyweight for large local models.
- Dedicated to running the largest feasible local LLMs with high context and reasoning capability.

**Recommended local models (July 2026)**:
1. Llama 3.1 70B full or high quant
2. Qwen2.5 72B
3. Mistral Large variants
4. Claude-equivalent local models if available
5. Emerging 100B+ class models optimized for Apple Silicon

## Collaboration Model
Porsche (coordinator) breaks down tasks, delegates to Lightning McKing and Doc Hakosuka, and relays results back to Grok. The fleet works as a unified system.

## Next Steps
- Daily backups to GitHub + future Nextcloud
- Communication via shared files

Last updated: July 9, 2026