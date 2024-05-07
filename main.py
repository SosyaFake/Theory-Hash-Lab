import tkinter as tk
from tkinter import ttk, messagebox, PhotoImage, filedialog
from PIL import Image, ImageTk
import webbrowser
import hashlib
import MD5


def spawn_window(root, window_width, window_height):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)

    root.geometry(f'{window_width}x{window_height}+{x}+{y}')


def on_select(event):
    print(event.widget.get())
    event.widget.selection_clear()


class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Main Window")
        self.root.iconbitmap('images/icons/icon.ico')
        # self.root.geometry('600x720')
        spawn_window(self.root, 600, 720)
        self.root.resizable(width=False, height=False)
        self.root.attributes('-fullscreen', False)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.image = PhotoImage(file='images/icons/icon.png')
        self.logo = ttk.Label(self.root, image=self.image)
        self.logo.pack(pady=5)

        self.about = ttk.Label(self.root, text="Эта программа поможет захэшировать текст/файл, а также поможет "
                                               "разобраться как работает хэширование.",
                               wraplength=300, style='Custom.TLabel', justify='center')
        self.about.pack(pady=5)

        self.hash_image = PhotoImage(file='images/icons/hash.png')
        self.hash_image = self.hash_image.subsample(3, 3)
        self.button_to_hash = ttk.Button(self.root, text="Хэширование",
                                         command=self.open_window1,
                                         image=self.hash_image, style='Custom.TButton', compound='left')
        self.button_to_hash.pack(pady=10)

        self.theory_image = PhotoImage(file='images/icons/theory.png')
        self.theory_image = self.theory_image.subsample(3, 3)
        self.button_to_theory = ttk.Button(self.root, text="Теория к хэшированию",
                                           command=self.open_window2,
                                           image=self.theory_image, style='Custom.TButton', compound='left')
        self.button_to_theory.pack(pady=10)

        self.telegram_image = PhotoImage(file='images/icons/telegram.png')
        self.telegram_image = self.telegram_image.subsample(3, 3)
        self.button_to_crypto_telegram = ttk.Button(self.root, text="Телеграм-бот с симметричным шифрованием",
                                                    command=self.open_telegram_bot,
                                                    image=self.telegram_image, style='Custom.TButton', compound='left')
        self.button_to_crypto_telegram.pack(pady=10)

        self.root.bind_all('<Control-c>', self.on_entry_copied)
        self.root.bind_all('<Control-v>', self.on_entry_pasted)

    @staticmethod
    def on_entry_copied(event):
        if isinstance(event.widget, ttk.Entry):
            event.widget.event_generate('<<Copy>>')

    @staticmethod
    def on_entry_pasted(event):
        if isinstance(event.widget, ttk.Entry):
            event.widget.event_generate('<<Paste>>')

    def open_window1(self):
        self.root.withdraw()
        Window1(self.root)

    def open_window2(self):
        self.root.withdraw()
        Window2(self.root)

    @staticmethod
    def open_telegram_bot():
        webbrowser.open('https://t.me/MEMREACryptographyBot')

    def on_closing(self):
        if tk.messagebox.askyesno("Выход", "Вы уверены, что хотите выйти?"):
            self.root.destroy()


class Window1:
    def __init__(self, root):
        self.root = tk.Toplevel(root)
        self.root.title("Window 1")
        self.root.iconbitmap('images/icons/icon.ico')

        spawn_window(self.root, 600, 600)
        self.root.resizable(width=False, height=False)
        self.root.attributes('-fullscreen', False)
        self.root.protocol("WM_DELETE_WINDOW", self.close_window)

        self.about = ttk.Label(self.root, text="Введите текст, который необходимо захэшировать.",
                               wraplength=600, style='Custom.TLabel', justify='center')
        self.about.pack()

        self.input_text = tk.StringVar()
        self.output_text = tk.StringVar()

        self.entry = ttk.Entry(self.root, width=50, textvariable=self.input_text, font=('TkDefaultFont', 14),
                               style='Custom.TEntry')
        self.entry.focus()
        self.entry.pack(pady=5)

        self.browse_button = ttk.Button(self.root, text="Обзор",
                                        command=self.open_file_dialog,
                                        style='Custom.TButton', compound='left')

        self.selected_option = tk.StringVar(value="text")

        self.text_radio = ttk.Radiobutton(self.root, text="Текст", value="text", style='Custom.TRadiobutton',
                                          variable=self.selected_option, command=self.on_select)
        self.text_radio.pack()

        self.file_radio = ttk.Radiobutton(self.root, text="Файл", value="file", style='Custom.TRadiobutton',
                                          variable=self.selected_option, command=self.on_select)
        self.file_radio.pack()

        self.options = ['MD5', 'SHA-1', 'SHA-256']
        self.options_hash = {'MD5': 'md5',
                             'SHA-1': 'sha1',
                             'SHA-256': 'sha256'}
        self.combo = ttk.Combobox(self.root, values=self.options, font=('TkDefaultFont', 14), style='Custom.TCombobox',
                                  state='readonly')
        # self.combo.bind("<<ComboboxSelected>>")
        self.combo.set(self.options[0])
        self.combo.pack(pady=20)

        self.output = ttk.Entry(self.root, width=50, textvariable=self.output_text, font=('TkDefaultFont', 14),
                                style='Custom.TEntry',
                                state='readonly')
        self.output.pack(pady=20)

        self.hash_button = ttk.Button(self.root, text="Захэшировать",
                                      command=self.hash,
                                      style='Custom.TButton', compound='left')
        self.hash_button.pack(pady=5)
        self.copy_button = ttk.Button(self.root, text="Скопировать хэш",
                                      command=self.copy_text,
                                      style='Custom.TButton', compound='left')
        self.copy_button.pack(pady=5)

        self.return_button = ttk.Button(self.root, text="Вернуться в главное меню",
                                        command=self.close_window,
                                        style='Custom.TButton', compound='left')
        self.return_button.pack(pady=35)

        self.entry.bind("<Button-3>", self.show_copy_menu)
        self.copy_menu = tk.Menu(self.root, tearoff=0)
        self.copy_menu.add_command(label="Копировать", command=self.copy_text)

    def close_window(self):
        if tk.messagebox.askyesno("Выход", "Вы уверены, что хотите вернуться в главное меню?"):
            self.root.destroy()
            root.deiconify()  # Показать основное окно снова

    def show_copy_menu(self, event):
        self.entry.focus()
        self.entry.selection_range(0, tk.END)
        self.copy_menu.post(event.x_root, event.y_root)

    def copy_text(self):
        text = self.output.get()
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        self.root.update()

    def on_select(self):
        if self.selected_option.get() == 'file':
            self.about.configure(text='Введите путь до файла, который необходимо захэшировать.')
            self.entry.configure(textvariable=self.input_text, state='readonly')
            self.browse_button.place(x=439, y=49)
            self.open_file_dialog()
        else:
            self.about.configure(text="Введите текст, который необходимо захэшировать.")
            self.input_text.set('')
            self.entry.configure(textvariable=self.input_text, state='normal')
            self.browse_button.place_forget()

    def open_file_dialog(self):
        path = filedialog.askopenfilename()
        if path:
            self.input_text.set(path)
            self.entry.configure(textvariable=self.input_text, state='readonly')

    def hash(self):
        h = hashlib.new(self.options_hash[self.combo.get()])
        if self.selected_option.get() == 'file':
            with open(self.entry.get(), 'rb') as file:
                while chunk := file.read(8192):
                    h.update(chunk)
            self.output_text.set(h.hexdigest())
        else:
            h.update(self.input_text.get().encode())
            self.output_text.set(h.hexdigest())


class Window2:
    def __init__(self, root):
        self.root = tk.Toplevel(root)
        self.root.title("Window 2")
        self.root.iconbitmap('images/icons/icon.ico')

        spawn_window(self.root, 1800, 895)
        self.root.resizable(width=False, height=False)
        self.root.attributes('-fullscreen', False)
        self.root.protocol("WM_DELETE_WINDOW", self.close_window)

        self.input_text = tk.StringVar()
        self.output_text = tk.StringVar()

        self.about = ttk.Label(self.root, text="Введите текст, который необходимо захэшировать.",
                               wraplength=600, style='Custom.TLabel', justify='center')
        self.about.pack()

        self.entry = ttk.Entry(self.root, width=50, textvariable=self.input_text, font=('TkDefaultFont', 14),
                               style='Custom.TEntry')
        self.entry.focus()
        self.entry.pack(pady=5)

        self.image_path = f"images/MD5/MD5.png"

        # Загружаем изображение
        self.image = Image.open(self.image_path)
        self.image = self.image.resize((600, 600))
        self.image = ImageTk.PhotoImage(self.image)

        # Отображаем изображение на вкладке
        self.labelMD5 = tk.Label(self.root, image=self.image)
        self.labelMD5.image = self.image  # сохраняем ссылку на изображение
        self.labelMD5.pack(pady=5)

        self.output = ttk.Entry(self.root, width=50, textvariable=self.output_text, font=('TkDefaultFont', 14),
                                style='Custom.TEntry',
                                state='readonly')
        self.output.pack(pady=5)

        self.hash_button = ttk.Button(self.root, text="Захэшировать",
                                      command=self.hash,
                                      style='Custom.TButton', compound='left')
        self.hash_button.pack(pady=5)

        self.return_button = ttk.Button(self.root, text="Вернуться в главное меню",
                                        command=self.close_window,
                                        style='Custom.TButton', compound='left')
        self.return_button.pack()

        self.labels = None
        self.buttons = None

        self.label_block = ttk.Label(self.root, width=19, justify='right', font=('TkDefaultFont', 17), anchor='e',
                                     wraplength=250,
                                     relief='solid')
        self.label_message = ttk.Label(self.root, width=30, justify='left', font=('TkDefaultFont', 17), anchor='w',
                                       wraplength=550,
                                       relief='solid')
        self.label_constant = ttk.Label(self.root, width=9, justify='center', font=('TkDefaultFont', 17),
                                        anchor='center', relief='solid', wraplength=550)

        self.label_upper_A = ttk.Label(self.root, width=9, justify='center', font=('TkDefaultFont', 17),
                                       anchor='center', background="#49d8ff")
        self.label_upper_B = ttk.Label(self.root, width=9, justify='center', font=('TkDefaultFont', 17),
                                       anchor='center', background="#49d8ff")
        self.label_upper_C = ttk.Label(self.root, width=9, justify='center', font=('TkDefaultFont', 17),
                                       anchor='center', background="#49d8ff")
        self.label_upper_D = ttk.Label(self.root, width=9, justify='center', font=('TkDefaultFont', 17),
                                       anchor='center', background="#49d8ff")

        self.label_down_A = ttk.Label(self.root, width=9, justify='center', font=('TkDefaultFont', 17), anchor='center',
                                      background="#49d8ff")
        self.label_down_B = ttk.Label(self.root, width=9, justify='center', font=('TkDefaultFont', 17), anchor='center',
                                      background="#49d8ff")
        self.label_down_C = ttk.Label(self.root, width=9, justify='center', font=('TkDefaultFont', 17), anchor='center',
                                      background="#49d8ff")
        self.label_down_D = ttk.Label(self.root, width=9, justify='center', font=('TkDefaultFont', 17), anchor='center',
                                      background="#49d8ff")

        self.label_rotate = ttk.Label(self.root, width=5, justify='center', font=('TkDefaultFont', 17), anchor='center',
                                      background='#ffe61d')

        self.label_function = ttk.Label(self.root, width=4, justify='center', font=('TkDefaultFont', 17),
                                        anchor='center', background='#74da00')

        self.iteration_button = ttk.Button(self.root, text="Итерация ->",
                                           style='Custom.TButton', compound='left')
        self.round_button = ttk.Button(self.root, text="Раунд ->",
                                           style='Custom.TButton', compound='left')
        self.block_button = ttk.Button(self.root, text="Блок ->",
                                           style='Custom.TButton', compound='left')



    def hash(self):
        self.image_path = f"images/MD5/MD5-fix.png"
        self.image = Image.open(self.image_path)
        self.image = self.image.resize((600, 600))
        self.image = ImageTk.PhotoImage(self.image)
        self.labelMD5.configure(image=self.image)
        self.labelMD5.image = self.image

        self.label_block.place(x=332, y=142)
        self.label_constant.place(x=458, y=368)
        self.label_message.place(x=1217, y=142)

        self.label_upper_A.place(x=644, y=123)
        self.label_upper_B.place(x=785, y=123)
        self.label_upper_C.place(x=926, y=123)
        self.label_upper_D.place(x=1067, y=123)

        self.label_down_A.place(x=644, y=663)
        self.label_down_B.place(x=785, y=663)
        self.label_down_C.place(x=926, y=663)
        self.label_down_D.place(x=1067, y=663)

        self.label_rotate.place(x=663, y=439)

        self.label_function.place(x=772, y=223)

        self.labels = [self.label_block, self.label_constant, self.label_message,
                       self.label_upper_A, self.label_upper_B, self.label_upper_C, self.label_upper_D,
                       self.label_down_A, self.label_down_B, self.label_down_C, self.label_down_D,
                       self.label_rotate, self.label_function]

        self.block_button.place(x=28, y=721)
        self.round_button.place(x=205, y=721)
        self.iteration_button.place(x=382, y=721)

        self.buttons = [self.block_button, self.round_button, self.iteration_button]

        MD5.md5(self.entry.get(), self.labels, self.buttons, self.output, self.output_text)

    def copy_text(self):
        text = self.output.get()
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        self.root.update()

    def close_window(self):
        if tk.messagebox.askyesno("Выход", "Вы уверены, что хотите вернуться в главное меню?"):
            self.root.destroy()
            root.deiconify()  # Показать основное окно снова


if __name__ == '__main__':
    root = tk.Tk()
    style = ttk.Style()
    style.configure('Custom.TButton', font=('TkDefaultFont', 14), padding=10, anchor='center')
    style.configure('Custom.TLabel', font=('TkDefaultFont', 14), padding=10, anchor='center')
    style.configure('Custom.TEntry', font=('TkDefaultFont', 14), padding=10, anchor='center')
    style.configure('Custom.TCombobox', font=('TkDefaultFont', 14), padding=10, anchor='center')
    style.configure('Custom.TRadiobutton', font=('TkDefaultFont', 14), padding=10, anchor='center')
    app = MainWindow(root)
    root.mainloop()
