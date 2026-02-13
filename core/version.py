import subprocess

def get_version():
    try:
        return subprocess.check_output(
            ["git", "describe", "--tags", "--always"]
        ).decode().strip()
    except:
        return "dev"

BOT_VERSION = get_version()
