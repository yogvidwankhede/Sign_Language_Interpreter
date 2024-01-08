# Sign Language Recognition - utilizing MediaPipe and DTW


This repository provides an implementation of a Sign Recognition Model using the MediaPipe library for landmark extraction and Dynamic Time Warping (DTW) as a similarity metric between signs.

![](Demo1.mp4)

---

## Setup

### 1. Navigate to the Project Directory in the Terminal

### 2. Install Required Libraries

- pip install -r requirements.txt

### 3. Import Videos of Signs for Reference

The structure of the videos/ folder should be as follows:
```
|data/
    |-videos/
          |-Hello/
            |-<video_of_hello_1>.mp4
            |-<video_of_hello_2>.mp4
            ...
          |-Thanks/
            |-<video_of_thanks_1>.mp4
            |-<video_of_thanks_2>.mp4
            ...
```

To automatically generate a small dataset of French signs:

- Install ffmpeg (for MacOS, use brew install ffmpeg)
- Run: python yt_download.py
- Add more YouTube links in yt_links.csv if needed
> Note: The current dataset may be insufficient for optimal results. Consider adding more links or importing your own videos.

### 4. Load the Dataset and Activate the Webcam

- 'python main.py'

### 5. Press the "r" key to record the sign.

---
## Code Description

### MediaPipe's landmark extraction

- We can extract the Hands, Pose, and Face models' important points using MediaPipe's Holistic Model.
As of right now, the implementation just predicts the sign using the Hand model.


### Hand Model

- To specify the hand gesture at each frame, a HandModel has been constructed for this project. 
We set all the places to zero in the event that there is no hand.

- The *feature vector of the HandModel is a list of the angles between each hand's connexions in order to be *invariant to orientation and scale.

### Sign Model

- A list of landmarks is used to generate the SignModel (extracted from a video)

- We store the feature vectors of every hand for every frame.

### Sign Recorder

- The HandModels of the left and right hands for each frame when recording are stored by the SignRecorder class.
- After recording is complete, it calculates the DTW for both the recorded sign and each of the dataset's reference signs.
- In order to produce a result only if the forecast confidence is higher than a threshold, a voting mechanism is finally introduced.

### Dynamic Time Warping

- Time series similarity is often calculated using DTW.
- We calculate the hand connection angle variation's DTW over time.

---
