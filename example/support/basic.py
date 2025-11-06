import cadquery as cq
from cqindustry.support import Basic

bp_support = Basic()
bp_support.length = 25
bp_support.width = 5
bp_support.height = 50
bp_support.make()
ex_support = bp_support.build()

#show_object(ex_support)
cq.exporters.export(ex_support,'stl/support_basic.stl')