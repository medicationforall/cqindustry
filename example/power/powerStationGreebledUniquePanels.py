import cadquery as cq
from cqindustry.power import PowerStation, SpoolCladdingGreebledUnique

bp_power = PowerStation()
bp_power.bp_stairs.overlook_tile_size = 10
bp_power.bp_stairs.bp_stairs.stair_chamfer = None


bp_power.bp_cladding = SpoolCladdingGreebledUnique()
bp_power.bp_cladding.seed="uniquePanels"

bp_power.render_spool = True
bp_power.render_cladding = True
bp_power.render_cradle = True
bp_power.render_stairs = True
bp_power.render_control = True
bp_power.render_walkway = True
bp_power.render_ladder = True

bp_power.make()
power = bp_power.build()
platform = bp_power.bp_control.build()

#show_object(power)
cq.exporters.export(platform,f"stl/power_controlPlatform.stl")
cq.exporters.export(power,f"stl/power_powerStation_seed_{bp_power.bp_cladding.seed}.stl")