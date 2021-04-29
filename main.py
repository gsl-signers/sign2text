import cv2
import time
import PIL
from PIL import ImageTk
import numpy as np
import HandTrackingModule as htm
import math
from tkinter import *

root = Tk()
root.bind('<Escape>', lambda e: root.quit())
lmain = Label(root)
lmain.pack()


def rotate(origin, point, angle):
    """
    Rotate a point counterclockwise by a given angle around a given origin.

    The angle should be given in radians.
    """
    ox, oy = origin
    px, py = point

    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
    return qx, qy


wCam, hCam = 640, 480

gestures = [
    # [[0, 159, 453], [1, 130, 416], [2, 124, 381], [3, 138, 355], [4, 158, 343], [5, 176, 347], [6, 195, 338], [7, 196, 347], [8, 189, 359], [9, 203, 362], [10, 219, 352], [11, 216, 361], [12, 206, 372], [13, 222, 385], [14, 231, 378], [15, 225, 386], [16, 215, 396], [17, 236, 410], [18, 238, 403], [19, 230, 410], [20, 221, 418]],
    [[0, 173, 197], [1, 201, 212], [2, 226, 213], [3, 243, 206], [4, 251, 203], [5, 244, 195], [6, 274, 185], [7, 294, 180], [8, 311, 178], [9, 242, 184], [10, 275, 175], [
        11, 298, 171], [12, 317, 169], [13, 239, 174], [14, 271, 167], [15, 293, 163], [16, 309, 161], [17, 232, 164], [18, 258, 158], [19, 275, 155], [20, 288, 153]],
    # [[0, 503, 389], [1, 512, 377], [2, 521, 370], [3, 528, 365], [4, 535, 361], [5, 519, 365], [6, 520, 355], [7, 523, 345], [8, 527, 336], [9, 514, 369], [10, 515, 360], [11, 514, 352], [12, 517, 342], [13, 510, 376], [14, 513, 368], [15, 513, 360], [16, 516, 351], [17, 505, 383], [18, 513, 378], [19, 518, 374], [20, 525, 368]],
    [[0, 141, 383], [1, 112, 366], [2, 101, 343], [3, 106, 318], [4, 119, 301], [5, 97, 330], [6, 118, 295], [7, 135, 279], [8, 146, 272], [9, 119, 331], [10, 139, 292], [
        11, 155, 274], [12, 166, 266], [13, 144, 335], [14, 159, 296], [15, 172, 278], [16, 182, 269], [17, 168, 339], [18, 179, 308], [19, 188, 293], [20, 194, 283]],
    # [[0, 262, 393], [1, 291, 395], [2, 313, 390], [3, 329, 388], [4, 339, 397], [5, 320, 355], [6, 345, 325], [7, 360, 308], [8, 372, 291], [9, 311, 344], [10, 336, 312], [11, 354, 294], [12, 368, 279], [13, 301, 338], [14, 325, 307], [15, 342, 290], [16, 354, 277], [17, 293, 336], [18, 312, 313], [19, 324, 301], [20, 333, 290]],
    [[0, 222, 400], [1, 192, 378], [2, 168, 352], [3, 145, 331], [4, 124, 323], [5, 185, 320], [6, 207, 289], [7, 223, 280], [8, 233, 279], [9, 206, 322], [10, 228, 286], [
        11, 245, 276], [12, 255, 277], [13, 228, 327], [14, 245, 292], [15, 260, 282], [16, 269, 282], [17, 249, 333], [18, 257, 304], [19, 266, 293], [20, 273, 289]],
    # [[0, 225, 382], [1, 259, 381], [2, 283, 365], [3, 294, 355], [4, 302, 363], [5, 280, 318], [6, 302, 309], [7, 291, 332], [8, 279, 338], [9, 266, 311], [10, 291, 304], [11, 278, 333], [12, 266, 334], [13, 251, 306], [14, 278, 300], [15, 266, 328], [16, 251, 329], [17, 234, 303], [18, 259, 296], [19, 256, 316], [20, 244, 319]],
    [[0, 198, 449], [1, 190, 408], [2, 193, 373], [3, 196, 343], [4, 191, 317], [5, 253, 377], [6, 288, 350], [7, 310, 337], [8, 327, 326], [9, 271, 399], [10, 309, 369], [
        11, 333, 352], [12, 350, 340], [13, 281, 422], [14, 318, 394], [15, 338, 377], [16, 352, 365], [17, 286, 446], [18, 318, 425], [19, 335, 412], [20, 348, 399]],
    [[0, 294, 381], [1, 292, 352], [2, 305, 334], [3, 325, 330], [4, 340, 334], [5, 326, 318], [6, 348, 289], [7, 360, 273], [8, 370, 261], [9, 345, 332], [10, 376, 313], [
        11, 395, 302], [12, 409, 296], [13, 358, 351], [14, 361, 352], [15, 349, 358], [16, 340, 362], [17, 366, 371], [18, 364, 372], [19, 353, 377], [20, 346, 380]],
    [[0, 163, 207], [1, 188, 228], [2, 210, 243], [3, 228, 253], [4, 238, 254], [5, 256, 209], [6, 288, 216], [7, 311, 219], [8, 332, 219], [9, 248, 190], [10, 253, 222], [
        11, 231, 230], [12, 225, 222], [13, 232, 182], [14, 229, 216], [15, 213, 223], [16, 213, 214], [17, 212, 180], [18, 209, 207], [19, 199, 216], [20, 198, 209]],
    [[0, 102, 313], [1, 137, 306], [2, 168, 289], [3, 192, 272], [4, 212, 265], [5, 147, 242], [6, 163, 212], [7, 171, 193], [8, 177, 175], [9, 125, 234], [10, 131, 198], [
        11, 134, 176], [12, 137, 157], [13, 104, 234], [14, 103, 201], [15, 102, 179], [16, 103, 161], [17, 83, 242], [18, 73, 217], [19, 66, 201], [20, 61, 185]],
    [[0, 147, 275], [1, 175, 291], [2, 201, 297], [3, 219, 295], [4, 237, 291], [5, 214, 286], [6, 231, 297], [7, 248, 302], [8, 266, 302], [9, 203, 266], [10, 206, 281], [
        11, 213, 277], [12, 223, 269], [13, 184, 252], [14, 177, 283], [15, 170, 295], [16, 168, 295], [17, 162, 246], [18, 158, 276], [19, 155, 285], [20, 156, 284]],
    [[0, 89, 362], [1, 124, 363], [2, 154, 361], [3, 178, 359], [4, 193, 346], [5, 152, 307], [6, 179, 298], [7, 192, 315], [8, 196, 333], [9, 146, 294], [10, 172, 266], [
        11, 194, 252], [12, 213, 240], [13, 134, 289], [14, 156, 261], [15, 174, 245], [16, 190, 232], [17, 118, 290], [18, 133, 264], [19, 147, 250], [20, 161, 239]],
    [[0, 175, 419], [1, 187, 372], [2, 210, 336], [3, 232, 309], [4, 241, 282], [5, 270, 370], [6, 317, 373], [7, 344, 377], [8, 364, 382], [9, 275, 398], [10, 328, 397], [
        11, 360, 399], [12, 384, 402], [13, 273, 425], [14, 323, 422], [15, 352, 422], [16, 373, 422], [17, 265, 451], [18, 306, 447], [19, 330, 446], [20, 349, 443]]
]

keys = [
    # "sıkıldım",
    "MERHABA",
    "NASILSIN",
    # "SEViYORUM",
    "GEL",
    # "BEN",
    "SAGOL",
    "GULMEK",
    "iNSALLAH",
    "GULE GULE",
    "SEN",
    "OK",
    "BEN"
]


cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

xsum = 0
ysum = 0

for g in gestures:
    xsum = g[0][1] + g[5][1] + g[17][1]
    ysum = g[0][2] + g[5][2] + g[17][2]
    xsum /= 3
    ysum /= 3
    for i in g:
        i[1] -= xsum
        i[2] -= ysum

    indexMCP = (g[0][1] - g[5][1])**2 + (g[0][2] - g[5][2])**2
    pinkyMCP = (g[0][1] - g[17][1])**2 + (g[0][2] - g[17][2])**2
    scale = (indexMCP + pinkyMCP) / 2
    # angle = math.atan2(g[5][2]-g[0][2], g[5][1]-g[0][1]) + math.pi/3
    for i in g:
        i[1] /= scale / 30
        i[2] /= scale / 30
        # i[1], i[2] = rotate((0,0), (i[1], i[2]), -angle)


print(gestures)

detector = htm.handDetector(detectionCon=0.7)

time.sleep(5)


def show_frame():
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    pTime = 0
    print(lmList)
    # for i in gestures[1]:
    #     cv2.circle(img, (int(i[1]*80 + wCam * 7/8), int(i[2]*80 + hCam * 3/8)), 3, (0, 0, 255), cv2.FILLED)
    # for i in gestures[0]:
    #     cv2.circle(img, (int(i[1]*80 + wCam * 8/8), int(i[2]*80 + hCam * 1/8)), 3, (0, 0, 255), cv2.FILLED)
    if(len(lmList) > 0):
        xsum = lmList[0][1] + lmList[5][1] + lmList[17][1]
        ysum = lmList[0][2] + lmList[5][2] + lmList[17][2]
        xsum /= 3
        ysum /= 3
        for i in lmList:
            i[1] -= xsum
            i[2] -= ysum

        indexMCP = math.sqrt(
            (lmList[0][1] - lmList[5][1])**2 + (lmList[0][2] - lmList[5][2])**2)
        pinkyMCP = math.sqrt(
            (lmList[0][1] - lmList[17][1])**2 + (lmList[0][2] - lmList[17][2])**2)
        scale = (indexMCP + pinkyMCP) / 2
        # angle = math.atan2(lmList[5][2]-lmList[0][2], lmList[5][1]-lmList[0][1]) + math.pi/3

        for i in lmList:
            i[1] /= scale / 30
            i[2] /= scale / 30
            # i[1], i[2] = rotate((0,0), (i[1], i[2]), -angle)
            # cv2.circle(img, (int(i[1] + wCam * 7/8), int(i[2] + hCam * 1/8)), 3, (0, 255, 0), cv2.FILLED)
        # print(lmList)

        nearest = ""
        smallestDist = 0
        secondNearest = ""
        secondSmallestDist = 0
        for g in gestures:
            totalDist = 0

            for p in lmList:
                # if lmList.index(p) == 4:
                #     totalDist += math.sqrt((p[1] - g[lmList.index(p)][1])**2 + (p[2] - g[lmList.index(p)][2])**2) * 100
                # if(lmList.index(p) == 8 or lmList.index(p) == 16 or lmList.index(p) == 20 or lmList.index(p) == 0):
                #     # if lmList.index(p) == 4:
                #     totalDist += math.sqrt((p[1] - g[lmList.index(p)][1])**2 + (p[2] - g[lmList.index(p)][2])**2) * 10
                # else:
                totalDist += math.sqrt((p[1] - g[lmList.index(p)][1])
                                       ** 2 + (p[2] - g[lmList.index(p)][2])**2)

                # if gestures.index(g) == 0:
                #     print("nasılsın:", totalDist)
                # if gestures.index(g) == 1:
                #     print("gel:", totalDist)
            if totalDist < smallestDist or smallestDist == 0:
                secondSmallestDist = smallestDist
                secondNearest = nearest
                smallestDist = totalDist
                nearest = keys[gestures.index(g)]
            if nearest != keys[gestures.index(g)] and (totalDist < secondSmallestDist or secondSmallestDist == 0):
                secondSmallestDist = totalDist
                secondNearest = keys[gestures.index(g)]

        cv2.putText(img, "1. " + nearest, (40, 50),
                    cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
        cv2.putText(img, "2. " + secondNearest, (40, 80),
                    cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 2)
    # Tkinter
    cv2image = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)
    img_func = PIL.Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img_func)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    lmain.after(10, show_frame)

    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime

    # cv2.putText(img,f"FPS {int(fps)}", (40 ,50), cv2.FONT_HERSHEY_COMPLEX,1 ,(255,0,0),2)


show_frame()
root.mainloop()
