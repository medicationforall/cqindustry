import cadquery as cq
from cqindustry.chip import Ring

bp_ring = Ring()
bp_ring.cut_diameter = 76
bp_ring.diameter = bp_ring.cut_diameter + 10
bp_ring.inset = 5
bp_ring.height = 10
bp_ring.render_ladders = True
bp_ring.ladder_height = 71
bp_ring.ladder_length = 25
bp_ring.ladder_width = 10
bp_ring.ladder_cut_padding = 1.5
bp_ring.ladder_cut_chamfer = 2
bp_ring.make()
ring = bp_ring.build()

#show_object(ring)
cq.exporters.export(ring, 'stl/ring.stl')
