import tkinter as tk
import random
import threading
import time
#import serial
import io
from pymodbus.client.sync import ModbusSerialClient as ModbusClient

default_rectangle = 100
default_port = '/dev/ttyUSB0'


# Hàm để vẽ hình chữ nhật trên canvas
def draw_rectangle(canvas, width, height, error_text=""):
    #center_x = canvas.winfo_width() / 2
    #center_y = canvas.winfo_height() / 2
    canvas.create_rectangle(center_screen_x - width / 2, center_screen_y - height / 2,
                            center_screen_x + width / 2, center_screen_y + height / 2,
                            outline="white", width=2, fill="black")
    canvas.create_text(center_screen_x, center_screen_y*2-100, text=f"X: {center_screen_x-width} - Chiều dài: {width}, Y: {center_screen_y - height} - Chiều rộng: {height}", fill="white", font=("Helvetica", 36))
    canvas.create_text(center_screen_x, center_screen_y*2-50, text=error_text, fill="red", font=("Helvetica", 18))

# Hàm cập nhật hình chữ nhật
def update_rectangle(canvas):
    isOpened = False
    ser = None
    width = 0
    height = 0
    while True:
        try:
            
            # Khởi tạo đối tượng ModbusClient với địa chỉ slave và cổng COM (hoặc USB)
            client = ModbusClient(method='rtu', port='/dev/ttyUSB0', baudrate=9600, stopbits=1, bytesize=8, parity='N', timeout=1)

            # Kết nối với thiết bị
            client.connect()

            # Đọc giá trị từ thanh ghi (Register) của thiết bị
            register_address = 0  # Thay đổi địa chỉ register tương ứng với thiết bị của bạn
            number_of_registers = 2  # Số lượng thanh ghi cần đọc

            # Đọc giá trị từ thanh ghi
            result = client.read_holding_registers(register_address, number_of_registers, unit=1)  # Thay đổi địa chỉ slave tương ứng với thiết bị của bạn

            if result.isError():
                print("Đọc lỗi: ", result)
            else:
                print("Giá trị đọc được: ", result.registers )
                #width, height = map(int,data.split(','))#get_random_data_from_com()
                if width != result.registers[0] and height != result.registers[1]:
                    width = result.registers[0]
                    height = result.registers[1]
                    canvas.delete("all")
                    draw_rectangle(canvas, round(width,2), round(height,2),"")
                    canvas.update()  # Cập nhật canvas
            client.close()
        except:
            canvas.delete("all")
            draw_rectangle(canvas,default_rectangle,default_rectangle,"Can not connect to COM port")
            canvas.update()
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
root.title("App Modbus")

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
