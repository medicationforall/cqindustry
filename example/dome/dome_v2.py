import cadquery as cq
from cqindustry.dome import Dome

bp = Dome()
bp.hex_height = 4
#bp.pen_radius_cut_distance = 20
#bp.render_cut_keys = True
bp.make()
test = bp.build()

#show_object(test)
cq.exporters.export(test, "./stl/dome_v2_test.stl")
