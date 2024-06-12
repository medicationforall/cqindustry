import cadquery as cq
from cadqueryhelper import Base

def make_platform_rails(
        bp_platform, 
        bp_guard_rail, 
        length_spacing, 
        width_spacing
    ):
    # guard rail length ways
    bp_guard_rail.length = bp_platform.length - bp_platform.corner_chamfer*2
    bp_guard_rail.clamp_spacing = length_spacing
    bp_guard_rail.make(bp_platform)
    rail_length = bp_guard_rail.build()
    rail_length_y_translate = bp_platform.width/2 - bp_guard_rail.width/2
    
    # guard rail width ways
    bp_guard_rail.length = bp_platform.width - bp_platform.corner_chamfer*2
    bp_guard_rail.clamp_spacing = width_spacing
    bp_guard_rail.make(bp_platform)
    
    rail_width = bp_guard_rail.build().rotate((0,0,1),(0,0,0),90)
    rail_width_x_translate = bp_platform.length/2 - bp_guard_rail.width/2
    
    z_translate = bp_platform.height/2 + bp_guard_rail.height/2
    rails = (
        cq.Workplane("XY")
        # minus y rail
        .union(rail_length.translate((
            0,
            -1*rail_length_y_translate,
            z_translate
        )))
        # plus y rail
        .union(rail_length.rotate((0,0,1),(0,0,0),180).translate((
            0,
            rail_length_y_translate,
            z_translate
        )))
        # plus x rail
        .union(rail_width.rotate((0,0,1),(0,0,0),180).translate((
            rail_width_x_translate,
            0,
            z_translate
        )))
        # minus x rail
        .union(rail_width.translate((
            -1*rail_width_x_translate,
            0,
            z_translate
        )))
    )
    
    return rails, rail_length, rail_width