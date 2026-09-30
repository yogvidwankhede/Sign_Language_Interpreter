# Sign Language Recognition - utilizing MediaPipe and DTW


This repository is a modified fork-style copy of
[gabguerin/Sign-Language-Recognition--MediaPipe-DTW](https://github.com/gabguerin/Sign-Language-Recognition--MediaPipe-DTW)
(MIT License, Copyright (c) 2022 gabguerin), which in turn is based on the
[Sicara blog post "Sign language recognition using MediaPipe"](https://www.theodo.com/blog/sign-language-recognition-using-mediapipe).
It recognises isolated signs from MediaPipe hand landmarks, using Dynamic Time Warping (DTW) as the similarity
measure between a recorded sign and reference videos. See [Attribution](#attribution) for what comes from
upstream and what was changed here.

![](Demo1.mp4)

---

## Setup

### 1. Navigate to the Project Directory in the Terminal

### 2. Install Required Libraries

- pip install -r requirements.txt

The last two requirements are only used by `utils/sentence.py`. It also needs the spaCy English model
(`python -m spacy download en_core_web_sm`). The pinned versions are from 2021 and may not install on a current Python.

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
Landmarks are set to zero when a hand is not detected, and `SignModel` then skips those frames.

- The *feature vector of the HandModel is a list of the angles between each hand's connexions in order to be *invariant to orientation and scale.

### Sign Model

- A list of landmarks is used to generate the SignModel (extracted from a video)

- We store the feature vectors of every hand for every frame.

### Sign Recorder

- The HandModels of the left and right hands for each frame when recording are stored by the SignRecorder class.
- After recording is complete, it calculates the DTW for both the recorded sign and each of the dataset's reference signs.
- In order to produce a result only if the forecast confidence is higher than a threshold, a voting mechanism is finally introduced.
  In this repository the defaults are `batch_size=1, threshold=0.8`, which is plain nearest-neighbour matching. The paper
  describes `batch_size=2`, and upstream uses `batch_size=5, threshold=0.5`.

### Dynamic Time Warping

- Time series similarity is often calculated using DTW.
- We calculate the hand connection angle variation's DTW over time.

---

## Attribution

The recognition pipeline (hand-angle `HandModel`, `SignModel`, DTW distances, reference-video dataset loading and the
webcam loop) comes from the upstream repository above, which is MIT licensed. The upstream copyright and permission
notice is kept in [LICENSE](LICENSE), as the MIT License requires.

Comparison against upstream at commit `68948d8`:

| File | Status |
|---|---|
| `models/hand_model.py`, `models/sign_model.py`, `utils/dataset_utils.py` | Identical to upstream |
| `webcam_manager.py`, `utils/mediapipe_utils.py` | Identical to upstream |
| `utils/dtw.py`, `utils/landmark_utils.py`, `yt_download.py` | Upstream code; only docstrings removed |
| `sign_recorder.py` | Upstream code; docstrings removed; voting defaults changed from `batch_size=5, threshold=0.5` to `batch_size=1, threshold=0.8`; "unknown" message changed to English |
| `main.py` | Upstream loop plus a call to the sentence step below |
| `utils/convList.py`, `utils/sentence.py` | Added here |
| `yt_links_ind.csv`, demo videos, `Documents/` | Added here |

What was added here is a keyword lookup, not sentence generation: `utils/sentence.py` checks whether the recognised
words all appear in one of eight hard-coded English sentences, otherwise joins the words, and speaks the result with
`pyttsx3`. The system recognises isolated signs from a small reference set; it does not interpret or translate a sign
language.

## Publication

Mankar Y., Wankhede Y., Thune V., Khawshe S., Sahu M. (2024). Real-Time Sign Language Interpreter Using MediaPipe,
Dynamic Time Warping, and NLP. In: *Multi-Strategy Learning Environment* (ICMSLE 2024), Algorithms for Intelligent
Systems, Springer, pp. 87-98. https://doi.org/10.1007/978-981-97-1488-9_7

Citation metadata is in [CITATION.cff](CITATION.cff).

## Known limitations

- The reference videos were downloaded from YouTube through `yt_download.py`. The repository does not include them,
  and their licences and the signers' consent have not been checked. Do not redistribute them.
- Dependencies are pinned to 2021-era versions (`mediapipe==0.8.7.3`, `pytube==11.0.1`). `pytube` is no longer
  maintained.
- No test set, signer-independent evaluation or accuracy script is included, so the paper's reported accuracy cannot be
  reproduced from this repository.

## Tests

```
pip install numpy pandas fastdtw pytest
python -m pytest -q tests
```

The tests stub `mediapipe` and `cv2` when they are not installed. They cover DTW ranking, the different-hands rule and
the voting defaults. They do not cover landmark extraction or the webcam loop.
