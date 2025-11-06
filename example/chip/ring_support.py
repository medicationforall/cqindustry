import cadquery as cq
from cqindustry.chip import RingSupport

bp_ring = RingSupport()
bp_ring.make()
ring = bp_ring.build()

#show_object(ring)
cq.exporters.export(ring, 'stl/ring_support.stl')