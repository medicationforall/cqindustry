import cadquery as cq
from cqindustry.portal import Portal

bp_portal = Portal()
bp_portal.render_base = False

bp_portal.bp_frame.width = 150

bp_portal.bp_frame.top_length = 90
bp_portal.bp_frame.base_length = 100
bp_portal.bp_frame.base_offset = 35
bp_portal.bp_frame.render_sides = True

bp_portal.bp_hinge.rotate_deg = -90
bp_portal.bp_hinge.ramp_bottom_margin = 0

bp_portal.bp_ramp.render_outside = True

bp_portal.make()

result = bp_portal.build()

#show_object(result)
cq.exporters.export(result, 'stl/portal_rotation_demo.stl')