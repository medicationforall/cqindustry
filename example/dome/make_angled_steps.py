import cadquery as cq
from cqindustry.dome.greeble import make_angled_steps

angled_steps = make_angled_steps(
    length = 30, 
    width = 10, 
    height = 15,
    dec = 5
)

# show_object(angled_steps)

cq.exporters.export(angled_steps,'stl/dome_angled_steps.stl')



