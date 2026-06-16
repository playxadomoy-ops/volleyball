import tkinter as tk
from tkinter import messagebox


class VolleyballScoreboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Волейбольне табло")
        self.root.geometry("500x500")  # Трохи збільшено висоту для нових кнопок
        self.root.resizable(False, False)

        # Початковий стан гри
        self.score_a = 0
        self.score_b = 0
        self.sets_a = 0
        self.sets_b = 0
        self.current_set = 1
        self.game_over = False

        # Історія для функції скасування дії (Undo)
        self.history = []

        self.create_widgets()
        self.update_display()

    def create_widgets(self):
        # Назва турніру / Заголовок
        self.title_label = tk.Label(self.root, text="МАТЧ З ВОЛЕЙБОЛУ", font=("Arial", 16, "bold"), fg="navy")
        self.title_label.pack(pady=10)

        # Рахунок за партіями (Сети)
        self.sets_label = tk.Label(self.root, text="Партії: 0 : 0", font=("Arial", 14, "bold"), fg="darkgreen")
        self.sets_label.pack(pady=5)

        # Номер поточної партії
        self.set_number_label = tk.Label(self.root, text="Партія 1", font=("Arial", 11, "italic"))
        self.set_number_label.pack()

        # Головний фрейм для кнопок керування рахунком
        self.buttons_frame = tk.Frame(self.root)
        self.buttons_frame.pack(pady=15)

        # --- БЛОК КОМАНДИ А ---
        self.frame_team_a = tk.Frame(self.buttons_frame)
        self.frame_team_a.grid(row=0, column=0, padx=20)

        # Велика кнопка +1 бал Команді А
        self.btn_a = tk.Button(
            self.frame_team_a,
            text="Команда А\n0",
            font=("Arial", 18, "bold"),
            bg="lightblue",
            width=12,
            height=3,
            command=lambda: self.add_point("A")
        )
        self.btn_a.pack()

        # Маленька кнопка -1 бал Команді А
        self.btn_minus_a = tk.Button(
            self.frame_team_a,
            text="-1 бал",
            font=("Arial", 10, "bold"),
            bg="#d0e1f9",
            fg="red",
            width=10,
            command=lambda: self.minus_point("A")
        )
        self.btn_minus_a.pack(pady=5)

        # --- БЛОК КОМАНДИ Б ---
        self.frame_team_b = tk.Frame(self.buttons_frame)
        self.frame_team_b.grid(row=0, column=1, padx=20)

        # Велика кнопка +1 бал Команді Б
        self.btn_b = tk.Button(
            self.frame_team_b,
            text="Команда Б\n0",
            font=("Arial", 18, "bold"),
            bg="lightcoral",
            width=12,
            height=3,
            command=lambda: self.add_point("B")
        )
        self.btn_b.pack()

        # Маленька кнопка -1 бал Команді Б
        self.btn_minus_b = tk.Button(
            self.frame_team_b,
            text="-1 бал",
            font=("Arial", 10, "bold"),
            bg="#f9d5d5",
            fg="red",
            width=10,
            command=lambda: self.minus_point("B")
        )
        self.btn_minus_b.pack(pady=5)

        # Фрейм для загального керування (Undo, Скидання)
        self.control_frame = tk.Frame(self.root)
        self.control_frame.pack(pady=20)

        # Кнопка скасування дії
        self.btn_undo = tk.Button(
            self.control_frame,
            text="↩ Скасувати дію",
            font=("Arial", 11),
            command=self.undo
        )
        self.btn_undo.grid(row=0, column=0, padx=10)

        # Кнопка нового матчу
        self.btn_reset = tk.Button(
            self.control_frame,
            text="🔄 Новий матч",
            font=("Arial", 11),
            bg="lightgray",
            command=self.reset_match
        )
        self.btn_reset.grid(row=0, column=1, padx=10)

    def save_state(self):
        """Зберігає поточний стан гри в історію перед зміною."""
        state = (self.score_a, self.score_b, self.sets_a, self.sets_b, self.current_set, self.game_over)
        self.history.append(state)

    def add_point(self, team):
        """Додає бал обраній команді."""
        if self.game_over:
            return

        self.save_state()

        if team == "A":
            self.score_a += 1
        elif team == "B":
            self.score_b += 1

        self.check_set_winner()
        self.update_display()

    def minus_point(self, team):
        """Віднімає бал у обраної команди (не нижче 0)."""
        if self.game_over:
            return

        # Перевірка, чи є взагалі що віднімати
        if team == "A" and self.score_a == 0:
            return
        if team == "B" and self.score_b == 0:
            return

        self.save_state()

        if team == "A":
            self.score_a -= 1
        elif team == "B":
            self.score_b -= 1

        self.update_display()

    def check_set_winner(self):
        """Перевіряє умови перемоги в партії чи матчі."""
        target_score = 15 if self.current_set == 5 else 25

        if self.score_a >= target_score and (self.score_a - self.score_b) >= 2:
            self.sets_a += 1
            self.next_set()
        elif self.score_b >= target_score and (self.score_b - self.score_a) >= 2:
            self.sets_b += 1
            self.next_set()

    def next_set(self):
        """Переводить гру на наступну партію або завершує матч."""
        if self.sets_a == 3:
            self.game_over = True
            self.update_display()
            messagebox.showinfo("Матч завершено", "Вітаємо! Команда А перемогла у матчі!")
            return
        elif self.sets_b == 3:
            self.game_over = True
            self.update_display()
            messagebox.showinfo("Матч завершено", "Вітаємо! Команда Б перемогла у матчі!")
            return

        self.score_a = 0
        self.score_b = 0
        self.current_set += 1

    def undo(self):
        """Скасовує останню дію (додавання або віднімання балу)."""
        if not self.history:
            messagebox.showwarning("Увага", "Немає дій для скасування!")
            return

        last_state = self.history.pop()
        self.score_a, self.score_b, self.sets_a, self.sets_b, self.current_set, self.game_over = last_state
        self.update_display()

    def reset_match(self):
        """Повністю скидає гру до початкового стану."""
        if messagebox.askyesno("Новий матч",
                               "Ви впевнені, що хочете почати новий матч? Поточний рахунок буде видалено."):
            self.score_a = 0
            self.score_b = 0
            self.sets_a = 0
            self.sets_b = 0
            self.current_set = 1
            self.game_over = False
            self.history.clear()
            self.update_display()

    def update_display(self):
        """Оновлює всі елементи інтерфейсу."""
        self.btn_a.config(text=f"Команда А\n{self.score_a}")
        self.btn_b.config(text=f"Команда Б\n{self.score_b}")
        self.sets_label.config(text=f"Партії: {self.sets_a} : {self.sets_b}")

        if self.game_over:
            self.set_number_label.config(text="Матч закінчено!", fg="red", font=("Arial", 12, "bold"))
            self.btn_a.config(state=tk.DISABLED)
            self.btn_b.config(state=tk.DISABLED)
            self.btn_minus_a.config(state=tk.DISABLED)
            self.btn_minus_b.config(state=tk.DISABLED)
        else:
            self.set_number_label.config(text=f"Партія {self.current_set}", fg="black", font=("Arial", 11, "italic"))
            self.btn_a.config(state=tk.NORMAL)
            self.btn_b.config(state=tk.NORMAL)
            self.btn_minus_a.config(state=tk.NORMAL)
            self.btn_minus_b.config(state=tk.NORMAL)


if __name__ == "__main__":
    root = tk.Tk()
    app = VolleyballScoreboard(root)
    root.mainloop()
