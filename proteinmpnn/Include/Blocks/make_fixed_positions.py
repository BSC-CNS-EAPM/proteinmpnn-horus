import os

from HorusAPI import PluginBlock, PluginVariable, VariableTypes

# Define the variables for the make_fixed_positions block
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
    description="List of the chains that need to be fixed.",
    type=VariableTypes.CHAIN,
)

fixed_positions = PluginVariable(
    id="fixed_positions",
    name="Fixed Positions",
    description="Space separated residue indices that should remain fixed for each chain. The order must be consistent with the selected chains. (i.e. chain A and B will be assigned first list and second list accordingly)",
    type=VariableTypes.LIST,
)

# Output
output_fixed_positions = PluginVariable(
    id="output_fixed_positions",
    name="Fixed Positions JSONL",
    description="The JSONL file containing the fixed positions dictionary.",
    type=VariableTypes.CUSTOM,
    allowedValues=["fixed_positions_jsonl"],
)


# Function to run the make_fixed_positions_dict.py script
def run_make_fixed_positions(block: PluginBlock):
    """
    Executes the make_fixed_positions_dict.py script with the provided arguments.
    """
    input_path = block.inputs[input_parsed_chains.id]
    output_path = "fixed_positions.jsonl"

    if os.path.exists(output_path):
        os.remove(output_path)

    chain_list_value = block.inputs[chain_list.id]
    fixed_positions_value = block.variables[fixed_positions.id]

    chains = [c["chainID"] for c in chain_list_value]
    positions = [str(pos) for pos in fixed_positions_value]

    print(f"Selected chains: {chains}")
    print(f"Fixed positions: {positions}")

    script_plugin_path = os.path.join(
        block.pluginDir,
        "Include",
        "ProteinMPNN",
        "helper_scripts",
        "make_fixed_positions_dict.py",
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
        f'"{",".join(positions)}"',
    ]

    # Run the command
    from utils import execute_in_environment

    out = execute_in_environment(block, " ".join(cmd))

    print(out)

    block.setOutput(output_fixed_positions.id, output_path)


# Instantiate the block
make_fixed_positions_block = PluginBlock(
    id="make_fixed_positions",
    name="Make Fixed Positions",
    description="This block executes the make_fixed_positions_dict.py script to define fixed positions for a protein structure.",
    inputs=[input_parsed_chains, chain_list],
    variables=[fixed_positions],
    outputs=[output_fixed_positions],
    action=run_make_fixed_positions,
)
