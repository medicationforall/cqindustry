import cadquery as cq
from cqindustry import GuardRail, Platform, make_platform_rails

bp_platform = Platform()
bp_platform.length = 150
bp_platform.width = 150
bp_platform.stripe_width = 5
bp_platform.corner_chamfer = 30
bp_platform.height = 4
bp_platform.bar_width = 10
bp_platform.render_stripes = False
bp_platform.stripe_padding = .3
bp_platform.render_center_cut = True
bp_platform.render_floor = False 
bp_platform.make()
platform = bp_platform.build()

bp_rail = GuardRail()
bp_rail.width = 3
bp_rail.height = 20
bp_rail.frame_padding = 4

bp_rail.render_posts = True
bp_rail.post_length = 7
bp_rail.post_width = 5
bp_rail.post_spacing = 23

bp_rail.render_clamps = True
bp_rail.clamp_length = 6
bp_rail.clamp_width = 7
bp_rail.clamp_height = 8
bp_rail.clamp_cut_width = 3
bp_rail.clamp_cut_height = 3.5
bp_rail.clamp_cut_z_translate = .25
bp_rail.make()
#test_rail = bp_rail.build()

rails, rail_length, rail_width = make_platform_rails(bp_platform, bp_rail, 23+7.5, 23+7.5)

#show_object(r_length)
cq.exporters.export(rail_length,'stl/guard_rail_platorm_test.stl')

scene = (
    cq.Workplane("XY")
    .union(platform)
    .union(rails)
)

#show_object(scene)
cq.exporters.export(scene, 'stl/guard_rail_platorm.stl')