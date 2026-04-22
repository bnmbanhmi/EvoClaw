import re

with open('harness/e2e/agents/gemini_coretext.py', 'r') as f:
    content = f.read()

# Define run_cmd at the top
content = content.replace("    def run_cmd", "    def run_cmd(cmd, shell=False):\n        '''Run command and return (success, stdout, stderr)'''\n        try:\n            result = subprocess.run(\n                cmd,\n                shell=shell,\n                capture_output=True,\n                text=True,\n                timeout=300\n            )\n            return result.returncode == 0, result.stdout.strip(), result.stderr.strip()\n        except Exception as e:\n            return False, '', str(e)\n\n    # Check current Node.js version\n    def OLD_RUN_CMD")

# Fix the OLD_RUN_CMD so we remove the duplicate definition
content = re.sub(r"    def OLD_RUN_CMD.*?# Check current Node.js version", "    # Check current Node.js version", content, flags=re.DOTALL)

with open('harness/e2e/agents/gemini_coretext.py', 'w') as f:
    f.write(content)
