import cadquery as cq
from cqindustry import CanTower
from cqterrain import tile

#-------------------
# regular soda can
bp_can_tower = CanTower()
bp_can_tower.render_can = True
bp_can_tower.can_height = 122
bp_can_tower.can_diameter = 66
bp_can_tower.cut_padding = .5
bp_can_tower.ring_width = 4.5
bp_can_tower.platform_height = 20
bp_can_tower.platform_ladder_extends = 15
bp_can_tower.make()
soda_can_tower = bp_can_tower.build()

#-------------------
# red bull can
bp_can_tower_2 = CanTower()
bp_can_tower_2.render_can = True
bp_can_tower_2.can_height = 155
bp_can_tower_2.can_diameter = 55
bp_can_tower_2.cut_padding = .5
bp_can_tower_2.ring_width = 4.5
bp_can_tower_2.platform_height = 10
bp_can_tower_2.platform_ladder_extends = 10
bp_can_tower_2.bp_platform.tile_method = tile.slot_diagonal

bp_can_tower_2.make()
red_bull_can_tower = bp_can_tower_2.build()


#-------------------
scene =(
        cq.Workplane("XY")
        .add(soda_can_tower)
        .add(red_bull_can_tower.translate((0,80,0)))
)

#show_object(scene)
cq.exporters.export(scene, 'stl/can_tower_set.stl')