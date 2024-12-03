import cadquery as cq
from cqindustry.dome import greeble

bp = greeble.CutKeyPentagon()
bp.radius = 58
bp.height = 2

# text
bp.text = "MiniForAll" 
bp.text_height = 2
bp.text_size = 7

#cut hole
bp.cut_hole_height = 3
bp.cut_hole_radius = 1.5
bp.cut_hole_y_translate = 12

bp.make()
cut_key = bp.build()

#show_object(cut_key)
cq.exporters.export(cut_key,'stl/dome_cut_key_pentagon.stl')