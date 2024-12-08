import cadquery as cq
from cqterrain.spool import Spool
from cqindustry.power import Cradle


bp_spool = Spool()
#bp.height = 100
#bp.radius = 100
#bp.wall_width = 3
#bp.cut_radius = 40
#bp.internal_wall_width = 4
#bp.internal_z_translate = -3
bp_spool.make()
spool_ex = (
      bp_spool.build()
      .rotate((1,0,0),(0,0,0),90)
      .translate((0,0,bp_spool.radius))
)

bp = Cradle()
bp.height = 70
bp.angle = 45
bp.make(bp_spool)
cradle_ex = bp.build().translate((0,0,bp.height/2))

#show_object(cradle_ex)
#show_object(spool_ex.translate((0,0,2)))
cq.exporters.export(cradle_ex,"stl/power_cradle_tall.stl")