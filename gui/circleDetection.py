import cv2
from cv2.typing import MatLike
import tkinter as tk
from tkinter import ttk, font, Misc
from PIL import Image, ImageTk
from numpy import array as npArray

from csv import writer
from time import time
from sys import stderr


class Application(ttk.Frame):
    def __init__(self, master: Misc | None, video_source=0):
        super().__init__(master)

        self.master.title("Tkinter with Video Streaming and Capture")

        self.vcap = self.getVideoSourceOrExit(video_source)

        # set video size
        self.height = 380
        self.width = 440
        self.video_capture = ImageTk.PhotoImage(file="app/img/440x380.png")

        # set widget size
        self.width_and_margin = self.width + 30
        self.height_and_margin = self.height + 50
        self.master.geometry(
            f"{max(self.width_and_margin, 600)}x{self.height_and_margin+270}"
        )

        ###button flags###
        self.circle_detection_flag = False
        self.save_flag = False

        ###fitting parameter###
        self.mdist = 20
        self.par1 = 100
        self.par2 = 60

        ###csv用意###
        self.csv_file = "test.csv"
        self.init_time = time()
        self.initializeCSV(filename_or_path=self.csv_file)
        #############

        self.create_widgets()

        # ---------------------------------------------------------
        # Canvas Update
        # ---------------------------------------------------------

        self.delay = 1  # [milliseconds]
        self.update()

    def getVideoSourceOrExit(self, video_source: int = 0):
        vcap = cv2.VideoCapture(video_source)
        if not vcap.isOpened():
            stderr.write("cannot access video source.")
            exit()

        video_origin_width = int(vcap.get(cv2.CAP_PROP_FRAME_WIDTH))
        video_origin_height = int(vcap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        print(f"resolution: {video_origin_width}x{video_origin_height}")

        return vcap

    def initializeCSV(self, filename_or_path: str = "test.csv"):
        columns_title = ["time"]
        for i in range(8):
            lis = [f"x{i + 1}", f"y{i + 1}", f"r{i + 1}"]
            columns_title.extend(lis)

        with open(file=filename_or_path, mode="w", newline="") as f:
            writer_object = writer(f)
            writer_object.writerow(columns_title)
            f.close()

    def create_widgets(self):
        # ---------------------------------------------------------
        # Font
        # ---------------------------------------------------------

        fontFamily = "Meiryo UI"
        fontSize = 15
        fontConfig = font.Font(family=fontFamily, size=fontSize, weight=font.NORMAL)
        fontConfig_big_bold = font.Font(
            family=fontFamily, size=fontSize + 10, weight=font.BOLD
        )

        font_frame = fontConfig
        font_btn = fontConfig_big_bold
        font_lbl = fontConfig

        ###Frame_Camera###

        self.frame_cam = ttk.LabelFrame(self.master, text="Camera")
        self.frame_cam.place(x=10, y=10)
        self.frame_cam.configure(
            width=self.width_and_margin, height=self.height_and_margin
        )
        self.frame_cam.grid_propagate(0)

        # Canvas
        self.canvas1 = tk.Canvas(self.frame_cam)
        self.canvas1.configure(width=self.width, height=self.height)
        self.canvas1.grid(column=0, row=0, padx=10, pady=10)

        ###Frame_Camera_End###

        ###Frame_Buttons###

        self.frame_btn = ttk.LabelFrame(self.master, text="Control")
        self.frame_btn.place(x=10, y=10 + self.height_and_margin)
        self.frame_btn.configure(width=max(self.width_and_margin, 570), height=100)
        self.frame_btn.grid_propagate(0)

        # circle detection button
        self.btn_snapshot = ttk.Button(self.frame_btn, text="円検出")
        self.btn_snapshot.configure(width=12, command=self.press_circle_detection)
        self.btn_snapshot.grid(column=0, row=0, padx=10, pady=10)

        # Close button
        self.btn_close = ttk.Button(self.frame_btn, text="Close")
        self.btn_close.configure(width=12, command=self.press_close_button)
        self.btn_close.grid(column=1, row=0, padx=10, pady=10)

        # Seve button
        self.btn_save = ttk.Button(self.frame_btn, text="CSV出力")
        self.btn_save.configure(width=12, command=self.press_save_flag)
        self.btn_save.grid(column=2, row=0, padx=10, pady=10)

        ###Frame_Buttons_End###

        ##Frame_params###

        self.frame_param = ttk.LabelFrame(self.master, text="Parameters")
        self.frame_param.place(x=10, y=+10 + 100 + self.height_and_margin)
        self.frame_param.configure(width=max(self.width_and_margin, 570), height=150)
        self.frame_param.grid_propagate(0)

        # min Dist
        self.minDist_label = ttk.Label(self.frame_param, text="min dist", font=font_lbl)
        self.minDist_label.grid(column=0, row=0, padx=10, pady=10)

        self.minDist_number = tk.DoubleVar()
        self.minDist_number.set(self.mdist)
        self.minDist_var = ttk.Entry(
            self.frame_param, textvariable=self.minDist_number, width=5
        )
        self.minDist_var.grid(column=1, row=0, padx=10, pady=10)

        # param1
        self.param1_label = ttk.Label(self.frame_param, text="param1", font=font_lbl)
        self.param1_label.grid(column=2, row=0, padx=10, pady=10)

        self.param1_number = tk.DoubleVar()
        self.param1_number.set(self.par1)
        self.param1_var = ttk.Entry(
            self.frame_param, textvariable=self.param1_number, width=5
        )
        self.param1_var.grid(column=3, row=0, padx=10, pady=10)

        # param2
        self.param2_label = ttk.Label(self.frame_param, text="param2", font=font_lbl)
        self.param2_label.grid(column=4, row=0, padx=10, pady=10)

        self.param2_number = tk.DoubleVar()
        self.param2_number.set(self.par2)
        self.param2_var = ttk.Entry(
            self.frame_param, textvariable=self.param2_number, width=5
        )
        self.param2_var.grid(column=5, row=0, padx=10, pady=10)

        # change
        self.btn_change = ttk.Button(self.frame_param, text="Change")
        self.btn_change.configure(width=12, command=self.press_change)
        self.btn_change.grid(column=5, row=1, padx=10, pady=10)

        ##Frame_params_End###

    def calibration(self, frame: MatLike):
        camera_mtx = npArray(
            [
                [2.23429413e03, 0.00000000e00, 6.36470010e02],
                [0.00000000e00, 2.31772325e03, 5.74525725e02],
                [0.00000000e00, 0.00000000e00, 1.00000000e00],
            ]
        )

        distortion_coefficients = npArray(
            [[-0.77271385, -0.55940247, -0.00505415, 0.08305395, 1.77990709]]
        )

        # 最適画像サイズ
        wh = (1080, 1920)

        # フリースケーリングパラメータ（変換後に出る画像端の黒い部分をどの程度含むか）
        α = 1

        new_camera_mtx, (x, y, w, h) = cv2.getOptimalNewCameraMatrix(
            camera_mtx, distortion_coefficients, wh, α
        )
        dst = cv2.undistort(
            frame, camera_mtx, distortion_coefficients, newCameraMatrix=new_camera_mtx
        )
        dst = dst[y : y + h, x : x + w]
        return dst

    def update(self):
        # count timer
        second = time() - self.init_time

        # Get a frame from the video source
        can_get_frame, frame = self.vcap.read()

        if not can_get_frame:
            # maybe unreachable
            self.video_capture = ImageTk.PhotoImage(file="app/img/440x380.png")
            self.canvas1.create_image(0, 0, image=self.video_capture, anchor=tk.NW)
            self.vcap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            stderr("couldn't get camera frame")
            exit()

        # カメラ歪補正
        # frame = self.calibration(frame)
        frame = frame[0 : self.height, 0 : self.width]
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        if self.circle_detection_flag:
            gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
            circles = cv2.HoughCircles(
                gray,
                cv2.HOUGH_GRADIENT,
                dp=1,
                minDist=self.mdist,
                param1=self.par1,
                param2=self.par2,
                minRadius=0,
                maxRadius=0,
            )
            if circles is not None:
                for circle in circles:
                    circle_color = (255, 0, 0)
                    circle_thickness = 3
                    for x, y, r in circle:
                        frame = cv2.circle(
                            frame,
                            (int(x), int(y)),
                            int(r),
                            circle_color,
                            circle_thickness,
                        )

                if self.save_flag:
                    with open(self.csv_file, "a", newline="") as f:
                        writer_object = writer(f)
                        writer_object.writerow([second] + circle.flatten().tolist())
                        f.close()
        self.video_capture = ImageTk.PhotoImage(image=Image.fromarray(frame))
        self.canvas1.create_image(0, 0, image=self.video_capture, anchor=tk.NW)
        self.master.after(self.delay, self.update)

    def press_close_button(self):
        self.master.destroy()
        self.vcap.release()

    def press_circle_detection(self):
        self.circle_detection_flag = not self.circle_detection_flag
        self.btn_snapshot.config(text=("円検出中" if self.circle_detection_flag else "円検出"))

    def press_save_flag(self):
        self.save_flag = not self.save_flag
        self.btn_save.config(text=("CSV出力中" if self.save_flag else "CSV出力"))

    def press_change(self):
        ###fitting parameter###
        self.mdist = self.minDist_number.get()
        self.par1 = self.param1_number.get()
        self.par2 = self.param2_number.get()


def main():
    root = tk.Tk()
    app = Application(master=root, video_source=0)  # Inherit
    app.mainloop()


if __name__ == "__main__":
    main()
