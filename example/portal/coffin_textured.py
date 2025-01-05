import cadquery as cq
from cqindustry.portal import CoffinTextured

bp_coffin = CoffinTextured()
bp_coffin.seed = 'rough'

bp_coffin.max_columns = 4
bp_coffin.max_rows = 2
bp_coffin.col_size = 15
bp_coffin.row_size = 15

bp_coffin.passes_count = 36
bp_coffin.make()

coffin = bp_coffin.build()

#show_object(coffin)

cq.exporters.export(coffin, "stl/portal_coffin_textured.stl")