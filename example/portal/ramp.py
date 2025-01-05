import cadquery as cq
from cqindustry.portal import Ramp

bp_ramp = Ramp()
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

bp_ramp.make()
result = bp_ramp.build()

#show_object(result)
cq.exporters.export(result, 'stl/portal_ramp.stl')