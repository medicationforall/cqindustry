import cadquery as cq
from cqindustry.portal import EnergyInsert

bp_iris = EnergyInsert()
bp_iris.length = 150
bp_iris.height = 150
bp_iris.width = 5
bp_iris.top_length = 90
bp_iris.base_length = 100
bp_iris.base_offset = 35
bp_iris.base_height = 10
bp_iris.uneven_plane_seed = 'left'
bp_iris.uneven_peak_count = (5,6)
bp_iris.uneven_segments = 10
bp_iris.uneven_spacer = 2.25
bp_iris.uneven_step = .5
bp_iris.truchet_tolerance = 0.05
bp_iris.truchet_seed = 'retro'
bp_iris.debug_plane = False
bp_iris.make()

iris = bp_iris.build()

#show_object(iris)
cq.exporters.export(iris,'stl/portal_energy_insert.stl')