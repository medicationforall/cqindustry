import cadquery as cq
from cqindustry.portal import PortalHinge, Ramp

bp_ramp = Ramp()
bp_ramp.make()

bp_hinge = PortalHinge()

bp_hinge.length = 80
bp_hinge.radius = 2.5
bp_hinge.segments = 3
bp_hinge.pad = 1

bp_hinge.base_inset = 0.6
bp_hinge.key_length = 1.5
bp_hinge.key_width = 0.5

bp_hinge.tab_length = 10
bp_hinge.rotate_deg = -30
bp_hinge.plate_spacer = 0.4

bp_hinge.ramp_bottom_margin = 0
bp_hinge.tab_height = bp_hinge.radius*2
bp_hinge.tab_z_translate = bp_hinge.radius
bp_hinge.invert = False
bp_hinge.hinge_flip = False

bp_hinge.make(bp_ramp)

hinge_ex = bp_hinge.build()

#show_object(hinge_ex)
cq.exporters.export(hinge_ex, 'stl/portal_hinge.stl')