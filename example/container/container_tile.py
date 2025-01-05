import cadquery as cq
from cqindustry.container import FloorTile, Container
from cqindustry.portal import RampGreebled
from cqterrain import tile as terrain_tile

#----------------------

def make_custom_tile(length, width, height):
    # https://github.com/medicationforall/cqterrain/blob/main/documentation/tile.md
    return terrain_tile.carton2(
        length, 
        width, 
        height,
        x_divisor = 2,
        y_divisor = 3.58
    )

bp_container = Container()
bp_container.render_ladder = False
#bp_container.bp_ladder.ladder_rungs = 6
#bp_container.bp_ladder.ladder_depth = 5
#bp_container.bp_ladder.ladder_rung_radius = 1.5

bp_container.bp_ramp = RampGreebled()
bp_container.bp_ramp.width = 8
bp_container.bp_ramp.segment_count = 10
bp_container.bp_ramp.segment_y_padding = 3

bp_container.bp_floor = FloorTile()

bp_container.bp_floor.height=2
bp_container.bp_floor.tile_length = 17
bp_container.bp_floor.tile_width = 17
bp_container.bp_floor.tile_padding = 0
bp_container.bp_floor.make_tile_method = make_custom_tile

bp_container.bp_hinge.rotate_deg = 0
bp_container.make()

result = bp_container.build()

#show_object(result)

cq.exporters.export(result, 'stl/container_tile.stl')