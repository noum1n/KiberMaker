from tkinter import Scale, messagebox
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import numpy as np
import datetime

# Массив для хранения загруженных изображений
images = []

# Переменная для хранения коллажа
collage = None

def load_data():
    images.clear()
    # Открываем диалоговое окно для выбора файлов
    file_paths = filedialog.askopenfilenames(filetypes=[("Images", "*.jpg *.jpeg *.png")])
    for file_path in file_paths:
        # Загружаем изображение с помощью библиотеки PIL
        image = Image.open(file_path)
        # Добавляем изображение в массив images
        images.append(image)

def generate_collage():
    global collage
    if len(images) == 0:
        return

    # Перемешиваем порядок имен изображений
    np.random.shuffle(images)
    # Получаем выбранное значение количества столбцов из слайдера
    cols = columns_slider.get()

    # Создаем коллаж из загруженных изображений
    num_images = len(images)
    rows = int(np.ceil(num_images / cols))

    # Добавляем размер рамки вокруг коллажа и между фотографиями
    border_size = border_slider.get()

    # Вычисляем размер каждого изображения в коллаже
    image_sizes = [(image.width, image.height) for image in images]
    min_width = min([size[0] for size in image_sizes])
    min_height = min([size[1] for size in image_sizes])
    image_width = min_width
    image_height = min_height

    # Создаем пустой холст для коллажа с белой рамкой
    collage_width = cols * (image_width + border_size) + border_size
    collage_height = rows * (image_height + border_size) + border_size
    collage = Image.new("RGB", (collage_width, collage_height), color="white")

    for i, image in enumerate(images):
        # Отрезаем центральную часть изображения
        left = (image.width - min_width) // 2
        top = (image.height - min_height) // 2
        right = left + min_width
        bottom = top + min_height
        cropped_image = image.crop((left, top, right, bottom))

        # Масштабируем отрезанную часть изображения до нужного размера
        if cropped_image.width > image_width or cropped_image.height > image_height:
            resized_image = cropped_image.resize((image_width, image_height), Image.LANCZOS)
        else:
            resized_image = cropped_image

        # Вычисляем координаты для размещения изображения на холсте
        row = i // cols
        col = i % cols
        x = col * (image_width + border_size) + border_size + (image_width - resized_image.width) // 2
        y = row * (image_height + border_size) + border_size + (image_height - resized_image.height) // 2

        # Размещаем изображение на холсте
        collage.paste(resized_image, (x, y))

    # Масштабируем метку для отображения коллажа под размеры окна программы
    window_width = window.winfo_screenwidth()
    window_height = window.winfo_screenheight()
    scale_factor = min(window_width / collage_width, window_height / collage_height)
    collage_width = int(collage_width * scale_factor)
    collage_height = int(collage_height * scale_factor)
    collage_resized = collage.resize((collage_width - 100, collage_height - 100), Image.LANCZOS)

    # Преобразуем масштабированный коллаж в объект ImageTk.PhotoImage
    collage_tk = ImageTk.PhotoImage(collage_resized)

    # Обновляем метку для отображения коллажа
    collage_label.configure(image=collage_tk)
    collage_label.image = collage_tk

def save_data():
    if len(images) == 0:
        messagebox.showwarning("Сохранение", "Нет загруженных изображений")
        return

    now = datetime.datetime.now()
    timestamp = now.strftime("%Y%m%d_%H%M")
    file_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG", "*.jpg")],
                                             initialfile=timestamp + ".jpg")

    if file_path:
        try:
            # Проверяем расширение файла
            if not file_path.lower().endswith(".jpg"):
                file_path += ".jpg"

            # Создаем копию коллажа для сохранения
            collage_copy = collage.copy()

            # Сохраняем коллаж в выбранном пути с заданным именем файла
            collage_copy.save(file_path)
            messagebox.showinfo("Сохранение", "Коллаж сохранен:\n" + file_path)
        except Exception as e:
            messagebox.showerror("Ошибка сохранения", str(e))

def close_program():
    window.destroy()

# Создаем графическое окно
window = tk.Tk()
window.title("Коллаж")
window.attributes("-fullscreen", True)

close_button = tk.Button(window, text="x", font=("Arial", 12, "bold"), command=close_program)
close_button.place(x=window.winfo_screenwidth() - 50, y=10, width=30, height=30)
close_button.bind("<Enter>", lambda event: close_button.config(bg="red"))
close_button.bind("<Leave>", lambda event: close_button.config(bg="SystemButtonFace"))

# Создаем кнопку "Загрузить" и привязываем функцию load_data к нажатию кнопки
load_button = tk.Button(window, text="Загрузить", command=load_data)
load_button.pack()

# Создаем кнопку "Сгенерировать" и привязываем функцию generate_collage к нажатию кнопки
generate_button = tk.Button(window, text="Сгенерировать", command=generate_collage)
generate_button.pack()

caption_label = tk.Label(window, text="количество столбцов:", font=("Arial", 10))
caption_label.pack()
# Создаем слайдер
columns_slider = Scale(window, from_=1, to=5, orient="horizontal", length=200)
columns_slider.pack()
caption_label = tk.Label(window, text="размер границы:", font=("Arial", 10))
caption_label.pack()


# Создаем слайдер для выбора ширины белой рамки
border_slider = Scale(window, from_=0, to=20, orient="horizontal", length=200)
border_slider.pack()

# Создаем кнопку "Сохранить" и привязываем функцию save_data к нажатию кнопки
save_button = tk.Button(window, text="Сохранить", command=save_data)
save_button.pack()

# Создаем метку для отображения коллажа
collage_label = tk.Label(window, bd=2, relief="groove")
collage_label.pack()

# Запускаем главный цикл окна
window.mainloop()
