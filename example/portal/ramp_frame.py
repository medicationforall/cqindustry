import cadquery as cq
from cqindustry.portal import Frame, Ramp

bp_frame = Frame()
bp_frame.width = 30
bp_frame.height = 200
bp_frame.make()
ex_frame = bp_frame.build()

bp_ramp = Ramp()
bp_ramp.width = 10
bp_ramp.side_inset = 10
bp_ramp.render_outside = True
bp_ramp.render_inside = True
bp_ramp.make()
bp_ramp.make(bp_frame)
ex_ramp = bp_ramp.build()

scene = (
    cq.Workplane("XY")
    .add(ex_ramp.translate((0,-30,0)))
    .add(ex_frame)
)

#show_object(scene)

cq.exporters.export(scene, 'stl/portal_ramp_frame.stl')