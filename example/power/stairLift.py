import cadquery as cq
from cqindustry.power import StairLift
from cadqueryhelper import wave

bp_stairs = StairLift()
bp_stairs.length = 150
bp_stairs.width = 75
bp_stairs.height = 75

bp_stairs.overlook_tile_size = 10
bp_stairs.walkway_tile_size = 27
bp_stairs.tile_height = 2

bp_stairs.face_cut_width = 4
bp_stairs.face_cut_padding = 3
bp_stairs.wave_function = wave.square #wave.triangle wave.sine
bp_stairs.wave_segment_length = 5

bp_stairs.bp_stairs.render_hollow = False
bp_stairs.make()
stairs = bp_stairs.build()
#show_object(stairs)
cq.exporters.export(stairs,"stl/power_stair_lift.stl")