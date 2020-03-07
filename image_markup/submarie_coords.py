# Изображения для разметки нужно положить в папку "in"
# Размеченные будут переносится в "out", файл с координатами - там же
import os
from tkinter import Tk, Canvas, Button, Frame, LEFT
from PIL import ImageTk, Image
from tkinter import ttk

# Устанавливаем пути
cwd = os.getcwd()
input_path = os.path.sep.join([cwd,"in"])
output_path = os.path.sep.join([cwd,"out"])
os.makedirs(output_path, exist_ok=True)

# Список имён файлов для разметки
pic_list = os.listdir(input_path)

pic_cur = "" # Имя текущего файла
img = ""     # Объект изображения в Canvas
frame_xy = [0, 0, 0, 0]
frame = ""
h_crop = 1
w_crop = 1
canvas_width = 800
canvas_height = 800

# ***************************** ROOT *****************************
root = Tk()
root.title("image markup")
root.geometry('1000x1000')

# ***************************** CANVAS *****************************
c = Canvas(root, width=canvas_width, height=canvas_height)
c.focus_set()

def next_image(event=1):
    global pic_cur, pic_list, img, input_path, frame_xy, image, frame, w_crop, h_crop

    # Если выбрано изображение (и оно на экране 0_o)
    if pic_cur:
        # убираем его
        c.delete(img)
        # переносим файл с картинкой в папку out
        pic_input_path = os.path.sep.join([input_path, pic_cur])
        pic_out_path = os.path.sep.join([output_path, pic_cur])
        os.rename(pic_input_path, pic_out_path)
        # открываем файл с метками на дозапись
        labels_path = os.path.sep.join([output_path, "labels.txt"])
        with open(labels_path, "a") as f:
            # имя картинки
            f.write(f"{pic_cur},")
            # масштабируем рамку
            crop_coord = []
            crop_coord.append(frame_xy[0] * w_crop)
            crop_coord.append(frame_xy[1] * h_crop)
            crop_coord.append(frame_xy[2] * w_crop)
            crop_coord.append(frame_xy[3] * h_crop)
            # дописываем координаты в файл, завершаем строку
            f.write("{},{},{},{}\n".format(*crop_coord))
        # сбрасываем выбранную картинку
        pic_cur = ""
        # TODO: canvas del all
        c.delete(img)
        c.delete(frame)

    # Еслив списке есть картинки
    if pic_list:
        # Достаём одну
        pic_cur = pic_list.pop()
        pic_path = os.path.sep.join([input_path, pic_cur])
        pilImage = Image.open(pic_path)

        # картинки отображаются на экране не в полный размер
        # вычисляем отношения реальных высоты и ширины к отображаемым
        # чтобы потом масштабировать рамку
        h_crop = pilImage.height / canvas_height
        w_crop = pilImage.width / canvas_width
        print(h_crop, w_crop)
        # ресайзим картинку до размеров холста
        pilImage = pilImage.resize((canvas_width, canvas_height))
        # конвертим в подходящий для Tk формат
        image = ImageTk.PhotoImage(pilImage)
        #отображаем на холсте
        img = c.create_image(0, 0, image=image, anchor="nw")
        # добавляем рамку
        frame = c.create_rectangle(*frame_xy, outline="green", width=3)

next_pic = ttk.Button(text="Next", command=next_image)
root.bind("<space>", next_image)

# ****************************** Mouse Motion ************************************
def frame_res_l (event):
    global frame_xy
    # TODO: eventxy - ?
    frame_xy[0], frame_xy[1] = [event.x, event.y]
    c.coords(frame, *frame_xy)

def frame_res_r (event):
    global frame_xy
    frame_xy[2], frame_xy[3] = [event.x, event.y]
    c.coords(frame, *frame_xy)

c.bind("<B1-Motion>", frame_res_l)
c.bind("<Button-1>", frame_res_l)
c.bind("<B3-Motion>", frame_res_r)
c.bind("<Button-3>", frame_res_r)

c.pack()
next_pic.pack()

root.mainloop()