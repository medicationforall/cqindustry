import cadquery as cq
from cqindustry.can import CanTower

bp_can_tower = CanTower()
bp_can_tower.render_can = False
bp_can_tower.can_height = 122
bp_can_tower.can_diameter = 66
bp_can_tower.cut_padding = .5
bp_can_tower.ring_width = 4.5
bp_can_tower.platform_height = 20
bp_can_tower.platform_ladder_extends = 10
bp_can_tower.pipe_length = 75

bp_can_tower.make()
can_tower = bp_can_tower.build()

#show_object(can_tower.translate((0,0,0)))
cq.exporters.export(can_tower, 'stl/can_tower.stl')

can_tower_plate = bp_can_tower.build_plate()
cq.exporters.export(can_tower_plate, 'stl/can_tower_plate.stl')
