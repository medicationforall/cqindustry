import cadquery as cq
from cqindustry.power import PowerStation

bp_power = PowerStation()

bp_power.make()
power = bp_power.build()
#show_object(power)
cq.exporters.export(power,f"stl/power_powerStation.stl")