import cadquery as cq
from cqindustry.barricade import WallRuinCorner

bp_wall = WallRuinCorner()
bp_wall.render_grid = True
bp_wall.panel_seed ='mess'
bp_wall.length:float = 30
bp_wall.width:float = 30
bp_wall.height:float = 25
bp_wall.vertical_beam_count = 1
bp_wall.direction = 'right'
bp_wall.debug = False

bp_wall.ruin_shift = (-3,3,1)
bp_wall.vertical_beam_count = 1

bp_wall.seed = 'ascension'
bp_wall.panel_seed = "downfall"
bp_wall.panel_count = 1

bp_wall.make()

ex_wall = bp_wall.build()

#show_object(ex_wall)
cq.exporters.export(ex_wall,'stl/barricade_wall_ruin_corner.stl')