# -*- coding: utf-8 -*-
"""
Created on Tue May 29 12:45:17 2018

@author: Hard-
"""
class BlockVo:
    count = 1

    def __init__(self):
        self.id = str(BlockVo.count)
        BlockVo.count += 1
        #str(uuid.uuid4())
        self.boxs = []
        self.children = []
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0
        self.parent = None
        self.isVisualBlock = True
        self.isDividable = True
        self.Doc = 0
    
    def refresh(self):
        for i in range(0, len(self.boxs)):
            box = self.boxs[i]
            #print (box.get_attribute("id"),",",box.tag_name,",",box.location)
            if i == 0:
                self.x = box.visual_cues['bounds']['x']
                self.y = box.visual_cues['bounds']['y']
                self.width = box.visual_cues['bounds']['width']
                self.height = box.visual_cues['bounds']['height']
            else:
                RBX = self.x + self.width
                RBY = self.y + self.height
                boxRBX = box.visual_cues['bounds']['x']+box.visual_cues['bounds']['width']
                boxRBY = box.visual_cues['bounds']['y']+box.visual_cues['bounds']['height']
                RBX = boxRBX if (boxRBX > RBX) else RBX
                RBY = boxRBY if (boxRBY > RBY) else RBY
                self.x = box.visual_cues['bounds']['x'] if (box.visual_cues['bounds']['x']<self.x) else self.x
                self.y = box.visual_cues['bounds']['y'] if (box.visual_cues['bounds']['y'] <self.y) else self.y
                self.width = RBX - self.x
                self.height = RBY - self.y

    @staticmethod  
    def refreshBlock(block):
        block.refresh()
        for blockVo in block.children:
            BlockVo.refreshBlock(blockVo)
    
    