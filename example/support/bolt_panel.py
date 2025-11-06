import cadquery as cq
from cqindustry.support import BoltPanel

bp_support = BoltPanel()
# basic parameters
bp_support.length = 25
bp_support.width = 5
bp_support.height = 50

#segmented parameters
bp_support.segments = 5
bp_support.side_length = 2
bp_support.height_margin = 3
bp_support.tile_depth = 1

#bolt panel parameters
bp_support.chamfer = 0.5
bp_support.radius_outer = 1
bp_support.radius_internal = 0.5
bp_support.cut_height = 0.5
bp_support.padding = 2

bp_support.make()
ex_support = bp_support.build()

#show_object(ex_support)
cq.exporters.export(ex_support,'stl/support_bolt_panel.stl')