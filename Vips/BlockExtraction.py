# -*- coding: utf-8 -*-
"""
Created on Tue May 29 12:37:05 2018

@author: Hard-
"""
import sys
from . import BlockVo
from . import BlockRule

class BlockExtraction:
    all_text_nodes = []
    max_dist = 7
    max_dist_gap = 4

    def __init__(self):
        self.html = None
        self.hrList = []
        self.cssBoxList = dict()
        self.count = 0
        self.count1 = 0
        self.count2 = 0
        self.count3 = 1
        self.block = BlockVo.BlockVo()
        self.blockList = []
                
    def service(self, url, nodeList):
        BlockRule.BlockRule.initialize(nodeList)
        body = nodeList[0]
        self.initBlock(body, self.block)  
        # print("-----Done Initialization-----")
        self.count3 = 0
        self.dividBlock(self.block)
        # print(self.count2)       
        # print("-----Done Division-----")
        BlockVo.BlockVo.refreshBlock(self.block)
        # print("-----Done Refreshing-----")
        self.filList(self.block)
        # print("-----Done Filling-----")
        self.groupBlock()
        #self.checkText()
        return self.block
        
    def initBlock(self, box, block):
        block.boxs.append(box)
        # print(self.count,"####Here Name=",box.nodeName)
        self.count+=1
            
        if(box.nodeName == "hr"):
            self.hrList.append(block)
            self.count1 = 0
        if box.nodeType != 3:
            subBoxList = box.childNodes
            for b in subBoxList:
                try:
                    if b.nodeName != "script" and b.nodeName != "noscript" and b.nodeName != "style":
                        #print(self.count1," : ",b.nodeName,", ",box.nodeName)
                        self.count1+=1
                        bVo = BlockVo.BlockVo()
                        bVo.parent = block
                        block.children.append(bVo)
                        self.initBlock(b, bVo)       
                except AttributeError:
                    print(b,",",b.nodeType)
                    sys.exit(0)
            
    def dividBlock(self, block):
        self.count2+=1
        # print (self.count2)
        if(block.isDividable and BlockRule.BlockRule.dividable(block)):
            block.isVisualBlock = False         
            for b in block.children:
                self.count3+=1
                # print(self.count3)
                self.dividBlock(b)
                        
    def filList(self, block):
        if block.isVisualBlock:
            self.blockList.append(block)
        else:
            for blockVo in block.children:
                self.filList(blockVo)
    
    def groupBlock(self):
        group = []
        grouped_texts = []
        grouped_text = ''
        for block in self.blockList:
            text_content = ''
            for box in block.boxs:
                writable = False              
                if box.nodeType == 3:
                    if box.parentNode.nodeName != "script" and box.parentNode.nodeName != "noscript" and box.parentNode.nodeName != "style":
                        if not box.nodeValue.isspace() or box.nodeValue == None:
                            text_content += str(box.nodeValue+'\n')
                            writable = True
            if writable:
                # cmp prev block & cur block
                if BlockExtraction.is_included(group, block):
                    group.append(block)
                    grouped_text += text_content
                else:
                    group = [block]
                    grouped_texts.append(grouped_text)
                    grouped_text = text_content
        if group:
            grouped_texts.append(grouped_text)
        self.grouped_texts = grouped_texts
        # for t in grouped_texts:
        #     print(t)

    def checkText(self):
        for blockVo in self.blockList:
            removed = True
            for box in blockVo.boxs:
                if box.nodeType == 3:
                    if box.parentNode.nodeName != "script" and box.parentNode.nodeName != "noscript" and box.parentNode.nodeName != "style":
                         if not box.nodeValue.isspace() or box.nodeValue == None:
                             removed = False
            if(removed):
                self.blockList.remove(blockVo)

    @staticmethod
    def is_included(group, current_block):
        if not group:
            return True
        elif len(group) == 1:
            # 1, 공유하는 parent 확인하기
            # 2, group의 블럭과 current block 각각의 parent 까지의 거리가 너무 멀거나 거리의 차이가 너무 크면 서로 관계없는 노드로 판단
            group_block = group[0].parent
            parents = []
            dist = 1
            while dist < BlockExtraction.max_dist and group_block is not None:
                parents.append(group_block)
                group_block = group_block.parent
                dist += 1
            cur_block = current_block.parent
            dist = 1
            while dist < BlockExtraction.max_dist and cur_block is not None:
                for idx, parent in enumerate(parents):
                    if cur_block.id == parent.id:
                        if dist < BlockExtraction.max_dist and -BlockExtraction.max_dist_gap < dist - (idx + 1) < BlockExtraction.max_dist_gap:
                            return True
                        return False
                dist += 1
                cur_block = cur_block.parent
            return False
        else:
            # 1, group 안에서 공유하는 parent 확인하기
            # 2, group + current_block까지 고려했을 때 공유하는 parent가 달라지는지 확인하기 -> 다르다면 관계없는 노드로 판단
            # 3, current block으로부터 parent 까지의 거리가 너무 멀거나 그 거리가 기존과 너무 크면 서로 관계없는 노드로 판단
            group_block = group[-2].parent

            parents = []
            dist = 1
            while dist < BlockExtraction.max_dist and group_block is not None:
                parents.append(group_block)
                group_block = group_block.parent
            cur_block = group[-1].parent
            dist1 = 1
            dist0 = None
            par = None
            while dist1 < BlockExtraction.max_dist and cur_block is not None and par is None:
                for idx, parent in enumerate(parents):
                    if cur_block.id == parent.id:
                        par = cur_block
                        dist0 = idx + 1
                        break
                dist1 += 1
                cur_block = cur_block.parent
            
            dist = 1
            new_block = current_block.parent
            while dist < BlockExtraction.max_dist and new_block is not None:
                for idx, parent in enumerate(parents):
                    if new_block.id == parent.id:
                        if dist < BlockExtraction.max_dist and (-BlockExtraction.max_dist_gap < dist - dist1 < BlockExtraction.max_dist_gap or -BlockExtraction.max_dist_gap < dist - dist0 < BlockExtraction.max_dist_gap):
                            return True
                        return False
                dist += 1
                new_block = new_block.parent
            return False
        