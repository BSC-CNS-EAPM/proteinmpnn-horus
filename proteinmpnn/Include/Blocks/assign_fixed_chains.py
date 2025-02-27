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

# Output
output_fixed_chains = PluginVariable(
    id="output_assigned_chains",
    name="Assigned chains JSONL",
    description="The JSONL file containing the assigned chains.",
    type=VariableTypes.CUSTOM,
    allowedValues=["assigned_chains_jsonl"],
)

output_selected_chains = PluginVariable(
    id="output_selected_chains",
    name="Selected chains",
    description="The selected chains",
    type=VariableTypes.CHAIN,
)


# Function to run the assign_fixed_chains.py script
def run_passign_chains(block: PluginBlock):
    """
    Executes the assign_fixed_chains.py script with the provided arguments.
    """
    input_path = block.inputs[input_parsed_chains.id]

    output_path = "assigned_chains.jsonl"

    if os.path.exists(output_path):
        os.remove(output_path)

    chain_list_value = block.inputs[chain_list.id]

    chains = [c["chainID"] for c in chain_list_value]

    print(f"Selected chains: {chains}")

    script_plugin_path = os.path.join(
        block.pluginDir,
        "Include",
        "ProteinMPNN",
        "helper_scripts",
        "assign_fixed_chains.py",
    )

    # Build the command to run
    cmd = [
        "python",
        script_plugin_path,
        f"--input_path={input_path}",
        f"--output_path={output_path}",
        "--chain_list",
        f'"{" ".join(chains)}"',
    ]

    # Run the command
    from utils import execute_in_environment

    out = execute_in_environment(block, " ".join(cmd))

    print(out)

    block.setOutput(output_fixed_chains.id, output_path)


# Instantiate the block
assign_chains_block = PluginBlock(
    id="assign_chains",
    name="Assign Fixed Chains",
    description="This block executes the assign_fixed_chains.py script to assign the desing chains to a protein structure.",
    inputs=[input_parsed_chains, chain_list],
    outputs=[
        output_fixed_chains,
    ],
    action=run_passign_chains,
)
