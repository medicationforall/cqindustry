import cadquery as cq
from cqindustry.container import ContainerDoor

bp_door = ContainerDoor()
bp_door.length = 150
bp_door.width = 5
bp_door.height = 150
bp_door.top_length = 90
bp_door.base_length = 100
bp_door.base_offset = 35 # offset distance from the base of the ramp

bp_door.cut_depth = 2
bp_door.padding = 3
bp_door.frame_width = 2
bp_door.x_translate = 0
bp_door.make()
door = bp_door.build()

#show_object(door)
cq.exporters.export(door, 'stl/container_door.stl')