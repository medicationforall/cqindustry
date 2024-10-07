import cadquery as cq
from cqindustry.can import CanPlatform
from cqterrain import tile

bp_can_top = CanPlatform()
bp_can_top.height = 20
bp_can_top.diameter = 75
bp_can_top.cut_diameter = 66.5
bp_can_top.cut_height = 10
bp_can_top.tile_length = 15
bp_can_top.tile_width = 15
bp_can_top.tile_height = 3

bp_can_top.ladder_length = 25
bp_can_top.ladder_width = 5
bp_can_top.ladder_height = 30
bp_can_top.ladder_cut_padding = 1
bp_can_top.ladder_cut_chamfer = 2

bp_can_top.tile_method = tile.bolt_panel
bp_can_top.make()
platform = bp_can_top.build()

#show_object(platform)
cq.exporters.export(platform, 'stl/can_platform.stl')