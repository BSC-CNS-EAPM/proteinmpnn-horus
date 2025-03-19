import os

from HorusAPI import PluginBlock, PluginVariable, VariableTypes, VariableList

import json
from Bio.PDB.Polypeptide import standard_aa_names
from Bio.Data.PDBData import protein_letters_3to1, protein_letters_1to3

# Define the variables for the make_fixed_positions block
input_parsed_chains = PluginVariable(
    id="output_parsed_chains",
    name="Parsed Chains JSONL",
    description="The JSONL file containing the parsed chains.",
    type=VariableTypes.CUSTOM,
    allowedValues=["parsed_pdbs_jsonl"],
)

specify_non_fixed = PluginVariable(
    id="specify_non_fixed",
    name="Specify Non Fixed",
    description="If true, only the specified residues will be designed. The mutation selection will not be taken into account, as the selected residues will be automatically designed.",
    type=VariableTypes.BOOLEAN,
    defaultValue=False,
)

chain_list = PluginVariable(
    id="chain_list",
    name="Chain list",
    description="List of the chains that need to be fixed.",
    type=VariableTypes.CHAIN,
)

fixed_residue = PluginVariable(
    id="fixed_residue",
    name="Fixed Residue",
    description="Residue ID that should be fixed for each chain. The order must be consistent with the selected chains.",
    type=VariableTypes.NUMBER,
)

chain_residue_variable = PluginVariable(
    id="chain_residue_variable",
    name="Chain",
    description="Chain",
    type=VariableTypes.STRING,
    placeholder="A",
)

mutate_variable = PluginVariable(
    id="mutate_varialbe",
    name="Mutate variable",
    description="Residue ID that should be mutated for each chain. The order must be consistent with the selected chains.",
    type=VariableTypes.STRING_LIST,
    allowedValues=["-"] + list(standard_aa_names),
)

fixed_positions_mutations = VariableList(
    id="fixed_positions",
    name="Fixed Positions and mutations",
    description="Residues that should remain fixed for each chain.",
    prototypes=[fixed_residue, chain_residue_variable, mutate_variable],
)


# Output
output_fixed_positions = PluginVariable(
    id="output_fixed_positions",
    name="Fixed Positions JSONL",
    description="The JSONL file containing the fixed positions dictionary.",
    type=VariableTypes.CUSTOM,
    allowedValues=["fixed_positions_jsonl"],
)

output_parsed_chains = PluginVariable(
    id="output_parsed_chains",
    name="Parsed Chains JSONL",
    description="The JSONL file containing the mutated sequences. Use this in ProteinMPNN if you have mutated any residue.",
    type=VariableTypes.CUSTOM,
    allowedValues=["parsed_pdbs_jsonl"],
)


# Function to run the make_fixed_positions_dict.py script
def run_make_fixed_positions(block: PluginBlock):
    """
    Executes the make_fixed_positions_dict.py script with the provided arguments.
    """
    input_path = block.inputs[input_parsed_chains.id]
    specify_non_fixed_value = block.variables[specify_non_fixed.id]

    output_path = "fixed_positions.jsonl"

    if os.path.exists(output_path):
        os.remove(output_path)

    fixed_positions_value = block.variables[fixed_positions_mutations.id]

    # Apply the mutations to the original fixed_positions.jsonl file.
    mutated_json = os.path.basename(input_path).split(".")[0] + "_mutated.jsonl"

    if not specify_non_fixed_value:
        original_seqs_chains = None
        with open(input_path, "r") as input_file:
            original_seqs_chains = json.load(input_file)

    chains_pos = {}
    has_mutations = False
    for r in fixed_positions_value:
        chain = r[chain_residue_variable.id]
        pos = r[fixed_residue.id]
        mutation = r[mutate_variable.id]

        if not chain in chains_pos:
            chains_pos[chain] = []

        chains_pos[chain].append(str(pos))

        if not specify_non_fixed_value:
            if mutation in standard_aa_names:
                has_mutations = True
                pos_index = pos - 1  # Indeces in python start with 0!
                print(
                    f"- Mutating {original_seqs_chains['seq'][pos_index]} ({protein_letters_1to3[original_seqs_chains['seq'][pos_index]]}) to {protein_letters_3to1[mutation]} ({mutation}) at {pos} in chain {chain}"
                )
                # Get the original sequence string
                seq = original_seqs_chains["seq"]
                seq_chain = original_seqs_chains[f"seq_chain_{chain}"]

                # Modify the sequence by creating a new string
                original_seqs_chains["seq"] = (
                    seq[:pos_index]
                    + protein_letters_3to1[mutation]
                    + seq[pos_index + 1 :]
                )
                original_seqs_chains[f"seq_chain_{chain}"] = (
                    seq_chain[:pos_index]
                    + protein_letters_3to1[mutation]
                    + seq_chain[pos_index + 1 :]
                )

    # Store the new JSONL file
    if has_mutations:
        with open(mutated_json, "w") as output_file:
            json.dump(original_seqs_chains, output_file)

    chains_argument = " ".join(chains_pos.keys())
    positions_argument = ",".join([" ".join(chains_pos[c]) for c in chains_pos.keys()])

    print(f"- Fixed positions: {positions_argument}")

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
        f'"{chains_argument}"',
        "--position_list",
        f'"{positions_argument}"',
    ]

    if specify_non_fixed_value:
        cmd.append("--specify_non_fixed")

    # Run the command
    from utils import execute_in_environment

    out = execute_in_environment(block, " ".join(cmd))

    print(out)

    block.setOutput(output_fixed_positions.id, output_path)
    block.setOutput(output_parsed_chains.id, mutated_json)


# Instantiate the block
make_fixed_positions_block = PluginBlock(
    id="make_fixed_positions",
    name="Make Fixed Positions and Mutations",
    description="This block executes the make_fixed_positions_dict.py script to define fixed positions for a protein structure. Furthermore, it allows to define mutations on the fixed positions.",
    inputs=[input_parsed_chains, chain_list],
    variables=[specify_non_fixed, fixed_positions_mutations],
    outputs=[output_fixed_positions, output_parsed_chains],
    action=run_make_fixed_positions,
)
