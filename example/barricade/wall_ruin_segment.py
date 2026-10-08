import cadquery as cq
from cqindustry.barricade import WallRuinSegment

bp_wall = WallRuinSegment()
bp_wall.seed = "newSelf"
bp_wall.length = 75
bp_wall.width= 30
bp_wall.height = 25
bp_wall.ruin_seed = None
bp_wall.panel_cut_seed = None
bp_wall.ruin_shift = (-1,3,1)
bp_wall.vertical_beam_count = 2

bp_wall.debug = False
bp_wall.direction = 'top'
bp_wall.ruin_height = 12.5
bp_wall.ruin_points= 7
bp_wall.ruin_padding = -10

bp_wall.make()

ex_wall = bp_wall.build()

#show_object(ex_wall)
cq.exporters.export(ex_wall,'stl/barricade_wall_ruin_segment.stl')