import cv2
import mediapipe as mp
import mouse
import Volume as vol

class handDetector():
    def __init__(self, mode=False, maxHands=1, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands,
                                        self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms,
                                               self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, handNo=0, draw=True):
        lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])
                if id == 0:
                    cv2.circle(img, (cx, cy), 10, (28, 50, 132), cv2.FILLED)
        return lmList

def main():
    beg = 0
    start = True
    cap = cv2.VideoCapture(1)
    detector = handDetector()
    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lmList = detector.findPosition(img)
        if len(lmList) != 0:
            if start == True:
                if beg == 0:
                    currentX = lmList[0][1]
                    currentY = lmList[0][2]
                mouse.move((currentX - lmList[0][1])/2, (lmList[0][2] - currentY)/2, absolute = False, duration=0)
                if lmList[8][2] < lmList[6][2] and lmList[12][2] < lmList[10][2] and lmList[4][1] > lmList[2][1] and \
                        lmList[16][2] > lmList[14][2] and lmList[20][2] > lmList[18][2] and beg > 30:
                    w = 0
                    while w < 10:
                        w = w +1
                    vol.VolumeTrack(img, cap)
                    beg = 1
                elif lmList[8][2] > lmList[6][2] and lmList[12][2] > lmList[10][2] and lmList[4][1] > lmList[2][1] and \
                        lmList[16][2] > lmList[14][2] and lmList[20][2] > lmList[18][2] and beg > 30:
                    mouse.click('left')
                    beg = 1
                elif lmList[8][2] < lmList[6][2] and lmList[12][2] > lmList[10][2] and lmList[4][1] < lmList[2][1] and \
                        lmList[16][2] > lmList[14][2] and lmList[20][2] < lmList[18][2] and beg > 30:
                    start = False
                    beg = 1
            elif start == False and beg > 30:
                if lmList[8][2] < lmList[6][2] and lmList[12][2] > lmList[10][2] and lmList[4][1] < lmList[2][1] and \
                        lmList[16][2] > lmList[14][2] and lmList[20][2] < lmList[18][2] and beg > 30:
                    start = True
                    beg = 1
            beg = beg + 1
        cv2.imshow("Image", img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()