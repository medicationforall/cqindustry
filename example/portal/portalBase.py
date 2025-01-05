import cadquery as cq
from cqindustry.portal import PortalBase

bp_portal_base = PortalBase()
bp_portal_base.length = 150
bp_portal_base.width = 75
bp_portal_base.height = 10

bp_portal_base.make()
result = bp_portal_base.build()

#show_object(result)
cq.exporters.export(result, 'stl/portal_base.stl')