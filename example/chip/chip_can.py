import cadquery as cq
from cqindustry.chip import ChipCan

bp_can = ChipCan()
bp_can.height = 75 * 3
bp_can.diameter = 75
bp_can.make()

can_ex = bp_can.build()

#show_object(can_ex)
cq.exporters.export(can_ex, 'stl/chip_can.stl')