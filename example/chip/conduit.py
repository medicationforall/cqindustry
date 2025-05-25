import cadquery as cq
from cqindustry.chip import Conduit

bp_conduit = Conduit()
bp_conduit.frame = 1
bp_conduit.frame_depth = 3
bp_conduit.pipe_count = 2
bp_conduit.pipe_radius = 4
bp_conduit.pipe_inner_radius = 2
bp_conduit.segment_length = 6
bp_conduit.space = 4
bp_conduit.pipe_padding = 1
bp_conduit.make()
ex_conduit = bp_conduit.build()

#show_object(ex_conduit)
cq.exporters.export(ex_conduit,'stl/chip_conduit_class.stl')