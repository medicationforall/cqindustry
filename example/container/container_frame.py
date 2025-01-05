import cadquery as cq
from cqindustry.container import ContainerFrame

bp_frame = ContainerFrame()

# Frame
bp_frame.length = 150
bp_frame.width = 150
bp_frame.height = 150
bp_frame.top_length = 90 # length at the top of the frame
bp_frame.base_length = 100 # length at the base of the frame
bp_frame.base_offset = 35 # offset distance from the center of the frame
bp_frame.side_inset = 8 # The amount the inset the side frames in relation to the center.
bp_frame.frame_size = 10 # distance from the outside wall and the inside wall.

bp_frame.make()
frame = bp_frame.build()

#show_object(frame)
cq.exporters.export(frame, 'stl/container_frame.stl')