import cadquery as cq
from cqindustry.dome.greeble import make_pentagon

pentagon = make_pentagon(
    radius = 30,
    height = 3,
    z_rotate = 30
)

#show_object(pentagon)

cq.exporters.export(pentagon, 'stl/dome_make_pentagon.stl')