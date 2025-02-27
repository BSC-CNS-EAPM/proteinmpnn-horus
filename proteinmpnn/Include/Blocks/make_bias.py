import os

from HorusAPI import PluginBlock, PluginVariable, VariableTypes

# Define the variables for the make_bias block
AA_list = PluginVariable(
    id="AA_list",
    name="AA list",
    description="List of aminoacids to bias.",
    type=VariableTypes.STRING,
    placeholder="D E H K N Q R S T W Y",
)

bias_list = PluginVariable(
    id="bias_list",
    name="Bias list",
    description="Residue positions to be tied. Lists must match in length. Has to be the same length as the input parsed chains. Has to be the same length as the AA list.",
    type=VariableTypes.STRING,
    placeholder="1.39 1.39 1.39 1.39 1.39 1.39 1.39 1.39 1.39 1.39 1.39",
)


# Output
output_path_for_bias_pdbs = PluginVariable(
    id="output_path_for_bias_pdbs",
    name="Bias JSONL",
    description="The JSONL file containing the biased positions.",
    type=VariableTypes.CUSTOM,
    allowedValues=["bias_aa_jsonl"],
)


# Function to run the assign_fixed_chains.py script
def run_make_bias(block: PluginBlock):
    """
    Executes the make_tied_positions.py script with the provided arguments.
    """

    output_path = "bias_pdbs.jsonl"

    if os.path.exists(output_path):
        os.remove(output_path)

    script_plugin_path = os.path.join(
        block.pluginDir,
        "Include",
        "ProteinMPNN",
        "helper_scripts",
        "make_bias_AA.py",
    )

    aa_list_value = block.variables[AA_list.id]
    bias_list_value = block.variables[bias_list.id]

    # Build the command to run
    cmd = [
        "python",
        script_plugin_path,
        f"--output_path={output_path}",
        f"--AA_list='{aa_list_value}'",
        f"--bias_list='{bias_list_value}'",
    ]
    # Run the command
    from utils import execute_in_environment

    out = execute_in_environment(block, " ".join(cmd))

    print(out)

    block.setOutput(output_path_for_bias_pdbs.id, output_path)


# Instantiate the block
make_bias = PluginBlock(
    id="make_bias",
    name="Make Bias AA",
    description="This block executes the make_bias_AA.py script to make biased positions for a protein structure.",
    variables=[AA_list, bias_list],
    outputs=[output_path_for_bias_pdbs],
    action=run_make_bias,
)
