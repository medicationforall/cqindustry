import cadquery as cq
from cqindustry.portal import RampGreebledTwo

bp_ramp = RampGreebledTwo()
#bp_ramp.length = 70
#bp_ramp.width = 10
#bp_ramp.height = 150
#bp_ramp.top_length = 60
bp_ramp.base_length = 80

bp_ramp.segment_x_padding = 1
bp_ramp.render_inside = True
bp_ramp.render_inside_outline = False
bp_ramp.make()
ex_ramp = bp_ramp.build()

#show_object(ex_ramp)
cq.exporters.export(ex_ramp, 'stl/portal_ramp_greebled_two.stl')