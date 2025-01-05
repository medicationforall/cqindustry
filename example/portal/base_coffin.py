import cadquery as cq
from cqindustry.portal import BaseCoffin

bp = BaseCoffin()
bp.length = 150
bp.width = 5
bp.height = 150
bp.top_length = 90
bp.base_length = 100
bp.base_offset = 35 # offset distance from the base of the ramp
bp.make()
ex = bp.build()

#show_object(ex)
cq.exporters.export(ex, 'stl/portal_base_coffin.stl')