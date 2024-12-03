import cadquery as cq
from cqindustry.dome import Dome, greeble

bp_0 = greeble.CutKeyPentagon()
bp_0.text='0'

bp_1 = greeble.CutKeyHexagon()
bp_1.text='1'


vent_bp = greeble.VentHexagon()
door_bp = greeble.DoorHexagon()
door_bp.hinge_x_translate = -4.5

window_pen_bp = greeble.WindowFrame()
window_pen_bp.type="pentagon"
window_pen_bp.margin=.1

window_hex_bp = greeble.WindowFrame()
window_hex_bp.type="hexagon"


bp = Dome()

#center
bp.greebles_bp.append(None)

#ring 1
bp.greebles_bp.append(vent_bp)
bp.greebles_bp.append(None)
bp.greebles_bp.append(None)
bp.greebles_bp.append(None)
bp.greebles_bp.append(None)

#ring2
bp.greebles_bp.append(None)
bp.greebles_bp.append(None)
bp.greebles_bp.append(None)
bp.greebles_bp.append(None)
bp.greebles_bp.append(None)
bp.greebles_bp.append(None)
bp.greebles_bp.append(None)
bp.greebles_bp.append(window_hex_bp)
bp.greebles_bp.append(window_pen_bp)
bp.greebles_bp.append(door_bp)

bp.render_greebles = True
bp.make()
dome = bp.build()

greebles = (
    cq.Workplane("XY")
    .add(window_pen_bp.build().translate((42,0,2)))
    .add(window_hex_bp.build().translate((0,0,2)))
    .add(vent_bp.build().translate((0,-44,2)))
    .add(door_bp.build().translate((0,44,2)))
)


window_hex_frame = (
    window_hex_bp.build()
    .rotate((0,0,1),(0,0,0),60)
    .rotate((1,0,0),(0,0,0),90)
    .translate((0,20,0))
)

window_pen_frame = (
    window_pen_bp.build()
    .rotate((0,0,1),(0,0,0),54+36)
    .rotate((1,0,0),(0,0,0),90)
    .translate((0,0,0))
)

pen_key = (
    window_pen_bp.cut_key_bp.build() #type:ignore
)

hex_key = (
    window_hex_bp.cut_key_bp.build() #type:ignore
)

#show_object(window_hex_frame) 
#show_object(window_pen_frame)

cq.exporters.export(dome, "./stl/dome_v3_test.stl")
cq.exporters.export(greebles, "./stl/dome_v3_greebles.stl")

cq.exporters.export(window_hex_frame, "./stl/dome_v3_hex_frame.stl")
cq.exporters.export(window_pen_frame, "./stl/dome_v3_pen_frame.stl")
cq.exporters.export(hex_key, "./stl/dome_v3_hex_key.stl")
cq.exporters.export(pen_key, "./stl/dome_v3_pen_key.stl")