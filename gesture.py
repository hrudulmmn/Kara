import cv2
import mediapipe as mp
import math 
import numpy as np
from PyQt6.QtCore import pyqtSignal,QObject,QThread
import time

class Smoother:
    def __init__(self,alpha=0.55):
        self.alpha=alpha
        self.smoothedland=None
    
    def smooth(self,landmarks):
        current=np.array(landmarks)

        if self.smoothedland is None:
            self.smoothedland=current
            return current
        
        self.smoothedland=(self.alpha*current + (1-self.alpha)*self.smoothedland)
        return self.smoothedland
    
    def reset(self):
        self.smoothedland=None

class GestureChecker:
    def __init__(self,min=75):
        self.minhold=min
        self.isactive={}
        self.activetime={}

    def trigger(self,gesturename,detected,time):
        if gesturename not in self.activetime:
            self.isactive[gesturename]=False
            self.activetime[gesturename]=None
        if detected:
            if self.activetime[gesturename] is None:
                self.activetime[gesturename]=time
                return False
            holdtime = time-self.activetime[gesturename]

            if holdtime>=self.minhold and not self.isactive[gesturename]:
                self.isactive[gesturename]=True
                return True
            return False
        else:
            self.isactive[gesturename]=False
            self.activetime[gesturename]=None
            return False

class Gesture(QObject):
    nextPage = pyqtSignal()
    prevPage = pyqtSignal()
    takt = pyqtSignal(bool)
    zoom = pyqtSignal(int)
    def __init__(self, parent =None):
        super().__init__(parent)
        self.hands = mp.solutions.hands
        self.draw = mp.solutions.drawing_utils
        self.running =True
        self.enabled = False
        self.active = False

        self.nextTime = 0.0
        self.prevTime = 0.0
        self.taktTime = 0.0
        self.cooldown = 350
        self.taktcooldown = 600
        self.lastpinch=0

        self.smoother = Smoother(alpha=0.55)
        self.checker = GestureChecker(min=75)

    def run(self):
        capture = cv2.VideoCapture(0)
        hand = self.hands.Hands(
                    static_image_mode = False,
                    max_num_hands = 1,
                    min_detection_confidence = 0.7,
                    min_tracking_confidence = 0.7
                )
        
        try:
            while self.running:
                ret,frame = capture.read()
                if not ret:
                    self.active = False
                    break

                self.time = time.time()*1000
                rgb = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)

                result = hand.process(rgb)
                if result.multi_hand_landmarks:
                    for landmarks in result.multi_hand_landmarks:
                        self.draw.draw_landmarks(
                            frame,
                            landmarks,
                            self.hands.HAND_CONNECTIONS
                        )
                        
                        norm = []
                        wristx = landmarks.landmark[0].x
                        wristy = landmarks.landmark[0].y
                        for point in landmarks.landmark:
                            
                            x = point.x - wristx
                            y = point.y - wristy
                            norm.append((x,y))
                        smoothedNorm = self.smoother.smooth(norm)

                        def fingUp(smoothedNorm,tip,pip):
                            return smoothedNorm[tip][1]<smoothedNorm[pip][1]
                        
                        thumb = fingUp(smoothedNorm,4,2)
                        index = fingUp(smoothedNorm,8,6)
                        middle = fingUp(smoothedNorm,12,10)
                        ring = fingUp(smoothedNorm,16,14)
                        smol = fingUp(smoothedNorm,20,18)

                        takt = middle and index and thumb and not ring and not smol and smoothedNorm[8][1]<-0.15

                        if(self.checker.trigger("takt",takt,self.time)):
                            if(self.time-self.taktTime>=self.taktcooldown and not self.enabled):
                                self.takt.emit(True)
                                self.taktTime = self.time
                                self.enabled = True
                            elif(self.time-self.taktTime>=self.taktcooldown and self.enabled):
                                self.takt.emit(False)
                                self.taktTime = self.time
                                self.enabled = False
                    
                        move=None
                        direction = middle and index and thumb and ring and smol
                        if(direction):
                            dx=smoothedNorm[12][0]
                            if dx<-0.22:
                                move="prev"
                            elif dx>0.22:
                                move="next"

                        if (move):
                            if(self.checker.trigger(move,True,self.time)):
                                if(move=="prev" and self.time-self.prevTime>=self.cooldown):
                                    self.prevPage.emit()
                                    self.prevTime = self.time
                        
                                if(move=="next" and self.time-self.nextTime>=self.cooldown):
                                    self.nextPage.emit()
                                    self.nextTime = self.time
                        else:
                            self.checker.trigger("prev",False,self.time)
                            self.checker.trigger("next",False,self.time)

                            #zoom
                        if(index and thumb and not middle and not ring and not smol):
                                a = smoothedNorm[4]
                                b = smoothedNorm[8]
                                
                                dist = math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)
                                threshold = 0.01

                                pinch = dist
                                if(pinch-self.lastpinch>threshold):
                                    self.zoom.emit(+1)
                                if(pinch-self.lastpinch<-threshold):
                                    self.zoom.emit(-1)
                                self.lastpinch = pinch
                else:
                    self.smoother.reset()

                cv2.imshow("Camera",frame)
                if cv2.waitKey(1) & 0xFF==ord('q'):
                    self.active==False
                    break
                

        finally:
            capture.release()
            cv2.destroyAllWindows()
            hand.close()

class GestureMan(QObject):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.thred = QThread()
        self.man = Gesture()
        self.man.moveToThread(self.thred)
        self.thred.started.connect(self.man.run)
        
    def start(self):
        self.thred.start()
        self.man.running = True
        self.man.active = True
    

    def stop(self):
        self.man.running=False
        self.man.active = False
        self.thred.quit()
        self.thred.wait()



