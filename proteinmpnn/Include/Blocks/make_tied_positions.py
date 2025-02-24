import os

from HorusAPI import PluginBlock, PluginVariable, VariableTypes

# Define the variables for the parse_multiple_chains block
input_parsed_chains = PluginVariable(
    id="output_parsed_chains",
    name="Parsed Chains JSONL",
    description="The JSONL file containing the parsed chains.",
    type=VariableTypes.CUSTOM,
    allowedValues=["parsed_pdbs_jsonl"],
)

chain_list = PluginVariable(
    id="chain_list",
    name="Chain list",
    description="List of the chains that need to be designed."
    " Note: Independently of the model, only the Chain ID will be considered."
    " Therefore, if the same chain ID (i.e. 'A') appears repeated, "
    "then it does not need to be selected twice.",
    type=VariableTypes.CHAIN,
)

# Variables
tied_positions = PluginVariable(
    id="tied_positions",
    name="Tied positions",
    description="Residue positions to be tied. Lists must match in length.",
    type=VariableTypes.LIST,
)

# Output
output_path_for_tied_positions = PluginVariable(
    id="output_path_for_tied_positions",
    name="Tied positions JSONL",
    description="The JSONL file containing the tied positions.",
    type=VariableTypes.CUSTOM,
    allowedValues=["tied_positions_jsonl"],
)


# Function to run the assign_fixed_chains.py script
def run_tied_positions(block: PluginBlock):
    """
    Executes the make_tied_positions.py script with the provided arguments.
    """
    input_path = block.inputs[input_parsed_chains.id]

    output_path = "tied_positions.jsonl"

    if os.path.exists(output_path):
        os.remove(output_path)

    chain_list_value = block.inputs[chain_list.id]

    chains = [c["chainID"] for c in chain_list_value]

    tied_positions_value = block.variables[tied_positions.id]

    print("Tied positions: ", "\n".join(tied_positions_value))

    script_plugin_path = os.path.join(
        block.pluginDir,
        "Include",
        "ProteinMPNN",
        "helper_scripts",
        "make_tied_positions_dict.py",
    )

    # Build the command to run
    cmd = [
        "python",
        script_plugin_path,
        f"--input_path={input_path}",
        f"--output_path={output_path}",
        "--chain_list",
        f'"{" ".join(chains)}"',
        "--position_list",
        f'"{",".join(tied_positions_value)}"',
    ]

    # Run the command
    from utils import execute_in_environment

    out = execute_in_environment(block, " ".join(cmd))

    print(out)

    block.setOutput(output_path_for_tied_positions.id, output_path)


# Instantiate the block
make_tied_positions = PluginBlock(
    id="make_tied_positions",
    name="Make Tied Positions",
    description="This block executes the make_tied_positions.py script to make tied positions for a protein structure.",
    inputs=[input_parsed_chains, chain_list],
    variables=[tied_positions],
    outputs=[output_path_for_tied_positions],
    action=run_tied_positions,
)
