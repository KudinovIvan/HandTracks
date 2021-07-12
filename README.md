# HandTracks
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
