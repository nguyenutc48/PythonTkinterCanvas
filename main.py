import tkinter as tk
import random
import threading
import time
import serial
import io

default_rectangle = 100
default_port = '/dev/ttyUSB0'


# Hàm để vẽ hình chữ nhật trên canvas
def draw_rectangle(canvas, width, height,error_text=""):
    #center_x = canvas.winfo_width() / 2
    #center_y = canvas.winfo_height() / 2
    canvas.create_rectangle(center_screen_x - width / 2, center_screen_y - height / 2,
                            center_screen_x + width / 2, center_screen_y + height / 2,
                            outline="white", width=2, fill="black")
    canvas.create_text(center_screen_x, 50, text=f"Chiều dài: {width}, Chiều rộng: {height}", fill="white", font=("Helvetica", 16))
    canvas.create_text(center_screen_x, center_screen_y*2-50, text=error_text, fill="red", font=("Helvetica", 16))

# Hàm cập nhật hình chữ nhật
def update_rectangle(canvas):
    isOpened = False
    ser = None
    while True:
        try:
            if isOpened == False:
                ser = serial.Serial(default_port, 9600, timeout=1)
                canvas.delete("all")
                draw_rectangle(canvas,default_rectangle,default_rectangle,"Connected")
                canvas.update()
                isOpened = True
            data = ser.readline()
            try:
                data = data.decode('utf-8',errors='ignore').strip()
                print(data)
                if data:
                    try:   
                        width, height = map(int,data.split(','))#get_random_data_from_com()
                        canvas.delete("all")
                        draw_rectangle(canvas, width, height,"")
                        canvas.update()  # Cập nhật canvas
                        #time.sleep(1)  # Đợi 1 giây trước khi cập nhật lại
                    except ValueError:
                        print("Du lieu khong hop le: ", data)
            except UnicodeDecodeError:
                print("Du lieu khong ma hoa duoc: ", data)
   
            send_data = str(random.randint(100, 300))+","+str(random.randint(100, 300))+"\n"
            print(send_data)
            ser.write(send_data.encode())
            ser.flush()
            
        except serial.SerialException:
            if isOpened == True:
                ser.close()
                canvas.delete("all")
                draw_rectangle(canvas,default_rectangle,default_rectangle,"Disconnected")
                canvas.update()
                isOpened = False
            print("Loi cong COM")
            time.sleep(1)
            
            

# Hàm lấy dữ liệu ngẫu nhiên từ cổng COM
def get_random_data_from_com():
    # Đoạn code để nhận dữ liệu từ cổng COM ở đây
    # Trả về width và height ngẫu nhiên cho mục đích minh họa
    return random.randint(100, 300), random.randint(100, 300)

# Tạo giao diện fullscreen với nền màu đen
root = tk.Tk()
root.attributes("-fullscreen", True)  # Thiết lập fullscreen
root.configure(bg='black', cursor='none')  # Thiết lập màu nền đen
root.title("App")

center_screen_x = root.winfo_screenwidth() / 2
center_screen_y = root.winfo_screenheight() / 2

center_screen_mmx = root.winfo_screenmmwidth() / 2
center_screen_mmy = root.winfo_screenmmheight() / 2

canvas = tk.Canvas(root, bg='black')
canvas.pack(fill=tk.BOTH, expand=True)
canvas.delete("all")
draw_rectangle(canvas,default_rectangle,default_rectangle)
canvas.update()  # Cập nhật canvas

# Tạo luồng riêng biệt để cập nhật hình chữ nhật
update_thread = threading.Thread(target=update_rectangle, args=(canvas,))
update_thread.daemon = True
update_thread.start()

root.mainloop()