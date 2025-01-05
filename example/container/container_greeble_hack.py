import cadquery as cq
from cqindustry.container import FloorTile, Container
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
bp_container.render_ladder = True
#bp_container.bp_ladder.ladder_rungs = 6
#bp_container.bp_ladder.ladder_depth = 5
#bp_container.bp_ladder.ladder_rung_radius = 1.5

bp_container.bp_floor = FloorTile()

bp_container.bp_floor.height=2
bp_container.bp_floor.tile_length = 17
bp_container.bp_floor.tile_width = 17
bp_container.bp_floor.tile_padding = 0
bp_container.bp_floor.make_tile_method = make_custom_tile

bp_container.bp_hinge.rotate_deg = -70
bp_container.make()

result = bp_container.build()

#show_object(result)

#----------------------

conduit = terrain_tile.conduit(length=35)

apricorn = terrain_tile.apricorn(
    length = 35, 
    width = 25, 
    height = 4,
    line_width = 2,
    line_depth = .5,
    center_radius = None,
    width_radius_divisor = 4
)

carton = terrain_tile.carton2(
    length = 35, 
    width = 25, 
    height = 4, 
    line_width = 2, 
    line_depth = 1.5,
    x_divisor = 2,
    y_divisor = 3
)

carton_other = terrain_tile.carton(
    length=35, 
    width=25, 
    height = 4,
    line_width = 3,
    line_depth = 1.5,
    x_divisor = 3,
    y_divisor = 2
)

bolt_panel = terrain_tile.bolt_panel(
    length = 35, 
    width = 25, 
    height = 4, 
    chamfer = .5, 
    radius_outer=1,
    radius_internal=0.5,
    cut_height=0.5,
    padding = 2
)

charge = terrain_tile.charge(
    length = 35, 
    width = 25, 
    height = 4,
    line_width = 3,
    line_depth = 1,
    corner_chamfer = 4,
    edge_chamfer = 2,
    padding = 2.5
)

cut_box= cq.Workplane("XY").box(35,25,4)

#center
conduits = (
    cq.Workplane("XY")
    .add(result)
    #top
    .cut(
        cut_box
        .rotate((0,1,0),(0,0,0), 71.5)
        .translate((-27.5,0,16))
    )
    .add(
        conduit
        .rotate((0,1,0),(0,0,0), 71.5)
        .translate((-27.5,0,16))
    )
    #bottom
    .cut(
        cut_box
        .rotate((0,1,0),(0,0,0), 110)
        .translate((-27.5,0,-20))
    )
    .add(
        bolt_panel
        .rotate((0,1,0),(0,0,0), 110)
        .translate((-27.5,0,-20))
    )
)

#right
conduits = (
    conduits
    #top
    .cut(
        cut_box
        .rotate((0,1,0),(0,0,0), 71.5)
        .translate((-27.5,-56,16))
    )
    .add(
        charge
        .rotate((0,1,0),(0,0,0), 71.5)
        .translate((-27.5,-56,16))
    )
    #bottom
    .cut(
        cut_box
        .rotate((0,1,0),(0,0,0), 110)
        .translate((-27.5,-56,-20))
    )
    .add(
        bolt_panel
        .rotate((0,1,0),(0,0,0), 110)
        .translate((-27.5,-56,-20))
    )
    
)

#left
conduits = (
    conduits
    #top
    .cut(
        cut_box
        .rotate((0,1,0),(0,0,0), 71.5)
        .translate((-27.5,56,16))
    )
    .add(
        charge
        .rotate((0,1,0),(0,0,0), 71.5)
        .translate((-27.5,56,16))
    )
    #bottom
    .cut(
        cut_box
        .rotate((0,1,0),(0,0,0), 110)
        .translate((-27.5,56,-20))
    )
    .add(
        bolt_panel
        .rotate((0,1,0),(0,0,0), 110)
        .translate((-27.5,56,-20))
    )
)
    
#flip
#left
conduits = (
    conduits
    #top
    .cut(
        cut_box
        .rotate((0,1,0),(0,0,0), 71.5)
        .translate((-27.5,56,16))
        .rotate((0,0,1),(0,0,0), 180)
    )
    .add(
        charge
        .rotate((0,1,0),(0,0,0), 71.5)
        .translate((-27.5,56,16))
        .rotate((0,0,1),(0,0,0), 180)
    )
    #bottom
    .cut(
        cut_box
        .rotate((0,1,0),(0,0,0), 110)
        .translate((-27.5,56,-20))
        .rotate((0,0,1),(0,0,0), 180)
    )
    .add(
        bolt_panel
        .rotate((0,1,0),(0,0,0), 110)
        .translate((-27.5,56,-20))
        .rotate((0,0,1),(0,0,0), 180)
    )
)

#right
conduits = (
    conduits
    #top
    .cut(
        cut_box
        .rotate((0,1,0),(0,0,0), 71.5)
        .translate((-27.5,-56,16))
        .rotate((0,0,1),(0,0,0), 180)
    )
    .add(
        charge
        .rotate((0,1,0),(0,0,0), 71.5)
        .translate((-27.5,-56,16))
        .rotate((0,0,1),(0,0,0), 180)
    )
    #bottom
    .cut(
        cut_box
        .rotate((0,1,0),(0,0,0), 110)
        .translate((-27.5,-56,-20))
        .rotate((0,0,1),(0,0,0), 180)
    )
    .add(
        bolt_panel
        .rotate((0,1,0),(0,0,0), 110)
        .translate((-27.5,-56,-20))
        .rotate((0,0,1),(0,0,0), 180)
    )
    
)

#show_object(conduits.rotate((0,0,1),(0,0,0),270))
cq.exporters.export(conduits, 'stl/container_greebled.stl')