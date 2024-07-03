import cadquery as cq
from cqindustry import CanPlatform, CanRail
from cadqueryhelper import Base

bp_platform = CanPlatform()
bp_platform.make()

platform = bp_platform.build()

bp_rail = CanRail()
bp_rail.make(bp_platform)
rail = bp_rail.build()

#show_object(rail)
cq.exporters.export(rail, 'stl/can_rail.stl')