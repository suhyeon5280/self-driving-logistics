import tkinter as tk
from playsound import playsound
import os
from threading import Thread
import subprocess
import json

class RobotInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("로봇 인터페이스")
        self.root.geometry("1500x700")

        # 소리 파일 경로
        self.sounds = {
            "recog": r"",
            "schedule": r"",
            "talking": r"",
            "logout": r""
        }

        # 캔버스 설정
        self.canvas = tk.Canvas(root, width=1500, height=700, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # 로봇 얼굴의 위치와
        face_center_x = 750
        face_center_y = 350
        mouth_width = 300
        mouth_height = 50

        self.left_eye = self.canvas.create_oval(face_center_x - 250, face_center_y - 150,
                                                face_center_x - 150, face_center_y - 50, fill="black")
        self.right_eye = self.canvas.create_oval(face_center_x + 150, face_center_y - 150,
                                                 face_center_x + 250, face_center_y - 50, fill="black")

        self.mouth = self.canvas.create_rectangle(face_center_x - mouth_width // 2, face_center_y + 50,
                                                  face_center_x + mouth_width // 2, face_center_y + 50 + mouth_height,
                                                  fill="black")

        self.create_buttons()

        self.recognition = 0

    def create_buttons(self):
        # 버튼을 위한 프레임 설정
        button_frame = tk.Frame(self.root)
        button_frame.place(relx=0.5, rely=0.9, anchor="center")

        # 버튼 목록 설정
        menu = [("Recognition", "recog"), ("Schedule", "schedule"), ("Talking", "talking"), ("Logout", "logout")]

        button_frame.grid_columnconfigure(tuple(range(len(menu))), weight=1)

        for i, (text, menu_item) in enumerate(menu):
            button = tk.Button(button_frame, text=text, command=lambda e=menu_item: self.set_menu(e), width=20, height=2)
            button.grid(row=0, column=i, padx=10)

    def play_sound(self, sound_file):
        if os.path.exists(sound_file):
            playsound(sound_file)
        else:
            print(f"소리 파일을 찾을 수 없습니다: {sound_file}")

    def set_menu(self, menu):
        if menu in self.sounds:
            self.play_sound(self.sounds[menu])

        if menu == "recog":
            self.run_external_script1()
            if self.recognition == 1:
                self.talk()
                self.play_sound(r" ")
            else:
                self.talk()
                self.play_sound(r"")

        elif menu == "schedule":
            if self.recognition == 1:
                self.talk()
                self.run_external_script2()
            else:
                self.talk()
                self.play_sound(r"")

        elif menu == "talking":
            self.talk()
            print("Talking 기능입니다.")

        elif menu == "logout":
            self.talk()
            print("Logout 기능입니다.")
            self.recognition = 0

    def run_external_script1(self):
        try:
            result = subprocess.run(["python3", r".py"], capture_output=True, text=True)
            # 스크립트 실행 후 출력 값을 읽어 recognition 값을 설정합니다.
            if "1" in result.stdout:
                self.recognition = 1
            else:
                self.recognition = 0
        except Exception as e:
            print(f"스크립트를 실행하는 중 오류 발생: {e}")

    def run_external_script2(self):
        try:
            result = subprocess.run(["python3", r"C:.py"], capture_output=True, text=True)
            # 스크립트 실행 후 출력된 JSON 데이터를 파싱하여 딕셔너리로 변환
            output_dict = json.loads(result.stdout)
            self.display_dictionary(output_dict)
        except Exception as e:
            print(f"스크립트를 실행하는 중 오류 발생: {e}")

    def display_dictionary(self, data):
        # 딕셔너리를 캔버스에 텍스트로 출력
        display_text = ""
        for key, value in data.items():
            display_text += f"{key}: {value}\n"
        
        self.canvas.create_text(750, 350, text=display_text, anchor="center", font=("Helvetica", 16))

    def talk(self):
        # 간단한 말하기 애니메이션: 입 모양이 네모로 뻐끔뻐끔
        self.canvas.coords(self.mouth, 650, 400, 850, 450)  # 기본 네모
        self.canvas.after(200, lambda: self.canvas.coords(self.mouth, 650, 380, 850, 480))  # 네모 크게
        self.canvas.after(400, lambda: self.canvas.coords(self.mouth, 650, 400, 850, 450))  # 기본 네모
        self.canvas.after(600, lambda: self.canvas.coords(self.mouth, 650, 420, 850, 430))  # 네모 작게
        self.canvas.after(800, lambda: self.canvas.coords(self.mouth, 650, 400, 850, 450))  # 기본 네모로 복귀

# 메인 루프 실행
root = tk.Tk()
app = RobotInterface(root)
root.mainloop()


