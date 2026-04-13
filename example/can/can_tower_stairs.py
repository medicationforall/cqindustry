import cadquery as cq
from cqindustry.can import CanTowerStairs

bp_tower = CanTowerStairs()

bp_tower.diameter = 73
bp_tower.height = 194

bp_tower.render_can = True
bp_tower.render_pipe = True
bp_tower.make()

ex_tower = bp_tower.build()

#show_object(ex_tower)
cq.exporters.export(ex_tower,'stl/can_tower_stairs.stl')