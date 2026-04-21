# Using Secure Gemini CLI Authentication with EvoClaw

By default, EvoClaw requires an API key (`UNIFIED_API_KEY`) to authenticate the Gemini agent running inside the evaluation Docker containers. However, you can securely share an isolated Gemini CLI authentication session with the container without needing a static API key.

To prevent the Docker container (which runs the agent with the sandbox-bypassing `--yolo` flag) from accessing your primary, host-level `~/.gemini` credentials, EvoClaw is configured to use an **isolated authentication directory**.

## How It Works

The `gemini-cli` agent adapter in EvoClaw uses the `GEMINI_CLI_HOME` environment variable. If this variable is set on your host machine, EvoClaw will mount the `.gemini` folder from that specific path into the Docker container at `/home/fakeroot/.gemini`. If `GEMINI_CLI_HOME` is not set, no credentials are mounted.

## Setup Instructions

Follow these steps to create an isolated authentication session for EvoClaw:

### 1. Create an Isolated Directory

Create a dedicated folder for EvoClaw's Gemini session.

```bash
mkdir -p /tmp/evoclaw-gemini-auth
```

### 2. Authenticate the CLI in the Isolated Directory

Export the `GEMINI_CLI_HOME` environment variable to point to your new directory, and then log in. The CLI will save its credentials inside `/tmp/evoclaw-gemini-auth/.gemini`.

```bash
export GEMINI_CLI_HOME="/tmp/evoclaw-gemini-auth"
gemini login
```

### 3. Run the Evaluation

Keep the `GEMINI_CLI_HOME` environment variable exported in your terminal session. Now, when you run the EvoClaw evaluation script, it will automatically detect the variable and mount only your isolated credentials into the container.

```bash
# Example: Running the Navidrome milestone 1 evaluation
python harness/e2e/run_e2e.py \
    --repo navidrome_navidrome_v0.57.0_v0.58.0 \
    --milestone milestone_001 \
    --agent gemini-cli \
    --model gemini-2.0-flash
```

## Security Considerations

- **Container Isolation:** By using `GEMINI_CLI_HOME`, your primary `~/.gemini` directory is completely isolated from the Docker container.
- **Session Revocation:** Once you are done running evaluations, you can simply delete the `/tmp/evoclaw-gemini-auth` directory to instantly revoke the container's access, without affecting your primary host machine's Gemini CLI login.
