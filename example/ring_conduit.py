import cadquery as cq
from cqindustry import RingConduit

bp_ring = RingConduit()
bp_ring.cut_diameter = 76
bp_ring.diameter = bp_ring.cut_diameter + 10
bp_ring.inset = 5
bp_ring.height = 10
bp_ring.render_ladders = True
bp_ring.ladder_height = 71
bp_ring.ladder_length = 25
bp_ring.ladder_width = 10

bp_ring.frame = 1
bp_ring.frame_depth = 3
bp_ring.pipe_count = None
bp_ring.pipe_radius = 4
bp_ring.pipe_inner_radius = 2
bp_ring.segment_length = 6
bp_ring.space = 4
bp_ring.pipe_padding = 1

bp_ring.make()
ring = bp_ring.build()

#show_object(ring)
cq.exporters.export(ring, 'stl/ring_conduit.stl')