# Gemini CLI Agent Scratchpad

## Documentation References
- **Project Overview & Architecture**: `README.md`
- **Dataset Structure & Statistics**: `EvoClaw-data/README.md`
- **Operational Guides**:
    - Launching & Monitoring: `docs/running-trials.md`
    - Troubleshooting & Recovery: `docs/running-trials.md#when-a-repo-looks-stuck`
    - Advanced Usage (Single-repo, CLI refs): `docs/advanced.md`
    - Gemini CLI Auth Setup: `docs/gemini-cli-auth.md`

## Current Status
- **Active Trial**: `ripgrep_gemini_3_flash_test_002` (Pending Restart)
- **Target Repository**: `ripgrep` (BurntSushi_ripgrep_14.1.1_15.0.0)
- **Agent**: `gemini-cli`
- **Model**: `gemini-3-flash-preview`
- **Authentication**: Isolated CLI login via `GEMINI_CLI_HOME="/tmp/evoclaw-gemini-auth"`.
- **Progress (2026-04-22)**: 0/11 graded milestones evaluated (All past trial data cleaned).

## Changes & Fixes
### 1. Gemini Initialization Optimization
- **File**: `harness/e2e/agents/gemini.py`
- **Problem**: Recursive filesystem search from `/` caused 99% CPU hang.
- **Fix**: Restricted search to `node_modules` paths.

### 2. Evaluation CPU Limit Adjustment
- **File**: `harness/e2e/evaluator.py`
- **Problem**: Score was 0.0% because the evaluator requested 16 CPUs for test containers, which exceeded the host's 10-CPU allocation (Docker error 125).
- **Fix**: Lowered default and fallback CPU limits to 8 in evaluator.py and metadata.json.

### 3. Coretext Engine Integration
- **Files**: `harness/e2e/prompt/coretext.md`, `harness/e2e/agents/gemini_coretext.py`, `harness/e2e/run_e2e.py`
- **Problem**: Need for dynamic context injection and architectural rule persistence across milestones.
- **Fix**:
    - Created `gemini-coretext` harness with automated Python dependency installation (supports `pyproject.toml` / `requirements.txt`).
    - Added `coretext` prompt template with mandatory file-linking steps in the agent workflow.
    - Updated `run_e2e.py` and `config.py` to support the new agent/prompt strategy.

## Operations Log
- **2026-04-21 21:07**: Resumed trial `_002`. Detected previous evaluation errors and triggered re-evaluation of submissions using the new CPU limit.
- **2026-04-22 09:42**: Detected potential wedge on `ripgrep` (>10h running sessions).
- **2026-04-22 09:48**: Performed global cleanup of all past trial runs (`_001` and `_002`). Removed all `e2e_trial` directories, locks, and logs across all repositories.
- **2026-04-22 10:55**: Integrated **Coretext Engine**. Created dedicated `gemini-coretext` harness and `coretext` prompt version for opt-in context injection benchmarks.

## Useful Commands
- **Monitor**: `uv run scripts/monitor.sh ripgrep_gemini_3_flash_test_002` (--detail or --full)
- **Pause/Stop**: `pgrep -f "run_e2e.*ripgrep_gemini_3_flash_test_002" | xargs kill`
- **Resume**: `export GEMINI_CLI_HOME="/tmp/evoclaw-gemini-auth" && uv run python scripts/run_all.py --config trial_config.yaml --repos ripgrep`
- **Run with Coretext**: `uv run python scripts/run_all.py --config trial_config.yaml --agent gemini-coretext --prompt-version coretext`
- **Diagnose Wedge (Session Heartbeat)**: `docker exec BurntSushi_ripgrep_14.1.1_15.0.0-ripgrep_gemini_3_flash_test_002 ls -la /home/fakeroot/.gemini`
- **Kill Wedged Agent**: `docker exec BurntSushi_ripgrep_14.1.1_15.0.0-ripgrep_gemini_3_flash_test_002 pkill -KILL -f 'gemini --model'`
