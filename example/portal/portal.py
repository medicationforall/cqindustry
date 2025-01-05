import cadquery as cq
from cqindustry.portal import Portal

bp_portal = Portal()
bp_portal.bp_frame.length = 150
bp_portal.bp_frame.width = 30
bp_portal.bp_frame.height = 150

bp_portal.render_base = False
bp_portal.render_hinges = True
bp_portal.bp_ramp.width = 10
bp_portal.make()


result_open = bp_portal.build()
#show_object(result_open)
cq.exporters.export(result_open, 'stl/portal_open.stl')

bp_portal.bp_hinge.rotate_deg = -90
bp_portal.make()

result_closed = bp_portal.build()
#show_object(result_closed.translate((-170,0,0)))
cq.exporters.export(result_closed, 'stl/portal_closed.stl')

