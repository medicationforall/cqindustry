import cadquery as cq 
from cqindustry.container import ContainerLadder, ContainerFrame

bp_frame = ContainerFrame()
bp_frame.width = 200
bp_frame.make()
frame = bp_frame.build()

bp_ladder = ContainerLadder()
bp_ladder.width = bp_frame.width / 5
bp_ladder.x_padding = 2
bp_ladder.ladder_depth = 6
bp_ladder.ladder_rungs = 8
bp_ladder.ladder_rung_radius = 2

bp_ladder.make(bp_frame)
ladder_cut, ladder_rungs = bp_ladder.build()

scene = (
    cq.Workplane("XY")
    .add(frame.translate((-20,0,0)))
    .add(ladder_cut)
    .add(ladder_rungs.translate((0,-40,0)))
)

#show_object(scene)
cq.exporters.export(scene, 'stl/container_ladder_exploded.stl')