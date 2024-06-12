
import cadquery as cq
from cqindustry import GuardRail

bp_rail = GuardRail()

bp_rail.length = 75
bp_rail.width = 3
bp_rail.height = 25
bp_rail.corner_chamfer = 5
bp_rail.frame_padding = 4

bp_rail.render_posts = True
bp_rail.post_length = 3
bp_rail.post_width = 3
bp_rail.post_spacing = 20

bp_rail.render_clamps = True
bp_rail.clamp_length = 6
bp_rail.clamp_width = 6
bp_rail.clamp_height = 6
bp_rail.clamp_padding = 2
bp_rail.clamp_spacing = 30
bp_rail.clamp_cut_width = 1
bp_rail.clamp_cut_height = 3
bp_rail.clamp_cut_z_translate = 0.5
bp_rail.clamp_y_translate = -1

bp_rail.make()
test_rail = bp_rail.build()

#show_object(test_rail)
cq.exporters.export(test_rail,'./stl/guard_rail.stl')