import cadquery as cq
from cqindustry.can import CanPlatform

bp_can_top = CanPlatform()
bp_can_top.height = 20
bp_can_top.make()
platform = bp_can_top.build()

#show_object(platform)
cq.exporters.export(platform, 'stl/can_platform.stl')