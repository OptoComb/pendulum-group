# video_source のファイル名を書き換えて実行

import cv2

import PIL.Image, PIL.ImageTk
import tkinter as tk
from tkinter import Misc, ttk, font

from csv import writer
from time import time

# from numpy import array as npArray
import sys

video_source = "IMG_4001.mov"
delay = 1  # milli seconds


class Application(tk.Frame):
    def __init__(self, master: Misc | None, video_source: str = video_source):
        super().__init__(master)

        # ---------------------------------------------------------
        # Open the video source
        # ---------------------------------------------------------

        self.vcap = cv2.VideoCapture(video_source)

        if not self.vcap.isOpened():
            sys.stderr.write("cannot access video source.")
            exit()

        self.width = int(self.vcap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.vcap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        print(f"resolusion: {self.width}x{self.height}")
        self.width_and_margin = self.width // 2 + 30
        self.height_and_margin = self.height // 2 + 30

        self.frame_rates = self.vcap.get(cv2.CAP_PROP_FPS)
        print(f"fps: {self.frame_rates}")

        self.master.geometry(
            f"{self.width_and_margin+20}x{self.height_and_margin + self.height//2 +222}"
        )
        self.master.title("Tkinter with Video Streaming and Capture")

        # ---------------------------------------------------------
        # initialize setting
        # ---------------------------------------------------------

        self.csvfile = f"{video_source.replace('.mov', '')}.csv"
        self.init_time = time()
        self.circle_detection_flag = False
        self.save_flag = False

        ###fitting parameter###
        self.mdist = 50
        self.par1 = 100
        self.par2 = 31

        ###csv用意###
        self.frame_iterator = 0
        columns_name = ["frame iterator", "time"]

        for i in range(10):
            lis = [f"x{i + 1}", f"y{i + 1}", f"r{i + 1}"]
            columns_name.extend(lis)

        with open(self.csvfile, "w", newline="") as f:
            writer_object = writer(f)
            writer_object.writerow(columns_name)
            f.close()
        #############

        # ---------------------------------------------------------
        # Font
        # ---------------------------------------------------------

        fontFamily = "Meiryo UI"
        fontSize = 15
        fontConfig = font.Font(family=fontFamily, size=fontSize, weight=font.NORMAL)
        fontConfig_bold = font.Font(family=fontFamily, size=fontSize, weight=font.BOLD)

        self.font_frame = fontConfig
        self.font_btn_big = fontConfig_bold

        self.font_lbl_bigger = font.Font(family=fontFamily, size=45, weight="bold")
        self.font_lbl_big = font.Font(family=fontFamily, size=20, weight="bold")
        self.font_lbl_middle = font.Font(family=fontFamily, size=15, weight="bold")
        self.font_lbl_small = font.Font(family=fontFamily, size=12, weight="normal")

        # ---------------------------------------------------------
        # Widget
        # ---------------------------------------------------------

        self.create_widgets()

        # ---------------------------------------------------------
        # Canvas Update
        # ---------------------------------------------------------

        self.delay = 15  # [milli seconds]
        self.update()

    def create_widgets(self):
        ###Frame_Camera###

        self.frame_cam = tk.LabelFrame(self.master, text="Camera", font=self.font_frame)
        self.frame_cam.place(x=10, y=10)
        self.frame_cam.configure(
            width=self.width_and_margin, height=self.height_and_margin
        )
        self.frame_cam.grid_propagate(False)

        # Canvas
        self.canvas1 = tk.Canvas(self.frame_cam)
        self.canvas1.configure(width=self.width, height=self.height)
        self.canvas1.grid(column=0, row=0, padx=10, pady=10)

        ###Frame_Camera_End###

        ###Frame_Buttons###

        self.frame_btn = tk.LabelFrame(
            self.master, text="Control", font=self.font_frame
        )
        self.frame_btn.place(x=10, y=self.height_and_margin + 10)
        self.frame_btn.configure(width=self.width_and_margin, height=100)
        self.frame_btn.grid_propagate(False)

        # circle detection button
        self.btn_snapshot = tk.Button(
            self.frame_btn, text="円検出", font=self.font_btn_big
        )
        self.btn_snapshot.configure(
            width=12, height=1, command=self.press_circle_detection
        )
        self.btn_snapshot.grid(column=0, row=0, padx=20, pady=10)

        # Close button
        self.btn_close = tk.Button(self.frame_btn, text="Close", font=self.font_btn_big)
        self.btn_close.configure(width=12, height=1, command=self.press_close_button)
        self.btn_close.grid(column=1, row=0, padx=20, pady=10)

        # Seve button
        self.btn_save = tk.Button(self.frame_btn, text="CSV出力", font=self.font_btn_big)
        self.btn_save.configure(width=12, height=1, command=self.press_save_flag)
        self.btn_save.grid(column=2, row=0, padx=20, pady=10)

        ###Frame_Buttons_End###

        ##Frame_params###

        self.frame_param = tk.LabelFrame(
            self.master, text="Parameters", font=self.font_frame
        )
        self.frame_param.place(x=10, y=+10 + 100 + self.height_and_margin)
        self.frame_param.configure(width=max(self.width_and_margin, 570), height=150)
        self.frame_param.grid_propagate(False)

        # min Dist
        self.minDist_label = tk.Label(
            self.frame_param, text="min dist", font=self.font_frame
        )
        self.minDist_label.grid(column=0, row=0, padx=10, pady=10)

        self.minDist_number = tk.DoubleVar()
        self.minDist_number.set(self.mdist)
        self.minDist_var = ttk.Entry(
            self.frame_param, textvariable=self.minDist_number, width=5
        )
        self.minDist_var.grid(column=1, row=0, padx=10, pady=10)

        # param1
        self.param1_label = ttk.Label(
            self.frame_param, text="param1", font=self.font_frame
        )
        self.param1_label.grid(column=2, row=0, padx=10, pady=10)

        self.param1_number = tk.DoubleVar()
        self.param1_number.set(self.par1)
        self.param1_var = ttk.Entry(
            self.frame_param, textvariable=self.param1_number, width=5
        )
        self.param1_var.grid(column=3, row=0, padx=10, pady=10)

        # param2
        self.param2_label = ttk.Label(
            self.frame_param, text="param2", font=self.font_frame
        )
        self.param2_label.grid(column=4, row=0, padx=10, pady=10)

        self.param2_number = tk.DoubleVar()
        self.param2_number.set(self.par2)
        self.param2_var = ttk.Entry(
            self.frame_param, textvariable=self.param2_number, width=5
        )
        self.param2_var.grid(column=5, row=0, padx=10, pady=10)

        # change
        self.btn_change = tk.Button(
            self.frame_param, text="Change", font=self.font_btn_big
        )
        self.btn_change.configure(width=12, height=1, command=self.press_change)
        self.btn_change.grid(column=6, row=0, padx=10, pady=10)

        ##Frame_params_End###

    def update(self):
        # Get a frame from the video source
        ret, frame = self.vcap.read()

        self.second = time() - self.init_time

        if ret:
            self.frame_iterator += 1
            # キャリブレーション
            # mtx = npArray([[2.23429413e+03, 0.00000000e+00, 6.36470010e+02],
            #                 [0.00000000e+00, 2.31772325e+03, 5.74525725e+02],
            #                 [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])
            # _dist = npArray([[-0.77271385, -0.55940247, -0.00505415,  0.08305395,  1.77990709]])
            # wh = (1080, 1920)
            # newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, _dist, wh, 1, wh)
            # dst = cv2.undistort(frame, mtx, _dist, None, newcameramtx)

            # 圧縮
            # frame = frame[40:420, 100:540]
            frame = cv2.resize(
                frame, dsize=None, fx=0.5, fy=0.5, interpolation=cv2.INTER_LINEAR
            )
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # 線
            detect_line_y = [self.height // 10, self.height // 4]
            frame = cv2.line(
                frame,
                (0, detect_line_y[0]),
                (self.width, detect_line_y[0]),
                (255, 0, 0),
                thickness=3,
            )
            frame = cv2.line(
                frame,
                (0, detect_line_y[1]),
                (self.width, detect_line_y[1]),
                (0, 255, 0),
                thickness=3,
            )

            # 円検出
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
                    maxRadius=50,
                )
                if circles is None:
                    print("no detected, at", self.second)
                else:
                    # circles.sort(axis=1)
                    for circle in circles:
                        circle_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
                        for x, y, r in circle:
                            frame = cv2.circle(
                                frame,
                                (int(x), int(y)),
                                int(r),
                                circle_colors[
                                    0
                                    if y < detect_line_y[0]
                                    else 1
                                    if y < detect_line_y[1]
                                    else 2
                                ],
                                3,
                            )
                    # for circle in circles:
                    #     for x, y, r in circle:
                    #         frame = cv2.circle(frame, (int(x), int(y)), int(r), (255, 0, 0), 3)

                if self.save_flag:
                    write_list = [self.frame_iterator, self.second]
                    if circles is not None:
                        for circle in circles:
                            write_list += circle.flatten().tolist()
                    with open(self.csvfile, "a", newline="") as f:
                        writer_object = writer(f)
                        writer_object.writerow(write_list)
                        f.close()
            self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))

            # self.photo -> Canvas
            self.canvas1.create_image(0, 0, image=self.photo, anchor=tk.NW)
            self.master.after(self.delay, self.update)
        else:
            self.vcap.set(cv2.CAP_PROP_POS_FRAMES, 0)

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
    app = Application(master=root)  # Inherit
    app.mainloop()


if __name__ == "__main__":
    main()
