import cadquery as cq
from cqindustry.container import ContainerRamp, ContainerDoor

bp_ramp = ContainerRamp()

# Ramp
bp_ramp.length = 150
bp_ramp.width = 10
bp_ramp.height = 150
bp_ramp.top_length = 90
bp_ramp.base_length = 100
bp_ramp.base_offset = 35 # offset distance from the base of the ramp

bp_ramp.side_inset = 8
bp_ramp.frame_size = 10
bp_ramp.inside_margin = 0.4

bp_ramp.render_outside = True
bp_ramp.render_inside = True

# RampGreebled
bp_ramp.segment_count = 20
bp_ramp.segment_x_padding = 2
bp_ramp.segment_y_padding = 3
bp_ramp.segment_depth = 2.5
bp_ramp.render_inside_outline = False

# ContainerRamp
bp_ramp.bp_outside = ContainerDoor()

bp_ramp.make()
ramp_ex = bp_ramp.build()

#show_object(ramp_ex)
cq.exporters.export(ramp_ex, 'stl/container_ramp.stl') 