import cv2
import numpy as np
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

def vol_control(img, detector, lmList, fingers):

    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))

    length, img, lineInfo = detector.findDistance(4, 8, img, lmList)
    volPer = np.interp(length, [25, 150], [0, 100])

    smoothness = 10
    volPer = smoothness * round(volPer/smoothness)

    if fingers[4]:
        volume.SetMasterVolumeLevelScalar(volPer/100, None)
        colorVol = (0, 255, 0)
    else:
        colorVol = (255, 0, 0)

    cVol = round(volume.GetMasterVolumeLevelScalar()*100)
    cv2.putText(img, "Set Volume: {0}".format(volPer), (30,50), cv2.FONT_HERSHEY_COMPLEX, 1, (255,0,0), 2)
    cv2.putText(img, "Volume: {0}".format(cVol), (400,50), cv2.FONT_HERSHEY_COMPLEX, 1, colorVol, 2)
