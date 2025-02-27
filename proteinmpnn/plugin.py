from HorusAPI import Plugin

from Blocks.protein_mpnn import protein_mpnn_block
from Blocks.parse_multiple_chains import parse_multiple_chains_block
from Blocks.assign_fixed_chains import assign_chains_block
from Blocks.make_fixed_positions import make_fixed_positions_block
from Blocks.make_tied_positions import make_tied_positions
from Blocks.make_bias import make_bias
from Blocks.make_pssm import make_pssm

from Config.config import conda_environment_config

plugin = Plugin()

# Blocks
plugin.addBlock(protein_mpnn_block)
plugin.addBlock(parse_multiple_chains_block)
plugin.addBlock(assign_chains_block)
plugin.addBlock(make_fixed_positions_block)
plugin.addBlock(make_tied_positions)
plugin.addBlock(make_bias)
plugin.addBlock(make_pssm)

# Configs
plugin.addConfig(conda_environment_config)
