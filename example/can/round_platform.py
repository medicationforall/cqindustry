import cadquery as cq
from cqindustry.can import RoundPlatform

bp_platform = RoundPlatform()

bp_platform.inner_diameter = 30
bp_platform.outer_diameter = 55
bp_platform.height = 4
bp_platform.angle = 90

bp_platform.make()

ex_platform = bp_platform.build()

#show_object(ex_platform)

cq.exporters.export(ex_platform,'stl/can_round_platform.stl')