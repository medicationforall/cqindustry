import cadquery as cq
from cqindustry.dome import Dome
from cqindustry.dome import greeble

bp_dome = Dome()
bp_dome.make()

bp_stairs = greeble.Stairs()
bp_stairs.display_dome = False
bp_stairs.make(bp_dome)

example_stairs = bp_stairs.build()

#show_object(example_stairs)
cq.exporters.export(example_stairs,'stl/dome_stairs.stl')