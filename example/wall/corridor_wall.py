import cadquery as cq
from cqindustry.wall import CorridorWall

bp_wall = CorridorWall()

bp_wall.length = 75
bp_wall.width = 12
bp_wall.height = 75
bp_wall.inner_width = 4
bp_wall.inner_height = 25

bp_wall.make()

ex_wall = bp_wall.build()

#show_object(ex_wall)

cq.exporters.export(ex_wall,'stl/wall_corridor_wall.stl')