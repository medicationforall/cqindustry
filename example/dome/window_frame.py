import cadquery as cq
from cqindustry.dome.greeble import WindowFrame

bp_window = WindowFrame()
bp_window.type= "hexagon" # hexagon, pentagon
bp_window.radius = 58
bp_window.height = 4
bp_window.margin = 0 # used when determing outside radius

bp_window.pane_height = 1 # internal cut height
bp_window.inner_pane_padding = 2
bp_window.pane_rail_translate = 0 
bp_window.frame_size = 5

bp_window.render_pane = False

bp_window.make()
ex_window= bp_window.build()

#show_object(ex_window)

cq.exporters.export(ex_window, 'stl/dome_window_frame_hexagon.stl')

#--------------------------
bp_window.type= "pentagon"
bp_window.make()
ex_window_two = bp_window.build()

cq.exporters.export(ex_window_two, 'stl/dome_window_frame_pentagon.stl')