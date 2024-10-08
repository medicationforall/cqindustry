import cadquery as cq
from cqindustry.chip import ChipTower

bp_tower = ChipTower()
#bp_tower.width = 230
bp_tower.stories = 3
bp_tower.story_height = 75
bp_tower.render_story_proxy = False

bp_platform = bp_tower.bp_platform
bp_platform.render_floor = True

bp_tower.make()
tower_ex = bp_tower.build()

#show_object(tower_ex)
cq.exporters.export(tower_ex, 'stl/chip_readme_example.stl')