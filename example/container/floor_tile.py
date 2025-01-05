import cadquery as cq
from cqindustry.container import FloorTile

#-------------
# Custom tile method
def make_basic_tile(
    length:float, 
    width:float, 
    height:float
) -> cq.Workplane:
    tile = cq.Workplane("XY").box(
        length, 
        width, 
        height
    )
    return tile

#------------
# Floor Tile Instantiation
bp_floor_tile = FloorTile()

## Floor parameters
bp_floor_tile.length = 75
bp_floor_tile.width = 75
bp_floor_tile.height = 4

## FloorTile parameters
bp_floor_tile.tile_length = 10
bp_floor_tile.tile_width = 10
bp_floor_tile.tile_padding = 1
bp_floor_tile.make_tile_method = make_basic_tile
bp_floor_tile.make()

floor_ex = bp_floor_tile.build()

#show_object(floor_ex)
cq.exporters.export(floor_ex, 'stl/container_floor_tile.stl')