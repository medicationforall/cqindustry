import cadquery as cq
from cqindustry.portal import FrameWindowBlock

bp_frame = FrameWindowBlock()
bp_frame.length = 150
bp_frame.width = 22
bp_frame.height = 150
bp_frame.top_length = 90 # length at the top of the frame
bp_frame.base_length = 100 # length at the base of the frame
bp_frame.base_offset = 35 # offset distance from the center of the frame
bp_frame.side_inset = 8 # The amount the inset the side frames in relation to the center.
bp_frame.frame_size = 10 # distance from the outside wall and the inside wall.
bp_frame.render_sides = True

bp_frame.seed = 'test'
bp_frame.max_columns = 2
bp_frame.max_rows = 3
bp_frame.col_size = 10
bp_frame.row_size = 10
bp_frame.passes_count = 1000
bp_frame.power_offset  = 4

bp_frame.window_cut_width = 3
bp_frame.window_cut_padding = 1

bp_frame.make()

result = bp_frame.build()

#show_object(result)
cq.exporters.export(result, 'stl/portal_frame_window_block.stl')