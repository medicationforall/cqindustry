import cadquery as cq
import math

from cqindustry import (
    jersey_shape,
    barrier_straight,
    barrier_cross,
    barrier_curved,
    barrier_diagonal,
    taper_barrier,
    cut_forklift
)

def cut_forklift2(
        barrier,
        length = 75,
        fork_length=5,
        width=20,
        fork_height = 2
):
    fork_cut = (
        cq.Workplane("XY")
        .box(fork_length, width, fork_height)
        .translate((0,0,fork_height/2))
    )
    result = (
        cq.Workplane("XY")
        .add(barrier)
        .add(fork_cut.translate((length/4,0,0)))
        .add(fork_cut.translate((-1*(length/4),0,0)))
    )
    return result

barrier_height = 20
barrier_width = 20

j_shape = jersey_shape(
    width = barrier_width,
    height = barrier_height,
    base_height = 4,
    middle_width_inset = -5,
    middle_height = 4,
    top_width_inset = -1
)

barrier = barrier_straight(
    j_shape = j_shape,
    length = 75
).translate((0,0,barrier_height/2))

barrier_forks = cut_forklift(barrier)

barrier_curve_60 = (
    barrier_curved(
        j_shape,
        x_radius = 75,
        y_radius = 75,#ellipse stretch
        angle = 300,
        rotation_angle=-30
    )
    .translate((0,0,barrier_height/2))
    .rotate((0,0,1),(0,0,0),-30)
    .translate((-1*(13.5),0,0))
)

barrier_curve_60_forks = cut_forklift(
    barrier_curve_60,
    width = 80
)

barrier_taper = taper_barrier(
    barrier,
    length = 75,
    debug = False
)

barrier_taper_forks = cut_forklift(barrier_taper)

barrier_diag_right = (
    barrier_diagonal(
        j_shape,
        x = 75,
        y = 37.5,
        axis = "ZY"
    ).translate(((75/2),-1*(37.5/2),barrier_height/2))
    .rotate((0,0,1),(0,0,0),-1*(53/2))
)

barrier_diag_right_forks = cut_forklift(
    barrier_diag_right
)

barrier_diag_left = (
    barrier_diagonal(
        j_shape,
        x = -75,
        y = 37.5,
        axis = "ZY"
    ).translate((-1*(75/2),-1*(37.5/2),barrier_height/2))
    .rotate((0,0,1),(0,0,0),(53/2))
)

barrier_diag_left_forks = cut_forklift(
    barrier_diag_left
)

barrier_c = barrier_cross(j_shape).translate((0,0,barrier_height/2))

scene = (
    cq.Workplane("XY")
    .add(barrier_forks)
    .add(barrier_curve_60_forks.translate((0,-8,0)))
    .add(barrier_taper_forks.translate((0,25,0)))
    .add(barrier_diag_right_forks.translate((0,47,0)))
    .add(barrier_diag_left_forks.translate((0,67,0)))
    .add(barrier_c.translate((0,-55,0)))
)

show_object(scene)

# Print These
#cq.exporters.export(barrier, 'stl/barrier.stl')
#cq.exporters.export(barrier_taper, 'stl/barrier_taper.stl')
#cq.exporters.export(barrier_c, 'stl/barrier_c.stl')
#cq.exporters.export(barrier_curve_60, 'stl/barrier_curve_60.stl')
#cq.exporters.export(barrier_diag_right, 'stl/barrier_diag_right.stl')
#cq.exporters.export(barrier_diag_left, 'stl/barrier_diag_left.stl')

## legacy
##cq.exporters.export(barrier_curve_45, 'stl/barrier_curve_45.stl')
##cq.exporters.export(barrier_curve_90, 'stl/barrier_curve_90.stl')

##cq.exporters.export(barrier_diag_right_short, 'stl/barrier_diag_right_short.stl')
##cq.exporters.export(barrier_diag_left_short, 'stl/barrier_diag_left_short.stl')
