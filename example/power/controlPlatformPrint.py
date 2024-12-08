import cadquery as cq
from cqindustry.power import ControlPlatformPrint

bp_control = ControlPlatformPrint()
bp_control.length = 150
bp_control.width = 75
bp_control.height = 71

bp_control.y_height = 8
bp_control.frame_insert_margin = .6
bp_control.frame_insert_height = 1
bp_control.frame_insert_height_margin = 1

bp_p = bp_control.platform_bp
bp_p.height = 4
bp_p.corner_chamfer = 4

bp_p.render_floor = True
bp_p.render_stripes = True
bp_p.bar_width = 10
bp_p.stripe_width = 5
bp_p.stripe_padding = .3

bp_control.make()

control_platform = bp_control.build()
#show_object(control_platform)
cq.exporters.export(control_platform,"stl/power_control_platform_print.stl")

platform = bp_control.build_print_patform()
#show_object(platform)
cq.exporters.export(platform,"stl/power_control_platform_platform.stl")

frame = bp_control.build_print_frame()
#show_object(frame)
cq.exporters.export(frame,"stl/power_control_platform_frame.stl")

frame_single = bp_control.build_print_frame_single()
#show_object(frame_single)
cq.exporters.export(frame_single,"stl/power_control_platform_frame_single.stl")
