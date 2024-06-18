import cadquery as cq
from cqindustry import ChipTower, Ring, RingConduit

bp_tower = ChipTower()

bp_tower.bp_ring=(Ring(), RingConduit(), Ring(), Ring()) #type:ignore
#bp_tower.width = 230
bp_tower.render_rings=False
bp_tower.stories = 4
bp_tower.story_height = 50
bp_tower.render_story_proxy = False

bp_platform = bp_tower.bp_platform
bp_platform.render_floor = False

bp_tower.make()
tower_ex = bp_tower.build()

#show_object(tower_ex)
cq.exporters.export(tower_ex, 'stl/chip_tower_set_2.stl')
