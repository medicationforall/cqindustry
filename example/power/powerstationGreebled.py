import cadquery as cq
from cqindustry.power import PowerStation, SpoolCladdingGreebled

bp_power = PowerStation()
bp_power.bp_cladding = SpoolCladdingGreebled()
bp_power.bp_cladding.seed="morePower!"
bp_power.make()
power = bp_power.build()
#show_object(power)
cq.exporters.export(power,f"stl/power_powerStation_seed_{bp_power.bp_cladding.seed}.stl")