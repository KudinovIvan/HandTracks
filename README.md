# HandTracks
# MediaPipe
To achieve this goal, namely, hand gesture recognition for human-machine interaction, it is necessary to connect a webcam to a computer. The program should allow the user to" control " the computer only through a webcam.
First, we create an instance of the Video Capture class.
```python
  cap = cv2.VideoCapture(1)
```
We run an infinite while loop to test the program.
```python
  while True:
```
Next, we capture the video from the connected webcam. If no frames were captured (the camera is disabled), the method returns false, and the function returns an empty image.
```python
  success, img = cap. read()
```
Putting the captured video in the window.
```python
  cv2. imshow ("Image", img)
```
We specify how many milliseconds to show the captured frame (for images – 0, for a webcam-1-10, for video-33). In our case, we will specify one.
As a result, we should already have a video capture from the webcam.
# ![Picture1](https://github.com/KudinovIvan/HandTracks/blob/ver1.0/assets/Picture1.png)
Next, we create the handDetector class and prescribe the following constructor:
class handDetector ():
```python
  def __init__(self, mode=False, maxHands=1, detectionCon=0.5, trackCon=0.5):
    self. mode = mode
    self.maxHands = maxHands
    self.detectionCon = detectionCon
    self.trackCon = trackCon
    self.mpHands = mp.solutions.hands
    self.hands = self.mpHands.Hands(self.mode, self.maxHands,
    self.detectionCon, self.trackCon)
    self.mpDraw = mp.solutions.drawing_utils
```
Now we will write the findHands function
```python
  def findHands(self, img, draw=True):
    #color detection
    imgRGB = cv2. cvtColor(img, cv2. COLOR_BGR2RGB)
    #drawing the palm
    self.results = self.hands. process (imgRGB)
    #drawing key points
    if self.results.multi_hand_landmarks:
      for handLms in self.results.multi_hand_landmarks:
        if draw:
          self.mpDraw.draw_landmarks(img, handLms, self.mpHands. HAND_CONNECTIONS)
    #return of the processed frame
    return img
```
Let's add a few lines to main() and test the above function. Create an instance of the hand Detector () class
```python
  detector = handDetector()
```
And add a line to the loop where the captured frame is sent to the find Hands function, processed and returned. The processed frame is displayed on the screen.
```python
  img = detector.findHands(img)
```
Compile the program
# ![Picture2](https://github.com/KudinovIvan/HandTracks/blob/ver1.0/assets/Picture2.png)
Next, we will write the function findPosition
```python
  def findPosition(self, img, handNo=0, draw=True):
    # declaring an array with coordinates of key points
    lm List = []
    #checking for the presence of key points
    if self.results.multi_hand_landmarks:
      myHand = self.results.multi_hand_landmarks[handNo]
      #a loop that runs through all the key points
      farid, elmin enumerate(my Hand.landmark):
        h, w, c = img.shape
        #determining the X and Y coordinates
        cx, cy = int(lm.x * w), int(lm.y * h)
        #the id of the key point and the X and Y coordinates are added to the array
        lm List.append([id, cx, cy])
        if id == 0:
          #highlighting the zero key point
          v2. circle(img, (cx, cy), 10, (132, 50, 28), cv2. FILLED)
    #returning an array with coordinates
    return lmList
```
To test the function, add the following line to main()
```python
  mist = detector.findPosition (img)
```
MediaPipe has been successfully connected and is working properly
# ![Picture3](https://github.com/KudinovIvan/HandTracks/blob/ver1.0/assets/Picture3.png)
# Defining gestures
We will recognize gestures according to the following logic:
There are 21 key points in total, with 4 points on each finger (see Figure 19). For example, consider the index finger. The fourth point is 8, the second point is 6. If the "y" coordinate of point 8 is less than that of point 6, the finger is raised up. Accordingly, if the "y" coordinate of point 8 is greater than that of point 6 – the finger is not raised up. This method works with all fingers except the thumb. Here you should look at the changes in the "x" coordinate.
# ![Picture4](https://github.com/KudinovIvan/HandTracks/blob/ver1.0/assets/Picture4.png)
Following this logic, you can recognize different gestures. Examples are given in the table.
| Logic | Gesture |
|----:|:----------|
|All fingers are raised up, the thumb is pressed out||xx|
|The index finger is raised up, the other fingers are pressed down||xx|
|All fingers are pressed down||x|
|Прижаты только средний и безымянный пальцы||xc|
Let's try this algorithm in our work. Let's create conditions when the index finger is raised or the thumb is pressed. The corresponding message will be displayed in the console.
```python
  if len(lm List) != 0:
    if lm List[4][1] > lm List[2][1]:
    print("the thumb is pressed")
    if lm List[8][2] < lm List[6][2]:
    print("the Index finger raised")
```
The result is presented below
# ![Picture5](https://github.com/KudinovIvan/HandTracks/blob/ver1.0/assets/Picture5.png)
# ![Picture6](https://github.com/KudinovIvan/HandTracks/blob/ver1.0/assets/Picture6.png)
# ![Picture7](https://github.com/KudinovIvan/HandTracks/blob/ver1.0/assets/Picture7.png)
# Volume control
To control the volume, import it to a file Volume.py the pycaw library
```python
  from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
```
Let's create the VolumeTrack(img, cap) function. The function returns nothing.
```python
  def VolumeTrack(img, cap):
```
Next, we will write the following lines
```python
  #getting information about the audio equipment
  devices = AudioUtilities. GetSpeakers ()
  #activating the equipment
  interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
  #creating a variable for working with audio equipment
  volume = cast(interface, POINTER(IAudioEndpointVolume))
  #getting the maximum and minimum volume levels
  volRange = volume.GetVolumeRange ()
  #minimum volume level
  minVol = volRange[0]
  #maximum volume level
  maxVol = volRange[1]
  volBar = 400
  volPer = 0
  b = 0
  #detector instance 
  detector = ht. handDetector(detectionCon=0.5)
```
Next, run the while loop and perform the same actions as in the main function HandTrack.py.
The volume is set relative to the distance between the thumb and index finger. The greater the distance, the higher the sound volume level.
The function is called from a file HandTrack.py as soon as the hand accepts the next gesture
# ![Picture8](https://github.com/KudinovIvan/HandTracks/blob/ver1.0/assets/Picture8.png)
After this gesture, the window interface will change. Between the thumb and forefinger line appears in the lower left corner will see a rectangular area that will be to illustrate how changing the volume.
```python
  cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
  cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
  cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
  cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

  length = math.hypot(x2 - x1, y2 - y1)*2.5
  vol = np.interp(length, [50, 300], [minVol, maxVol])
  if vol == -96:
    vol = volume.GetMasterVolumeLevel()

  volBar = np.interp(length, [50, 300], [400, 150])
  volPer = np.interp(length, [50, 300], [0, 100])
  volume.SetMasterVolumeLevel(vol, None)

  if length < 50:
    cv2.circle(img, (cx, cy), 15, (0, 255, 0), cv2.FILLED)

  cv2.rectangle(img, (50, 150), (85, 400), (255, 0, 0), 3)
  cv2.rectangle(img, (50, int(volBar)), (85, 400), (255, 0, 0), cv2.FILLED)
  cv2.putText(img, f'{int(volPer)} %', (40, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)
```
The volume change function will work as long as the index finger is raised. As soon as it goes down, the VolumeTrack function will stop.
# ![Picture9](https://github.com/KudinovIvan/HandTracks/blob/ver1.0/assets/Picture9.png)
# ![Picture10](https://github.com/KudinovIvan/HandTracks/blob/ver1.0/assets/Picture10.png)
# Mouse cursor control
To control the mouse cursor, import it to a file HandTrack.py the mouse library.
```python
  import mouse
```
To control the mouse cursor when capturing each frame, it is necessary to read the coordinates of the zero control point and move the cursor to the difference obtained from the initial position of the palm and the current one.
The function by which the mouse cursor starts moving
```python
  mouse.move((current - list[0][1])/2, (mlist[0][2] - currency)/2, absolute = False, duration=0)
```
In order to click with the left mouse button, you need to squeeze all the fingers on your hand, except for the thumb.
```python
  elif lm List[8][2] > lm List[6][2] and lm List[12][2] > lm List[10][2] and lm List[4][1] > lm List[2][1] and \
  lm List[16][2] > lm List[14][2] and lm List[20][2] > lm List[18][2] and beg > 30:
  mouse.click('left')
```
# ![Picture11](https://github.com/KudinovIvan/HandTracks/blob/ver1.0/assets/Picture11.png)
The function of stopping the program is also implemented. In order to put the program on pause and I don't move the cursor when it is not necessary, you must show the following gesture.
```python
  elf lm List[8][2] < lm List[6][2] and lm List[12][2] > lm List[10][2] and lm List[4][1] < lm List[2][1] and \
  lm List[16][2] > lm List[14][2] and lm List[20][2] < lm List[18][2] and beg > 30:
    start = False
```
# ![Picture12](https://github.com/KudinovIvan/HandTracks/blob/ver1.0/assets/Picture12.png)
In order to remove the program from the "pause", you need to show the same gesture.
