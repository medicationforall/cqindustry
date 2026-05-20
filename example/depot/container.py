import cadquery as cq
from cqindustry.depot import Container

bp_container = Container()

bp_container.length = 126
bp_container.width = 114
bp_container.height = 65

bp_container.top_length = 111
bp_container.top_width = 93
bp_container.top_fillet = 8
bp_container.side_fillet = 9

bp_container.material_width = 1

bp_container.make()

ex_container = bp_container.build()

#show_object(ex_container)
cq.exporters.export(ex_container, 'stl/depot_container.stl')