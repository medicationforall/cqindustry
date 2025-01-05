import cadquery as cq
from cqindustry.container import Floor

floor_bp = Floor()
floor_bp.length = 75
floor_bp.width = 75
floor_bp.height = 4

floor_bp.make()
floor_ex = floor_bp.build()

#show_object(floor_ex)
cq.exporters.export(floor_ex, 'stl/container_floor.stl')