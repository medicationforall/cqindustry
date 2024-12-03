import cadquery as cq
from cqindustry.dome import greeble

bp = greeble.DoorHexagon()
bp.frame_inset = 9

# door
bp.door_padding = .5
bp.door_chamfer = 1.5
bp.door_height = 4

#hinge
bp.hinge_length = 4
bp.hinge_width = 16
bp.hinge_height = 5
bp.hinge_cylinder_height = 20
bp.hinge_cylinder_radius = 2.5
bp.hinge_x_translate= -3.5

# handle
bp.handle_x_translate = 8.5
bp.handle_length = 5
bp.handle_width = 7

bp.make()
door = bp.build()

#show_object(door)
cq.exporters.export(door,'stl/dome_door_hexagon.stl')