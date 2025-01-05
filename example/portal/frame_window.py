import cadquery as cq
from cqindustry.portal import FrameWindow

bp_frame = FrameWindow()
bp_frame.length = 150
bp_frame.width = 20
bp_frame.height = 150
bp_frame.top_length = 90 # length at the top of the frame
bp_frame.base_length = 100 # length at the base of the frame
bp_frame.base_offset = 35 # offset distance from the center of the frame
bp_frame.side_inset = 8 # The amount the inset the side frames in relation to the center.
bp_frame.frame_size = 10 # distance from the outside wall and the inside wall.
bp_frame.render_sides = True

bp_frame.window_cut_width = 0.4
bp_frame.window_cut_padding = 1

bp_frame.window_key_width = 2
bp_frame.window_key_padding = 0.8

bp_frame.window_key_text = "Portal Key"
bp_frame.window_key_text_size = 10
bp_frame.window_key_text_height = 1
bp_frame.make()

result = bp_frame.build()

#show_object(result.translate((bp_frame.length/2,0,bp_frame.height/2)))
#show_object(bp_frame.window_cut_key.translate((-(bp_frame.length/2),0,0)))

scene = (
    cq.Workplane("XY")
    .add(result.translate((bp_frame.length/2,0,bp_frame.height/2)))
    .add(bp_frame.window_cut_key.translate((-(bp_frame.length/2),0,0)))
)
cq.exporters.export(scene, 'stl/portal_frame_window.stl')