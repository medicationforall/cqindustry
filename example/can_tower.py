import cadquery as cq
from cqindustry import CanTower

bp_can_tower = CanTower()
bp_can_tower.render_can = False
bp_can_tower.make()
can_tower = bp_can_tower.build()

#show_object(can_tower.translate((0,0,0)))
cq.exporters.export(can_tower, 'stl/can_tower.stl')