import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import numpy as np

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

# Importing all images
imgBackground = cv2.imread("Resources/background.png")
imgball = cv2.imread("Resources/ball.png", cv2.IMREAD_UNCHANGED)
imgbat1 = cv2.imread("Resources/bat1.png", cv2.IMREAD_UNCHANGED)  # 26*129
imgbat2 = cv2.imread("Resources/bat2.png", cv2.IMREAD_UNCHANGED)
imgtop = cv2.imread("Resources/top.png", cv2.IMREAD_UNCHANGED)
imgbottom = cv2.imread("Resources/bottom.png", cv2.IMREAD_UNCHANGED)
imgGameOver = cv2.imread("Resources/background.png")

detector = HandDetector(detectionCon=0.8, maxHands=2)

# Variables
ballPos = [100, 100]
speedX = 15
speedY = 15
gameOver = False

while True:
    _, img = cap.read()
    img = cv2.flip(img, 1)

    # Find hands and it's landmarks
    hands = detector.findHands(img, flipType=False, draw=False)

    # Overlaying the background image
    img = cv2.addWeighted(img, 0.2, imgBackground, 0.8, 0)

    # Check for hands
    if hands:
        for hand in hands:
            x, y, w, h = hand['bbox']
            h1, w1, _ = imgbat1.shape
            y1 = y - h1//2
            y1 = np.clip(y1, 20, 415)
            if hand['type'] == 'Left':
                img = cvzone.overlayPNG(img, imgbat1, (20, y1))
                if 59 < ballPos[0] < 59+w1 and y1 < ballPos[1] < y1+h1:
                    speedX = -speedX
                    ballPos[0] += 30
            if hand['type'] == 'Right':
                img = cvzone.overlayPNG(img, imgbat2, (1210, y1))
                if 1195-50 < ballPos[0] < 1195-30 and y1 < ballPos[1] < y1+h1:
                    speedX = -speedX
                    ballPos[0] -= 30
    # Game Over
    if ballPos[0] < 40 or ballPos[0] > 1200:
        gameOver = True

    if gameOver:
        img = imgGameOver
        if ballPos[0] < 40:
            cv2.putText(img, "Player 2 wins", (300, 450), cv2.FONT_HERSHEY_COMPLEX, 3, (255, 255, 255), 5)
        else:
            cv2.putText(img, "Player 1 wins", (300, 450), cv2.FONT_HERSHEY_COMPLEX, 3, (255, 255, 255), 5)
    else:
        # Move the ball
        if ballPos[1] >= 500 or ballPos[1] <= 10:
            speedY = -speedY

        ballPos[0] += speedX
        ballPos[1] += speedY

        # Draw the ball
        img = cvzone.overlayPNG(img, imgball, ballPos)
        img = cvzone.overlayPNG(img, imgtop, (0, 5))
        img = cvzone.overlayPNG(img, imgbottom, (0, 550))

    cv2.imshow("image", img)
    cv2.waitKey(1)
