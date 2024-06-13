import cadquery as cq
from cadqueryhelper import Base

class ChipCan(Base):
    def __init__(self):
        super().__init__()
        
        # parameters
        self.height:float = 75 * 3
        self.radius:float = 75 / 2
        
        #shape
        self.can_cylinder:cq.Workplane|None = None
        
    def _make_can(self):
        can = (
            cq.Workplane("XY")
            .cylinder(self.height, self.radius)
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