import cadquery as cq
from cqindustry.segment import SegmentFloor

bp_floor = SegmentFloor()
bp_floor.length = 75
bp_floor.width = 75
bp_floor.height = 4
bp_floor.top_padding = 1

bp_floor.make()

ex_floor = bp_floor.build()

#show_object(ex_floor)

cq.exporters.export(ex_floor,'stl/segment_floor.stl')