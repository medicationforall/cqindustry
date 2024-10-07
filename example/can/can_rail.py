import cadquery as cq
from cqindustry.can import CanPlatform, CanRail

bp_platform = CanPlatform()
bp_platform.make()

platform = bp_platform.build()

bp_rail = CanRail()
bp_rail.height = 20
bp_rail.rail_width = 3
bp_rail.rail_height = 2

bp_rail.support_count = 6
bp_rail.support_length = 2.5
bp_rail.support_width = 2
bp_rail.support_height = 25

bp_rail.make(bp_platform)
rail = bp_rail.build()

#show_object(rail)
cq.exporters.export(rail, 'stl/can_rail.stl')