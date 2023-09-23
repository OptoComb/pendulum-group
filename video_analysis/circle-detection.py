import tkinter as tk
from tkinter import _Cursor, _Relief, _ScreenUnits, _TakeFocusValue, Misc
from typing import Any
from typing_extensions import Literal

import cv2
from cv2.typing import MatLike, Size

import numpy as np

video_source = "video_analysis/iPhone_data/simple.mov"


class Application(tk.Frame):
    def __init__(
        self,
        master: Misc | None = None,
        cnf: dict[str, Any] | None = ...,
        *,
        background: str = ...,
        bd: _ScreenUnits = ...,
        bg: str = ...,
        border: _ScreenUnits = ...,
        borderwidth: _ScreenUnits = ...,
        class_: str = ...,
        colormap: Misc | Literal["new", ""] = ...,
        container: bool = ...,
        cursor: _Cursor = ...,
        height: _ScreenUnits = ...,
        highlightbackground: str = ...,
        highlightcolor: str = ...,
        highlightthickness: _ScreenUnits = ...,
        name: str = ...,
        padx: _ScreenUnits = ...,
        pady: _ScreenUnits = ...,
        relief: _Relief = ...,
        takefocus: _TakeFocusValue = ...,
        visual: str | tuple[str, int] = ...,
        width: _ScreenUnits = ...,
    ) -> None:
        super().__init__(
            master,
            cnf,
            background=background,
            bd=bd,
            bg=bg,
            border=border,
            borderwidth=borderwidth,
            class_=class_,
            colormap=colormap,
            container=container,
            cursor=cursor,
            height=height,
            highlightbackground=highlightbackground,
            highlightcolor=highlightcolor,
            highlightthickness=highlightthickness,
            name=name,
            padx=padx,
            pady=pady,
            relief=relief,
            takefocus=takefocus,
            visual=visual,
            width=width,
        )


def getVideoCapture(filename: str) -> cv2.VideoCapture:
    vcap = cv2.VideoCapture(filename)
    if not vcap.isOpened():
        raise FileExistsError(f"cannot open the video file: {filename}")
    return vcap


def getVideoInfo(vcap: cv2.VideoCapture) -> {"width": float, "height": float, "fps": float}:
    width: float = vcap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height: float = vcap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    fps: float = vcap.get(cv2.CAP_PROP_FPS)
    return {"width": width, "height": height, "fps": fps}

def calibrate(
    frame: MatLike,
    cameraMatrix: MatLike = np.array(
        [
            [2.23429413e03, 0.00000000e00, 6.36470010e02],
            [0.00000000e00, 2.31772325e03, 5.74525725e02],
            [0.00000000e00, 0.00000000e00, 1.00000000e00],
        ]
    ),
    distortionCoefficients: MatLike = np.array(
        [[-0.77271385, -0.55940247, -0.00505415, 0.08305395, 1.77990709]]
    ),
    imageSize: Size=(1080,1920),
    scalingParameter: float=1 # 変換後に出る画像端の歪をどの程度含むか
) -> MatLike:
    optCamMtx, (x, y, width, height) = cv2.getOptimalNewCameraMatrix(cameraMatrix, distortionCoefficients, imageSize, scalingParameter, imageSize)
    dst = cv2.undistort(frame, cameraMatrix, distortionCoefficients, None, optCamMtx)
    dst = dst[y: y+height, x: x+width]
    return dst

def circleDetect(frame: MatLike, minDist: float, param2: float) -> MatLike:
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    circles = cv2.HoughCircles(
        gray_frame,
        cv2.HOUGH_GRADIENT, # Hough変換手法
        dp=1, # 検出基準の緩さ
        minDist=minDist, # 検出される円の最小距離（円の重複度）
        param1=100, # Canny法 の Hysteresis処理 の上限値
        param2=param2, # Canny法 の Hysteresis処理 の下限値（検出感度の逆）
        # minRadius=0, # 検出円の半径の下限値
        # maxRadius=0 # 検出円の半径の上限値
    )
    return circles

def main():
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()


if __name__ == "__main__":
    main()
