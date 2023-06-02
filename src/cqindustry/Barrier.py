import cadquery as cq
import math
from . import Base

def jersey_shape(
    width = 10,
    height = 10,
    base_height = 2,
    middle_width_inset = -2,
    middle_height = 2,
    top_width_inset = -1
):
    mid_height = base_height + middle_height
    top_width = middle_width_inset + top_width_inset
    pts = [
        (0,0),
        (0,width),# base width
        (base_height,width),#base Height
        (mid_height, width + middle_width_inset), # middle

        (height,width + top_width),# top
        (height,-1*(top_width)),# top

        (mid_height, -1*(middle_width_inset)), # middle
        (base_height,0)
    ]

    result = (
        cq.Workplane("XY")
        .center(-1*(height/2),-1*(width/2))
        .polyline(pts)
        .close()
    )
    return result

def barrier_straight(
    j_shape,#non-optional
    length = 10
):
    j_barrier = (
        j_shape
        .extrude(length)
        .translate((0,0,-1*(length/2)))
        .rotate((0,1,0),(0,0,0),90)
    )
    return j_barrier

def barrier_curved(
    j_shape,
    x_radius = 75,
    y_radius = 75,#ellipse stretch
    angle = 270,
    rotation_angle=0
):
    path = (
        cq.Workplane("ZY")
        .ellipseArc(
            x_radius,
            y_radius,
            angle,
            rotation_angle=rotation_angle
        )
    )

    return (
        j_shape
        .toPending()
        .sweep(path)
        .rotate((0,1,0),(0,0,0),90)
        .translate((x_radius/2,-1*(y_radius/2),0))
    )

def barrier_diagonal(
    j_shape,
    x = 75,
    y = 37.5,
    axis = "ZY"
):
    path = cq.Workplane(axis).lineTo(x,y)
    result = j_shape.toPending().sweep(path)
    return result.rotate((0,1,0),(0,0,0),90)

def taper_barrier(
    straight_barrier,
    length = 75,
    width = 20,
    height = 20,
    rotation=-12.8,
    z_offset = 3,
    length_padding = 2,
    debug = False
):
    length_combined = length + length_padding
    taper_block = (
        cq.Workplane("XY")
        .box(length_combined, width, height)
        .translate((-1*(length_combined/2),0,(height/2)))
        .rotate((0,1,0),(0,0,0),rotation)
        .translate(((length/2),0,z_offset))

    )
    barrier_taper = (
        cq.Workplane("XY")
        .add(straight_barrier)
    )

    if debug:
        barrier_taper = barrier_taper.add(taper_block)
    else:
        barrier_taper = barrier_taper.cut(taper_block)

    return barrier_taper

def __extrude_faces(
        shape,
        extrude=10,
        faces=4,
        intersect=True
    ):
    poly = (
        shape
        .toPending()
        .extrude(extrude)
        .translate((0,0,-1*(extrude/2)))
    )

    mirror = (
        cq.Workplane("XY")
        .union(poly)
        .union(poly.rotate((1,0,0),(0,0,0),180))
    )

    rotate_degrees = math.floor(360 / faces)
    rotations = int(faces/2)

    scene = (
        cq.Workplane("XY")
        .union(mirror)
    )
    for i in range(rotations):
        if i == 0:
            scene = scene.union(mirror)
        else:
            if intersect:
                scene = scene.intersect(mirror.rotate((1,0,0),(0,0,0),rotate_degrees*i))
            else:
                scene = scene.union(mirror.rotate((1,0,0),(0,0,0),rotate_degrees*i))

    return scene.rotate((0,1,0),(0,0,0),90)

def barrier_cross(j_shape, extrude=20, faces=4, intersect=False):
    corner = __extrude_faces(
        j_shape,
        extrude=extrude,
        faces=faces,
        intersect=intersect
    )

    return corner
