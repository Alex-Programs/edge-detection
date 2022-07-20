import cv2 as cv
import keyboard

cap = cv.VideoCapture(0)


class Parameters():
    min = 90
    max = 200
    aperture = 3


tracker = cv.TrackerCSRT_create()
bbox = (0, 0, 50, 50)
first = True

while True:
    ret, frame = cap.read()

    frame = cv.Canny(frame, Parameters.min, Parameters.max, apertureSize=Parameters.aperture)

    frame = cv.resize(frame, (frame.shape[1] * 2, frame.shape[0] * 2), 2, 2)

    if first:
        bbox = cv.selectROI(frame, False)
        ok = tracker.init(frame, bbox)

    first = False

    print(bbox)

    ok, bbox = tracker.update(frame)

    frame = cv.cvtColor(frame, cv.COLOR_GRAY2RGB)

    p1 = (int(bbox[0]), int(bbox[1]))
    p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
    cv.rectangle(frame, p1, p2, (0, 0, 255), 2, 1)

    if keyboard.is_pressed("7"):
        Parameters.min = Parameters.min + 1

    if keyboard.is_pressed("1"):
        if Parameters.min > 0:
            Parameters.min = Parameters.min - 1

    if keyboard.is_pressed("8"):
        Parameters.max = Parameters.max + 1

    if keyboard.is_pressed("2"):
        if Parameters.max > 0:
            Parameters.max = Parameters.max - 1

    if keyboard.is_pressed("9"):
        if Parameters.aperture < 7:
            Parameters.aperture = Parameters.aperture + 2

    if keyboard.is_pressed("3"):
        if Parameters.aperture > 3:
            Parameters.aperture = Parameters.aperture - 2

    print(Parameters.min, Parameters.max, Parameters.aperture)

    cv.imshow("Input", frame)

    c = cv.waitKey(1)
    if c == 27:
        break

cap.release()
cv.destroyAllWindows()
