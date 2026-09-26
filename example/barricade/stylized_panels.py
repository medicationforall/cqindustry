import cadquery as cq
from cqindustry.barricade import stylized_panels

result = stylized_panels(
    length = 75,
    width = 10,
    height=2,
    count=(2,3,1),
    seed = "seed",
    rotate = (-45,45,5)
    #tiles = [rivet,bolt_panel]
)

#show_object(result)
cq.exporters.export(result,'stl/barricade_stylized_panels.stl')