import cadquery as cq
from cqindustry.dome import greeble

bp = greeble.VentHexagon()
bp.radius = 58
bp.height = 4
bp.frame_size = 9
bp.vent_width = 2
bp.vent_space = 0.6
bp.vent_rotate = 45
bp.make()
vent = bp.build()

#show_object(vent)
cq.exporters.export(vent,'stl/dome_vent_hexagon.stl')
