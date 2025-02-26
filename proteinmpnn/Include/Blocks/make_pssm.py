import os

from HorusAPI import PluginBlock, PluginVariable, VariableTypes

# Define the variables for the make_bias block
input_parsed_chains = PluginVariable(
    id="output_parsed_chains",
    name="Parsed Chains JSONL",
    description="The JSONL file containing the parsed chains.",
    type=VariableTypes.CUSTOM,
    allowedValues=["parsed_pdbs_jsonl"],
)


pssm_input_path = PluginVariable(
    id="pssm_input_path",
    name="PSSMs",
    description="Path to the folder containiong PSSMs saved as npz files.",
    type=VariableTypes.FOLDER,
)


# Output
output_path_for_pssm_dict = PluginVariable(
    id="output_path_for_pssm_dict",
    name="PSSM Dict",
    description="Path to the generated PSSM dictionary.",
    type=VariableTypes.CUSTOM,
    allowedValues=["psmm_dict_jsonl"],
)


# Function to run the assign_fixed_chains.py script
def run_make_pssm(block: PluginBlock):
    """
    Executes the make_pssm_input_dict.py script with the provided arguments.
    """

    output_path = "pssm.jsonl"

    if os.path.exists(output_path):
        os.remove(output_path)

    script_plugin_path = os.path.join(
        block.pluginDir,
        "Include",
        "ProteinMPNN",
        "helper_scripts",
        "make_pssm_input_dict.py",
    )

    input_parsed_chains_value = block.inputs[input_parsed_chains.id]
    pssm_input_path_value = block.inputs[pssm_input_path.id]

    # Build the command to run
    cmd = [
        "python",
        script_plugin_path,
        f"--output_path={output_path}",
        f"--PSSM_input_path={pssm_input_path_value}",
        f"--jsonl_input_path={input_parsed_chains_value}",
    ]
    # Run the command
    from utils import execute_in_environment

    out = execute_in_environment(block, " ".join(cmd))

    print(out)

    block.setOutput(output_path_for_pssm_dict.id, output_path)


# Instantiate the block
make_pssm = PluginBlock(
    id="make_pssm",
    name="Make PSSM dictionary",
    description="This block executes the make_pssm_input_dict.py script to make the PSSM dictionary.",
    inputs=[input_parsed_chains, pssm_input_path],
    outputs=[output_path_for_pssm_dict],
    action=run_make_pssm,
)
