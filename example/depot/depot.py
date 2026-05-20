import cadquery as cq
from cqindustry.depot import Depot

bp_container = Depot()
bp_container.make()

ex_container = bp_container.build()

#show_object(ex_container)
cq.exporters.export(ex_container, 'stl/depot.stl')