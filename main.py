import cv2 as cv
import keyboard

cap = cv.VideoCapture(0)


class Parameters():
    min = 70
    max = 150
    aperture = 3


while True:
    ret, frame = cap.read()

    frame = cv.Canny(frame, Parameters.min, Parameters.max, apertureSize=Parameters.aperture)

    frame = cv.resize(frame, (frame.shape[1] * 2, frame.shape[0] * 2), 2, 2)

    contours, heirarchy = cv.findContours(frame, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    simplified = []

    for polygon in contours:
        simplified.append(cv.approxPolyDP(polygon, 0.01 * cv.arcLength(polygon, True), True))

    simplified = contours

    frame = cv.cvtColor(frame, cv.COLOR_GRAY2RGB)

    largestContourSize = 0
    largestContour = None
    largestContourIndex = 0
    index = 0

    for polygon in simplified:
        index += 1

        area = cv.contourArea(polygon)
        if area > largestContourSize:
            largestContourSize = area
            largestContour = polygon
            largestContourIndex = index

    # overlay the caclulated polygons with a white area and red border. If it's the largest contour, fill in blue with green border
    index = 0

    for polygon in simplified:
        index += 1

        if index == largestContourIndex:
            cv.drawContours(frame, [polygon], -1, (255, 0, 0), -1)
            cv.drawContours(frame, [polygon], -1, (0, 255, 0), 1)
            continue

        cv.drawContours(frame, [polygon], -1, (255, 255, 255), -1)
        cv.drawContours(frame, [polygon], -1, (0, 0, 255), 1)

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
