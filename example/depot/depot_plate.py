import cadquery as cq
from cqindustry.depot import Depot

bp_container = Depot()
bp_container.make()

ex_container_plate = bp_container.build_plate()

#show_object(ex_container_plate)
cq.exporters.export(ex_container_plate, 'stl/depot_plate.stl')