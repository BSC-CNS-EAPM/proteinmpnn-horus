import os

from HorusAPI import PluginBlock, PluginVariable, VariableTypes

# Define the variables for the parse_multiple_chains block
input_pdbs_folder = PluginVariable(
    id="input_pdbs_folder",
    name="PDBs Folder",
    description="The folder containing the PDBs to be processed by the parse_multiple_chains script.",
    type=VariableTypes.FOLDER,
)

ca_only = PluginVariable(
    id="ca_only",
    name="CA Only",
    description="If set to true, parse a backbone-only structure.",
    type=VariableTypes.BOOLEAN,
    defaultValue=False,
)

# Output
output_parsed_chains = PluginVariable(
    id="output_parsed_chains",
    name="Parsed Chains JSONL",
    description="The JSONL file containing the parsed chains.",
    type=VariableTypes.CUSTOM,
    allowedValues=["parsed_pdbs_jsonl"],
)


# Function to run the parse_multiple_chains.py script
def run_parse_multiple_chains(block: PluginBlock):
    """
    Executes the parse_multiple_chains.py script with the provided arguments.
    """
    input_path = block.inputs[input_pdbs_folder.id]

    output_path = "parsed_pdbs.jsonl"

    if os.path.exists(output_path):
        os.remove(output_path)

    ca_only_value = block.variables[ca_only.id]

    script_plugin_path = os.path.join(
        block.pluginDir,
        "Include",
        "ProteinMPNN",
        "helper_scripts",
        "parse_multiple_chains.py",
    )

    # Build the command to run
    cmd = [
        "python",
        script_plugin_path,
        f"--input_path={input_path}",
        f"--output_path={output_path}",
    ]

    if ca_only_value:
        cmd.append("--ca_only")

    # Run the command
    from utils import execute_in_environment

    out = execute_in_environment(block, " ".join(cmd))

    print(out)

    block.setOutput(output_parsed_chains.id, output_path)


# Instantiate the block
parse_multiple_chains_block = PluginBlock(
    id="ParseMultipleChains",
    name="Parse Multiple Chains",
    description="This block executes the parse_multiple_chains.py script to process PDBs.",
    inputs=[input_pdbs_folder],
    variables=[ca_only],
    outputs=[output_parsed_chains],
    action=run_parse_multiple_chains,
)
