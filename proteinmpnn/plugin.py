from HorusAPI import Plugin

from Blocks.protein_mpnn import protein_mpnn_block
from Blocks.parse_multiple_chains import parse_multiple_chains_block
from Config.config import conda_environment_config

plugin = Plugin()

plugin.addBlock(protein_mpnn_block)
plugin.addBlock(parse_multiple_chains_block)

plugin.addConfig(conda_environment_config)
