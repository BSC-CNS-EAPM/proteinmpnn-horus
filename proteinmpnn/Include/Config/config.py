from HorusAPI import PluginConfig, VariableTypes, PluginVariable

conda_environment = PluginVariable(
    id="plugin_conda_env",
    name="Conda Environment",
    description="The conda environment name to use for the plugin. "
    "Use this command to install the correct dependencies in the environment: "
    "conda install pytorch torchvision torchaudio cudatoolkit=11.3 -c pytorch",
    type=VariableTypes.STRING,
    defaultValue="proteinmpnn",
)

conda_run_config = PluginVariable(
    id="config_plugin_conda_run",
    name="Conda run command",
    description="The prefix to run the command inside the environment.",
    type=VariableTypes.STRING,
    defaultValue="conda run -p",
)

conda_environment_config = PluginConfig(
    id="config_plugin_conda_env",
    name="Conda Environment",
    description="Configuration for the plugin's conda environment.",
    variables=[conda_environment, conda_run_config],
)
