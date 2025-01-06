"""Module providing main entrypoint."""
import os
import click
import uvicorn
from core.config import get_config
from pathlib import Path

# Setup cli parameter for main command (main.py --debug --env local --log-path /path/to/log)
@click.command()
@click.option(
    "--env",
    type=click.Choice(["local", "prod"], case_sensitive=False),
    default="prod",
)
@click.option(
    "--debug",
    type=click.BOOL,
    is_flag=True,
    default=False,
)
@click.option(
    "--log-path",
    type=click.Path(exists=False, file_okay=True, dir_okay=False, readable=True),
    default="/var/log/apache2/access.log",
)
def main(env: str, debug: bool, log_path: str):
    """
    Start main function.

    Args:
        env (str): The environment name.
        debug (bool): Debug mode flag.
        log_path (str): Path to the log file.
    """
    # Inject click option in environment variable for config
    os.environ["AGENT_ENV"] = env
    os.environ["AGENT_DEBUG"] = str(debug)
    os.environ["LOG_PATH"] = log_path

    # Check if the log file exists
    log_file = Path(log_path)
    if not log_file.exists():
        print(f"Please provide a log path. The default one does not exist: {log_path}")
        new_log_path = input("Give another log path or press Enter to proceed without: ").strip()
        if new_log_path:
            log_file = Path(new_log_path)
            os.environ["LOG_PATH"] = new_log_path
            if not log_file.exists():
                print(f"The provided log path does not exist: {new_log_path}")
                print("Proceeding without a log file.")
        else:
            print("Proceeding without a log file.")

    config = get_config()
    # Start Webserver
    uvicorn.run(
        app="server:app",
        host=config.app_host,
        port=config.app_port,
        reload=config.env == "local",
        workers=1,
    )

# Main entrypoint, click will mutate main() with cli options
if __name__ == "__main__":
    main()
