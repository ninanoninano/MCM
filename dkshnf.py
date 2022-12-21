import cv2
from cvzone.HandTrackingModule import HandDetector
from cvzone.PoseModule import PoseDetector
from cvzone.ClassificationModule import Classifier
import math
import numpy as np
from google.protobuf.json_format import MessageToDict
import mediapipe as mp

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1960)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1440)




detectorH = HandDetector(maxHands=2)
detectorP = PoseDetector()
classifier = Classifier("Model/keras_model.h5", "Model/labels.txt")

offset = 20
imgSize = 300
counter = 0

labels = ["Rock", "Paper"]

mpHands = mp.solutions.hands
hands1 = mpHands.Hands(
    static_image_mode=False,
    model_complexity=1,
    min_detection_confidence=0.75,
    min_tracking_confidence=0.75,
    max_num_hands=2)



while True:
    success, img = cap.read()
    # Flip the image(frame)
    img = cv2.flip(img, 1)

    imgOutput = img.copy()
    hands, img = detectorH.findHands(img)
    img = detectorP.findPose(img)
    # Convert BGR image to RGB image
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    if hands:
        hand = hands[0]
        x, y, w, h = hand['bbox']

        # Process the RGB image
        results = hands1.process(imgRGB)


        imgWhite = np.ones((imgSize, imgSize, 3), np.uint8)*255
        imgCrop = img[y-offset:y + h + offset, x-offset:x + w + offset]

        imgCropShape = imgCrop.shape

        aspectRatio = h / w
        if aspectRatio > 1:
            k = imgSize / h
            wCal = math.ceil(k * w)
            ImgResize = cv2.resize(imgCrop, (wCal, imgSize))
            imgResizeShape = ImgResize.shape
            wGap = math.ceil((imgSize - wCal) / 2)
            imgWhite[:, wGap:wCal + wGap] = ImgResize
            prediction, index = classifier.getPrediction(imgWhite)
            print(prediction, index)

        else:
            k = imgSize / w
            hCal = math.ceil(k * h)
            ImgResize = cv2.resize(imgCrop, (imgSize, hCal))
            imgResizeShape = ImgResize.shape
            hGap = math.ceil((imgSize - hCal) / 2)
            imgWhite[hGap:hCal + hGap, :] = ImgResize
            prediction, index = classifier.getPrediction(imgWhite)
            print(prediction, index)

        if results.multi_hand_landmarks is not None:
            if results.multi_hand_landmarks:

                # Both Hands are present in image(frame)
                if len(results.multi_handedness) == 2:
                    # Display 'Both Hands' on the image
                    cv2.putText(img, 'Both Hands', (500, 50), cv2.FONT_HERSHEY_COMPLEX, 0.9, (0, 255, 0), 2)

                # If any hand present
                else:
                    for i in results.multi_handedness:

                        # Return whether it is Right or Left Hand
                        label = MessageToDict(i)['classification'][0]['label']

                        # 왼손 행동제어
                        if label == 'Left':
                            # Display 'Left Hand' on
                            # left side of window
                            cv2.putText(img, label + ' Hand', (20, 50), cv2.FONT_HERSHEY_COMPLEX, 0.9, (0, 255, 0), 2)
                            if labels[index] == 'Rock':
                                cv2.imshow("ImageWhite", imgWhite)

                        # 오른손 행동제어
                        if label == 'Right':
                            # Display 'Left Hand'
                            # on left side of window
                            cv2.putText(img, label + ' Hand', (1100, 50), cv2.FONT_HERSHEY_COMPLEX, 0.9, (0, 255, 0), 2)

        cv2.putText(imgOutput, labels[index], (x, y-20), cv2.FONT_HERSHEY_SCRIPT_COMPLEX, 2, (255, 0, 255), 2)
        cv2.rectangle(imgOutput, (x-offset, y-offset), (x + w + offset, y + h+offset), (255, 0, 255), 4)
        cv2.imshow("ImageCrop", imgCrop)


    cv2.imshow("Image", img)
    cv2.waitKey(1)