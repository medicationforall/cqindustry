import cadquery as cq
from cqindustry import Ring

bp = Ring()
bp.render_ladders = True
bp.make()
ring = bp.build()
#show_object(ring)
cq.exporters.export(ring, 'stl/ring.stl')
