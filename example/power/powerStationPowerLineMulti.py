import cadquery as cq
from cqterrain.walkway import Walkway
from cqterrain.spool import Spool
from cqterrain.pipe import straight as power_line_straight
from cqindustry.power import ( 
    Cradle, 
    PowerStation,
    SpoolCladdingGreebledUnique
)

bp_spool = Spool()
bp_spool.height = 60
bp_spool.radius = 97.5
bp_spool.wall_width =4
bp_spool.cut_radius = 36.5
bp_spool.make()
ex_spool = bp_spool.build()

bp_cradle = Cradle()
bp_cradle.height = bp_spool.radius - bp_spool.cut_radius+2
bp_cradle.angle = 45
bp_cradle.make(parent = bp_spool)
ex_cradle = bp_cradle.build().translate((0,0,bp_cradle.height/2))

power_line =(
    power_line_straight()
    .rotate((0,0,1),(0,0,0),90)
    .translate((0,75,0))
)

bp_power = PowerStation()
bp_power.bp_cladding = SpoolCladdingGreebledUnique()
bp_power.bp_cladding.seed="uniquePanels"
bp_power.render_control = False
bp_power.render_walkway = False
bp_power.make()
ex_power = bp_power.build()

bp_power.render_stairs = False
bp_power.render_control = True
bp_power.bp_cladding.seed="uniquePanels2"
bp_power.make()
ex_power2 = bp_power.build()

bp_walkway = Walkway()
bp_walkway.length = 150 + 75
bp_walkway.make()
ex_walkway = bp_walkway.build()

combined = (
    cq.Workplane("XY")
    .add(ex_power)
    .add(ex_power2.translate((0,150,0)))
    .add(power_line.translate((75/2,0,0)))
    .add(power_line.translate((-1*(75/2),0,0)))
    .add(power_line.translate((75/2,150,0)))
    .add(power_line.translate((-1*(75/2),150,0)))
    .add(ex_walkway.rotate((0,0,1),(0,0,0),90).translate((0,75,75)))
)

#show_object(combined)
cq.exporters.export(combined,"stl/power_station_combined.stl")