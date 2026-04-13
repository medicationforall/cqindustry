import cadquery as cq
from cqindustry.can import StairSegment

bp_segment = StairSegment()

bp_segment.diameter = 73
bp_segment.diameter_margin = 0.5
bp_segment.height = 75 - 4

bp_segment.render_can = False
bp_segment.render_stairs = True
bp_segment.render_ladder = True
bp_segment.stair_count = 11
bp_segment.ramp_width = 64

bp_segment.platform_height = 4
bp_segment.platform_angle = 180

bp_segment.ring_rotate = -45
bp_segment.ring_padding = 10
bp_segment.ring_height = 10

#blueprints
#self.bp_can:Base|None = self.init_can()
#self.bp_ring:Base|None = self.init_ring()

bp_segment.make()

ex_segment = bp_segment.build()

#show_object(ex_segment)
cq.exporters.export(ex_segment, 'stl/can_stair_segment.stl')