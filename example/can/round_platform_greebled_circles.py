import cadquery as cq
from cqindustry.can import RoundPlatformGreebledCircles

bp_platform = RoundPlatformGreebledCircles()

bp_platform.inner_diameter = 40
bp_platform.outer_diameter = 100
bp_platform.width = 25
bp_platform.height = 4
bp_platform.tile_height = 1
bp_platform.spacing = 10
bp_platform.rows = 11
bp_platform.taper = None
bp_platform.offset = -1
bp_platform.angle = 180
bp_platform.tile_height = 2
bp_platform.circle_diameter = 2.8
bp_platform.cut_circle_diameter = 2
bp_platform.circle_max_index = 1

bp_platform.make()

ex_platform = bp_platform.build()

#show_object(ex_platform)

cq.exporters.export(ex_platform,'stl/can_round_platform_greebled_circles.stl')