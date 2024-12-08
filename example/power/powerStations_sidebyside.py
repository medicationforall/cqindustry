import cadquery as cq
from cqindustry.power import PowerStation, SpoolCladdingGreebled, SpoolCladdingGreebledUnique 

bp_power = PowerStation()
bp_power.bp_cladding = SpoolCladdingGreebled()
bp_power.bp_cladding.seed="morePower!"
bp_power.make()
power = bp_power.build()


bp_power.bp_cladding.seed="test5"
bp_power.make()
power2 = bp_power.build()

bp_power.bp_cladding = SpoolCladdingGreebledUnique()
bp_power.bp_cladding.seed="uniquePanels"
bp_power.make()
power3 = bp_power.build()

# use cqeditor or equivalent that supports show_object
#show_object(power)
#show_object(power2.translate((0,250,0)))
#show_object(power3.translate((0,500,0)))

scene = (
    cq.Workplane("XY")
    .union(power)
    .union(power2.translate((0,250,0)))
    .union(power3.translate((0,500,0)))
)

cq.exporters.export(scene, 'stl/power_stations_side_by_side.stl')