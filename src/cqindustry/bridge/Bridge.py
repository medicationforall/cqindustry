from cqterrain.bridge import Bridge as cqterrainBridge
from . import Straight

class Bridge(cqterrainBridge):
    def __init__(self):
        super().__init__()
        self.bp_straight:Straight = Straight()
        
    def make(self, parent=None):
        super().make(parent)
        
    def build(self):
        return super().build()