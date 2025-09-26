import tkinter as tk
from tkinter import messagebox, ttk
import random
import time

TEXT_RU = [
    "Программирование — искусство создания логики из хаоса.",
    "Технологии меняют мир, но люди остаются прежними.",
    "Каждый день — новая возможность стать лучше.",
    "Практика ведёт к совершенству, особенно в программировании.",
    "Информация — сила, а знания — путь к свободе."
]
TEXT_ENG = [
    "Programming is the art of creating logic from chaos.",
    "Technology changes the world, but people remain the same.",
    "Every day is a new chance to become better.",
    "Practice leads to perfection, especially in programming.",
    "Information is power, and knowledge is the path to freedom."
]

WORD_RU = ["яблоко", "стол", "дверь", "книга", "ручка", "свет", "мышь", "ноутбук", "программа", "код"]
WORD_ENG = ["apple", "table", "door", "book", "pen", "light", "mouse", "laptop", "program", "code"]


class LoadingScreen:
    def __init__(self, root, on_start):
        self.root = root
        self.on_start = on_start
        self.root.title("Клавиатурный тренажер")
        self.root.geometry("900x550")
        self.root.resizable(False, False)
        self.canvas = tk.Canvas(root, width=900, height=550)
        self.canvas.pack()
        self.canvas.create_text(450, 150, text="Клавиатурный тренажёр", font=("Arial", 36, "bold"), fill="black")
        self.start_button = tk.Button(
            root,
            text="НАЧАТЬ",
            font=("Arial", 18),
            width=20,
            bg="#007acc",
            fg="white",
            command=self.start_app
        )
        self.start_button_window = self.canvas.create_window(450, 300, window=self.start_button)
        self.quit_button = tk.Button(
            root,
            text="ВЫЙТИ",
            font=("Arial", 18),
            width=20,
            bg="#f44336",
            fg="white",
            command=root.destroy
        )
        self.quit_button_window = self.canvas.create_window(450, 370, window=self.quit_button)

    def start_app(self):
        self.canvas.destroy()
        self.start_button.destroy()
        self.quit_button.destroy()
        self.on_start()


class KeyboardTrainer:
    def __init__(self, root):
        self.root = root
        self.root.title("Клавиатурный тренажёр")
        self.root.geometry("900x550")
        self.root.configure(bg="#1e1e1e")
        self.root.resizable(True, True)

        self.bg_color = "#1e1e1e"
        self.fg_color = "#ffffff"
        self.accent_color = "#007acc"
        self.correct_color = "#4caf50"
        self.incorrect_color = "#f44336"
        self.cursor_color = "#00ffff"

        self.target_text = ""
        self.error_count = 0
        self.start_time = None
        self.current_language = "RU"
        self.current_mode = "words_10"

        self.top_frame = tk.Frame(root, bg=self.bg_color)
        self.top_frame.pack(pady=15)

        self.ru_button = tk.Button(self.top_frame, text="RU", width=5,
                                   command=lambda: self.set_language("RU"),
                                   bg=self.accent_color, fg=self.fg_color, font=("Arial", 12))
        self.ru_button.pack(side='left', padx=5)
        self.eng_button = tk.Button(self.top_frame, text="ENG", width=5,
                                    command=lambda: self.set_language("ENG"),
                                    bg=self.accent_color, fg=self.fg_color, font=("Arial", 12))
        self.eng_button.pack(side='left', padx=5)

        self.quotes_button = tk.Button(self.top_frame, text="Цитаты", width=10,
                                       command=self.load_quote,
                                       bg=self.accent_color, fg=self.fg_color, font=("Arial", 12))
        self.quotes_button.pack(side='left', padx=5)

        self.words_button = tk.Button(self.top_frame, text="Слова", width=10,
                                      command=self.show_word_options,
                                      bg=self.accent_color, fg=self.fg_color, font=("Arial", 12))
        self.words_button.pack(side='left', padx=5)

        self.word_buttons_frame = tk.Frame(root, bg=self.bg_color)
        self.word_buttons = []

        self.text_frame = tk.Frame(root, bg=self.bg_color)
        self.text_frame.pack(pady=20)
        self.text_widget = None

        self.entry = tk.Entry(root, font=("Consolas", 18), width=60, justify="center",
                              bg="#2d2d2d", fg=self.fg_color, insertbackground=self.fg_color)
        self.entry.pack(pady=15)
        self.entry.bind("<KeyRelease>", self.check_input)
        self.entry.config(state='disabled')
        self.entry.focus_set()

        self.button_frame = tk.Frame(root, bg=self.bg_color)
        self.button_frame.pack(pady=10)

        self.restart_button = tk.Button(self.button_frame, text="Попробовать снова",
                                        command=self.restart_test, state='normal', width=20,
                                        bg=self.accent_color, fg=self.fg_color, font=("Arial", 12))
        self.restart_button.pack(side='left', padx=5)

        self.quit_button = tk.Button(self.button_frame, text="Закончить",
                                     command=self.root.destroy, width=20,
                                     bg=self.accent_color, fg=self.fg_color, font=("Arial", 12))
        self.quit_button.pack(side='left', padx=5)

        self.set_language("RU")
        self.show_word_options()

    def set_language(self, lang):
        self.current_language = lang
        self.ru_button.config(relief=tk.SUNKEN if lang == "RU" else tk.RAISED)
        self.eng_button.config(relief=tk.SUNKEN if lang == "ENG" else tk.RAISED)
        if self.current_mode == "quotes":
            self.load_quote()
        elif self.current_mode.startswith("words"):
            count = int(self.current_mode.split('_')[1])
            self.generate_words(count)

    def generate_words(self, count):
        self.current_mode = f"words_{count}"
        bank = WORD_RU if self.current_language == "RU" else WORD_ENG
        words = [random.choice(bank) for _ in range(count)]
        self.target_text = " ".join(words)
        self.generate_display()

    def generate_display(self):
        if hasattr(self, 'text_widget') and self.text_widget:
            self.text_widget.destroy()
        self.text_widget = tk.Text(
            self.text_frame,
            font=("Consolas", 18),
            height=4,
            width=60,
            wrap='word',
            bg=self.bg_color,
            fg=self.fg_color,
            bd=0,
            highlightthickness=0,
            state='disabled'
        )
        self.text_widget.pack()
        self.text_widget.tag_configure("correct", foreground=self.correct_color)
        self.text_widget.tag_configure("incorrect", foreground=self.incorrect_color)
        self.text_widget.tag_configure("default", foreground=self.fg_color)

        self.text_widget.config(state='normal')
        self.text_widget.delete("1.0", tk.END)
        self.text_widget.insert("1.0", self.target_text)
        self.text_widget.config(state='disabled')

        self.entry.config(state='normal')
        self.entry.delete(0, tk.END)
        self.entry.focus_set()
        self.start_time = None
        self.error_count = 0

    def check_input(self, event):
        if self.start_time is None:
            self.start_time = time.time()

        user_input = self.entry.get()
        target = self.target_text

        if len(user_input) > len(target):
            self.entry.delete(len(target), tk.END)
            return
        self.text_widget.config(state='normal')
        self.text_widget.delete("1.0", tk.END)
        self.error_count = 0
        for i in range(len(target)):
            char = target[i]
            if i < len(user_input):
                if user_input[i] == char:
                    self.text_widget.insert(tk.END, char, "correct")
                else:
                    self.text_widget.insert(tk.END, char, "incorrect")
                    self.error_count += 1
            else:
                self.text_widget.insert(tk.END, char, "default")

        self.text_widget.config(state='disabled')

        if len(user_input) >= len(target):
            elapsed_time = max(1, int(time.time() - self.start_time))
            speed = len(user_input) / (elapsed_time / 60)
            self.entry.config(state='disabled')
            messagebox.showinfo("Завершено!", f"Вы успешно завершили тест!\n"
                                              f"Время: {elapsed_time} сек\n"
                                              f"Ошибки: {self.error_count}\n"
                                              f"Скорость: {int(speed)} знаков/мин")

    def show_word_options(self):
        self.hide_all_mode_buttons()
        for btn in self.word_buttons:
            btn.destroy()
        self.word_buttons.clear()
        counts = [10, 25, 50]
        for count in counts:
            btn = tk.Button(self.word_buttons_frame, text=str(count), width=5,
                            command=lambda c=count: self.generate_words(c),
                            bg=self.accent_color, fg=self.fg_color, font=("Arial", 12))
            btn.pack(side='left', padx=5)
            self.word_buttons.append(btn)
        self.word_buttons_frame.pack(after=self.words_button, pady=5)
        self.generate_words(10)

    def hide_all_mode_buttons(self):
        self.word_buttons_frame.pack_forget()

    def load_quote(self):
        self.hide_all_mode_buttons()
        self.current_mode = "quotes"
        bank = TEXT_RU if self.current_language == "RU" else TEXT_ENG
        self.target_text = random.choice(bank)
        self.generate_display()

    def restart_test(self):
        if self.current_mode == "quotes":
            self.load_quote()
        elif self.current_mode.startswith("words"):
            count = int(self.current_mode.split('_')[1])
            self.generate_words(count)


if __name__ == "__main__":
    root = tk.Tk()
    def start_main_app():
        app = KeyboardTrainer(root)
    splash = LoadingScreen(root, start_main_app)
    root.mainloop()