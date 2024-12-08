import cadquery as cq
from cqindustry.power import SteelFrame
    
bp_frame = SteelFrame()
bp_frame.length = 75*2
bp_frame.width = 75*1
bp_frame.height = 70
bp_frame.segment_length = 75
bp_frame.segment_width = 75
bp_frame.z_width = 5
bp_frame.z_height = 10
bp_frame.y_width = 5
bp_frame.render_debug_outline = False
bp_frame.render_debug_grid = False
bp_frame.make()
ex_frame = bp_frame.build()

#show_object(ex_frame)
cq.exporters.export(ex_frame,"stl/power_steel_frame.stl")