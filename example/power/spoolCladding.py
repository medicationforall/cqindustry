import cadquery as cq
from cqterrain.spool import Spool
from cqindustry.power import SpoolCladding

# --- Spool
bp_spool = Spool()
bp_spool.height = 60
bp_spool.radius = 97.5
bp_spool.wall_width =4
bp_spool.cut_radius = 36.5
bp_spool.make()
ex_spool = bp_spool.build()

# --- Claddding
bp_cladding = SpoolCladding()
bp_cladding.make(bp_spool)
cladding = bp_cladding.build()

scene = (
    cq.Workplane("XY")
    .add(ex_spool)
    .add(cladding)
)

#show_object(scene)

cq.exporters.export(scene,"stl/power_spool_cladding.stl")