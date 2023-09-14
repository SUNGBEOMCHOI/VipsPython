# -*- coding: utf-8 -*-
"""
Created on Sat Jun 02 20:45:02 2018

@author: Hard-
"""
import time

from PIL import Image, ImageDraw, ImageFont
import io

class ImageOut:
       
    def outImg(self, browser, url, screenshot_path="screenshot.png", save = True):
        # print('-----------------------------Getting Screenshot------------------------------------')
        default_width=1920
        default_height=1080
        # 1. get dimensions
        # print('getting dimensions...')
        browser.set_window_size(default_width, default_height)
        browser.get(url)
        # print('loading...')  
        total_height = browser.execute_script("return document.body.parentNode.scrollHeight")
        #self.browser.quit()
    
        # 2. get screenshot
        # print('getting screenshot...')
        browser.set_window_size(default_width, total_height)
        browser.get(url)
        #time.sleep(3) 
        # browser.save_screenshot(screenshot_path+'.png')
        screenshot = browser.get_screenshot_as_png()
        img = Image.open(io.BytesIO(screenshot)).convert('RGB')
        if save:
            img.save(screenshot_path+'.png', 'JPEG')
        # print('done')
        return img
    
    def outBlock(self, block, fileName, i=0, orig_img = None, visualize = False):
        # img = Image.open(fileName+'.png')
        if orig_img is None:
            orig_img = Image.open(fileName+'.jpeg')
        width, height = orig_img.size

        img = None
        dr = None
        if visualize:
            img = orig_img.copy()
            dr = ImageDraw.Draw(img)

        for blockVo in block:
            if blockVo.isVisualBlock:    
                cor = (2 * blockVo.x, 2 * blockVo.y, 2 * (blockVo.x + blockVo.width), 2 * (blockVo.y + blockVo.height))   
                if visualize:        
                    ############### Rectangle ###################
                    line = (cor[0],cor[1],cor[0],cor[3])
                    dr.line(line, fill="red", width=1)
                    line = (cor[0],cor[1],cor[2],cor[1])
                    dr.line(line, fill="red", width=1)
                    line = (cor[0],cor[3],cor[2],cor[3])
                    dr.line(line, fill="red", width=1)
                    line = (cor[2],cor[1],cor[2],cor[3])
                    dr.line(line, fill="red", width=1)
                    ###############                ####################
                    font = ImageFont.load_default()
                    dr.text((2 * blockVo.x,2 * blockVo.y),blockVo.id,(255,0,0),font=font)
                    #if blockVo.boxs[0].tag != None and blockVo.boxs[0].text != None and not blockVo.boxs[0].text.isspace():
                flag = False
                for box in blockVo.boxs:
                    if box.nodeName == 'img':
                        flag = True
                        break
                if flag:
                    if 0 <= cor[0] < width and 0 <= cor[1] < height and 0 <= cor[2] < width and 0 <= cor[3] < height:
                        if cor[0] != cor[2] and cor[1] != cor[3]:
                            cropimg = orig_img.crop(cor)
                            cropimg = cropimg.convert('RGB')
                            cropimg.save(fileName + '_img_' + blockVo.id + '.jpeg')
                        # else:
                            # print(blockVo.id, 'has not saved')
                    # else:
                        # print(blockVo.id, 'has not saved')

        if visualize:
            saved_path = fileName + '_Block_' + str(i) + '.png'
            img.save(saved_path)
    
    def outSeparator(self, List, fileName, direction, i=0):
        print(i)
        if (direction == '_vertica_'):
            img = Image.open(fileName + '_Block_' + str(i) + '.png')
        elif (direction == '_horizontal_'):
            img = Image.open(fileName + '_vertica_' + str(i) + '.png')
        dr = ImageDraw.Draw(img)
        for sep in List:             
            ################ Rectangle ###################
            dr.rectangle(((sep.x,sep.y),(sep.x + sep.width, sep.y + sep.height)),fill = "blue")
            """
            cor = (sep.x,sep.y, sep.x + sep.width, sep.y + sep.height)
            line = (cor[0],cor[1],cor[0],cor[3])
            dr.line(line, fill="blue", width=1)
            line = (cor[0],cor[1],cor[2],cor[1])
            dr.line(line, fill="blue", width=1)
            line = (cor[0],cor[3],cor[2],cor[3])
            dr.line(line, fill="blue", width=1)
            line = (cor[2],cor[1],cor[2],cor[3])
            dr.line(line, fill="blue", width=1)
            """
            ###############                ####################
        saved_path = fileName + direction + str(i) + '.png'
        img.save(saved_path)
    
    @staticmethod
    def outText(fileName, blockList, i=0):     
        f = open(fileName+'_text_output_'+str(i)+'.txt','a', encoding= 'utf-8')  
        for blockVo in blockList:
            write_line = ''
            text_content = ""
            for box in blockVo.boxs:
                writable = False              
                if box.nodeType == 3:
                    if box.parentNode.nodeName != "script" and box.parentNode.nodeName != "noscript" and box.parentNode.nodeName != "style":
                        if not box.nodeValue.isspace() or box.nodeValue == None:
                            text_content += str(box.nodeValue+'\n')
                            writable = True
            write_line += text_content                   
            if(writable):
                try:
                    f.write(write_line)
                except UnicodeEncodeError:
                    f.write(str(write_line.encode("utf-8").decode('utf-8')))
                    # print(blockVo.id)
        f.close()
