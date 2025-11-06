import cadquery as cq
from cqindustry.support import Strut

bp_support = Strut()
# basic parameters
bp_support.length = 25
bp_support.width = 5
bp_support.height = 50

#segmented parameters
bp_support.segments = 5
bp_support.side_length = 2
bp_support.height_margin = 3
bp_support.tile_depth = 1

#strut parameters
bp_support.strut_width = 1.5

bp_support.make()
ex_support = bp_support.build()

#show_object(ex_support)
cq.exporters.export(ex_support,'stl/support_strut.stl')