import cadquery as cq
from cadqueryhelper import Base

class ChipCan(Base):
    def __init__(self):
        super().__init__()
        
        # parameters
        self.height:float = 75 * 3
        self.diameter:float = 75
        
        #shape
        self.can_cylinder:cq.Workplane|None = None
        
    def _make_can(self):
        radius = self.diameter / 2
        can = (
            cq.Workplane("XY")
            .cylinder(self.height, radius)
        )
        
        self.can_cylinder = can
        
    def make(self, parent = None):
        super().make(parent)
        self._make_can()
        
    def build(self) -> cq.Workplane:
        super().build()
        scene = cq.Workplane()

        if self.can_cylinder:
            scene = scene.union(self.can_cylinder)
        return scene