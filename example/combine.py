import cadquery as cq
from cqindustry import Platform, Ring

bp = Platform()
bp.make()
platform = bp.build()

bp = Ring()
bp.make()
ring = bp.build()

scene = (
    cq.Workplane("XY")
    .add(platform.translate((0,0,3)))
    .add(
        ring
        .rotate((1,0,0),(0,0,0),180)
        .rotate((0,0,1),(0,0,0),45)
    )
)

#show_object(scene)
cq.exporters.export(scene, 'stl/combine.stl')
