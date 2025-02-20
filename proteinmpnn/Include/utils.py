from HorusAPI import PluginBlock

from Config.config import conda_environment, conda_run_config


def execute_in_environment(block: PluginBlock, cmd: str):
    """
    Gets the conda environment and executes the command in that environment.
    """

    env: str = block.config[conda_environment.id]
    conda_run: str = block.config[conda_run_config.id]

    return block.remote.command(f"{conda_run} {env} {cmd}")
