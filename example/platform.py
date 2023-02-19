import cadquery as cq
from cqindustry import Platform

bp = Platform()
bp.length = 150
bp.stripe_width = 5
#bp.width = 80
bp.height = 4
bp.render_stripes = True
bp.stripe_padding = .3
bp.make()
platform = bp.build()

#show_object(platform)
cq.exporters.export(platform,'./stl/platform.stl')


bp = Platform()
bp.length = 150
bp.stripe_width = 5
bp.corner_chamfer = 30
#bp.width = 80
bp.height = 4
bp.bar_width = 10
bp.render_stripes = True
bp.stripe_padding = .3
bp.make()
platform = bp.build()

cq.exporters.export(platform,'./stl/platform_alt.stl')
