import cadquery as cq
from cqindustry.power import ControlPlatform

bp_control = ControlPlatform()
bp_control.length = 75*3
bp_control.width = 75*2
bp_control.height = 70

bp_p = bp_control.platform_bp
bp_p.height = 5
bp_p.corner_chamfer = 4

bp_p.render_floor = True
bp_p.render_stripes = True
bp_p.bar_width = 10
bp_p.stripe_width = 5
bp_p.stripe_padding = .3

bp_control.make()
control_platform = bp_control.build()

#show_object(control_platform)
cq.exporters.export(control_platform,"stl/power_control_platform_alt.stl")