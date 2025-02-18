import os
import shutil

from HorusAPI import SlurmBlock, PluginVariable, VariableTypes

jsonl_path_variable = PluginVariable(
    id="jsonl_path",
    name="JSONL Path",
    description="Path to the parsed PDB in JSONL format.",
    type=VariableTypes.FILE,
    allowedValues=["jsonl"],
)

suppress_print_variable = PluginVariable(
    id="suppress_print",
    name="Suppress Print",
    description="If set to true, no print statements will be executed.",
    type=VariableTypes.BOOLEAN,
    defaultValue=False,
)

ca_only_variable = PluginVariable(
    id="ca_only",
    name="CA Only",
    description="Parse CA-only structures and use CA-only models.",
    type=VariableTypes.BOOLEAN,
    defaultValue=False,
)

path_to_model_weights_variable = PluginVariable(
    id="path_to_model_weights",
    name="Path to Model Weights",
    description="Path to model weights folder.",
    type=VariableTypes.FOLDER,
    placeholder="Optional",
)

model_name_variable = PluginVariable(
    id="model_name",
    name="Model Name",
    description="ProteinMPNN model name.",
    type=VariableTypes.RADIO,
    defaultValue="v_48_020",
    allowedValues=[
        "v_48_002",
        "v_48_010",
        "v_48_020",
        "v_48_030",
    ],
)

use_soluble_model_variable = PluginVariable(
    id="use_soluble_model",
    name="Use Soluble Model",
    description="Flag to load ProteinMPNN weights trained on soluble proteins only.",
    type=VariableTypes.BOOLEAN,
    defaultValue=False,
)

seed_variable = PluginVariable(
    id="seed",
    name="Seed",
    description="Random seed for reproducibility. If set to 0, a random seed will be used",
    type=VariableTypes.INTEGER,
    defaultValue=0,
)

save_score_variable = PluginVariable(
    id="save_score",
    name="Save Score",
    description="Save score (-log_prob) to npy files.",
    type=VariableTypes.BOOLEAN,
    defaultValue=False,
)

save_probs_variable = PluginVariable(
    id="save_probs",
    name="Save Probs",
    description="Save MPNN predicted probabilities per position.",
    type=VariableTypes.BOOLEAN,
    defaultValue=False,
)

score_only_variable = PluginVariable(
    id="score_only",
    name="Score Only",
    description="Score input backbone-sequence pairs.",
    type=VariableTypes.BOOLEAN,
    defaultValue=False,
)

path_to_fasta_variable = PluginVariable(
    id="path_to_fasta",
    name="Path to Fasta",
    description="Score provided input sequence in a fasta format; e.g. GGGGGG/PPPPS/WWW for chains A, B, C sorted alphabetically and separated by /.",
    type=VariableTypes.FILE,
)

conditional_probs_only_variable = PluginVariable(
    id="conditional_probs_only",
    name="Conditional Probs Only",
    description="Output conditional probabilities p(s_i given the rest of the sequence and backbone).",
    type=VariableTypes.BOOLEAN,
    defaultValue=False,
)

conditional_probs_only_backbone_variable = PluginVariable(
    id="conditional_probs_only_backbone",
    name="Conditional Probs Only Backbone",
    description="Output conditional probabilities p(s_i given backbone).",
    type=VariableTypes.BOOLEAN,
    defaultValue=False,
)

unconditional_probs_only_variable = PluginVariable(
    id="unconditional_probs_only",
    name="Unconditional Probs Only",
    description="Output unconditional probabilities p(s_i given backbone).",
    type=VariableTypes.BOOLEAN,
    defaultValue=False,
)

backbone_noise_variable = PluginVariable(
    id="backbone_noise",
    name="Backbone Noise",
    description="Standard deviation of Gaussian noise to add to backbone atoms.",
    type=VariableTypes.FLOAT,
    defaultValue=0.00,
)

num_seq_per_target_variable = PluginVariable(
    id="num_seq_per_target",
    name="Number of Sequences Per Target",
    description="Number of sequences to generate per target.",
    type=VariableTypes.INTEGER,
    defaultValue=1,
)

batch_size_variable = PluginVariable(
    id="batch_size",
    name="Batch Size",
    description="Batch size for sequence generation.",
    type=VariableTypes.INTEGER,
    defaultValue=1,
)

max_length_variable = PluginVariable(
    id="max_length",
    name="Max Length",
    description="Max sequence length.",
    type=VariableTypes.INTEGER,
    defaultValue=200000,
)

sampling_temp_variable = PluginVariable(
    id="sampling_temp",
    name="Sampling Temperature",
    description="Sampling temperature for amino acids.",
    type=VariableTypes.STRING,
    defaultValue="0.1",
)

pdb_path_variable = PluginVariable(
    id="pdb_path",
    name="PDB Path",
    description="Path to a single PDB to be designed.",
    type=VariableTypes.FILE,
)

pdb_path_chains_variable = PluginVariable(
    id="pdb_path_chains",
    name="PDB Path Chains",
    description="Define which chains need to be designed for a single PDB.",
    type=VariableTypes.FILE,
)

chain_id_jsonl_variable = PluginVariable(
    id="chain_id_jsonl",
    name="Chain ID JSONL",
    description="Path to a dictionary specifying which chains need to be designed.",
    type=VariableTypes.FILE,
    allowedValues=["jsonl"],
)

fixed_positions_jsonl_variable = PluginVariable(
    id="fixed_positions_jsonl",
    name="Fixed Positions JSONL",
    description="Path to a dictionary with fixed positions.",
    type=VariableTypes.FILE,
    allowedValues=["jsonl"],
)

omit_aas_variable = PluginVariable(
    id="omit_AAs",
    name="Omit Amino Acids",
    description="Specify which amino acids should be omitted in the generated sequence.",
    type=VariableTypes.LIST,
    defaultValue=["X"],
    allowedValues=["string"],
)

bias_aa_jsonl_variable = PluginVariable(
    id="bias_AA_jsonl",
    name="Bias AA JSONL",
    description="Path to a dictionary specifying AA composition bias.",
    type=VariableTypes.FILE,
    allowedValues=["jsonl"],
)

bias_by_res_jsonl_variable = PluginVariable(
    id="bias_by_res_jsonl",
    name="Bias by Residue JSONL",
    description="Path to a dictionary with per position bias.",
    type=VariableTypes.FILE,
    allowedValues=["jsonl"],
)

omit_aa_jsonl_variable = PluginVariable(
    id="omit_AA_jsonl",
    name="Omit AA JSONL",
    description="Path to a dictionary specifying which amino acids need to be omitted from design.",
    type=VariableTypes.FILE,
    allowedValues=["jsonl"],
)

pssm_jsonl_variable = PluginVariable(
    id="pssm_jsonl",
    name="PSSM JSONL",
    description="Path to a dictionary with PSSM.",
    type=VariableTypes.FILE,
    allowedValues=["jsonl"],
)

pssm_multi_variable = PluginVariable(
    id="pssm_multi",
    name="PSSM Multi",
    description="Value to determine PSSM usage (0.0 means no PSSM, 1.0 means ignore MPNN predictions).",
    type=VariableTypes.FLOAT,
    defaultValue=0.0,
)

pssm_threshold_variable = PluginVariable(
    id="pssm_threshold",
    name="PSSM Threshold",
    description="Threshold for per position AAs.",
    type=VariableTypes.FLOAT,
    defaultValue=0.0,
)

pssm_log_odds_flag_variable = PluginVariable(
    id="pssm_log_odds_flag",
    name="PSSM Log Odds Flag",
    description="Flag to use PSSM log odds.",
    type=VariableTypes.BOOLEAN,
    defaultValue=False,
)

pssm_bias_flag_variable = PluginVariable(
    id="pssm_bias_flag",
    name="PSSM Bias Flag",
    description="Flag to apply PSSM bias.",
    type=VariableTypes.BOOLEAN,
    defaultValue=False,
)

tied_positions_jsonl_variable = PluginVariable(
    id="tied_positions_jsonl",
    name="Tied Positions JSONL",
    description="Path to a dictionary with tied positions.",
    type=VariableTypes.FILE,
    allowedValues=["jsonl"],
)

# Outputs
out_folder_variable = PluginVariable(
    id="out_folder",
    name="Output Folder",
    description="Path to a folder to output sequences.",
    type=VariableTypes.FOLDER,
)


def run_protein_mpnn(block: SlurmBlock):
    """
    Executes the script
    """

    input_jsonl = block.inputs[jsonl_path_variable.id]

    parameters = ""
    for k, v in block.variables.items():
        if v is not None:
            if isinstance(v, bool):
                if v:
                    parameters += f" --{k}"
            else:
                parameters += f" --{k} '{v}'"

    out_folder_value = "mpnn_output"

    if os.path.exists(out_folder_value):
        shutil.rmtree(out_folder_value)

    os.makedirs(out_folder_value, exist_ok=True)

    script_plugin_path = os.path.join(
        block.pluginDir, "Include", "ProteinMPNN", "protein_mpnn_run.py"
    )

    script = f"python3 {script_plugin_path} --out_folder {out_folder_value} --jsonl_path {input_jsonl} {parameters}"

    from utils import execute_in_environment

    out = execute_in_environment(block, script)

    print(out)

    block.setOutput(out_folder_variable.id, out_folder_value)


protein_mpnn_block = SlurmBlock(
    id="ProteinMPNN",
    name="ProteinMPNN",
    description="This block executes the ProteinMPNN code.",
    inputs=[jsonl_path_variable],
    variables=[
        suppress_print_variable,
        ca_only_variable,
        path_to_model_weights_variable,
        model_name_variable,
        use_soluble_model_variable,
        seed_variable,
        save_score_variable,
        save_probs_variable,
        score_only_variable,
        path_to_fasta_variable,
        conditional_probs_only_variable,
        conditional_probs_only_backbone_variable,
        unconditional_probs_only_variable,
        backbone_noise_variable,
        num_seq_per_target_variable,
        batch_size_variable,
        max_length_variable,
        sampling_temp_variable,
        pdb_path_variable,
        pdb_path_chains_variable,
        jsonl_path_variable,
        chain_id_jsonl_variable,
        fixed_positions_jsonl_variable,
        omit_aas_variable,
        bias_aa_jsonl_variable,
        bias_by_res_jsonl_variable,
        omit_aa_jsonl_variable,
        pssm_jsonl_variable,
        pssm_multi_variable,
        pssm_threshold_variable,
        pssm_log_odds_flag_variable,
        pssm_bias_flag_variable,
        tied_positions_jsonl_variable,
    ],
    initialAction=run_protein_mpnn,
    finalAction=lambda x: None,
    outputs=[out_folder_variable],
)
