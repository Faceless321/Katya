import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os

DATA_FILE = 'movies.json'

class MovieLibrary:
    def __init__(self, root):
        self.root = root
        self.root.title("Movie Library")
        
        self.movies = []
        
        self.create_widgets()
        self.load_data()
        self.populate_treeview()
    
    def create_widgets(self):
        frame_input = tk.Frame(self.root)
        frame_input.pack(pady=10)
        
        tk.Label(frame_input, text='Название:').grid(row=0, column=0, padx=5, pady=5)
        self.entry_title = tk.Entry(frame_input)
        self.entry_title.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(frame_input, text='Жанр:').grid(row=0, column=2, padx=5, pady=5)
        self.entry_genre = tk.Entry(frame_input)
        self.entry_genre.grid(row=0, column=3, padx=5, pady=5)
        
        tk.Label(frame_input, text='Год выпуска:').grid(row=1, column=0, padx=5, pady=5)
        self.entry_year = tk.Entry(frame_input)
        self.entry_year.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(frame_input, text='Рейтинг:').grid(row=1, column=2, padx=5, pady=5)
        self.entry_rating = tk.Entry(frame_input)
        self.entry_rating.grid(row=1, column=3, padx=5, pady=5)
        
        btn_add = tk.Button(self.root, text="Добавить фильм", command=self.add_movie)
        btn_add.pack(pady=5)
        
        frame_filter = tk.Frame(self.root)
        frame_filter.pack(pady=10)
        tk.Label(frame_filter, text='Фильтр по жанру:').grid(row=0, column=0, padx=5)
        self.combo_genre_filter = ttk.Combobox(frame_filter, values=[])
        self.combo_genre_filter.grid(row=0, column=1, padx=5)
        self.combo_genre_filter.bind("<<ComboboxSelected>>", self.filter_movies)
        tk.Label(frame_filter, text='Фильтр по году:').grid(row=0, column=2, padx=5)
        self.combo_year_filter = ttk.Combobox(frame_filter, values=[])
        self.combo_year_filter.grid(row=0, column=3, padx=5)
        self.combo_year_filter.bind("<<ComboboxSelected>>", self.filter_movies)
        
        btn_clear_filter = tk.Button(frame_filter, text="Сбросить фильтр", command=self.clear_filter)
        btn_clear_filter.grid(row=0, column=4, padx=5)
        
        columns = ('Название', 'Жанр', 'Год', 'Рейтинг')
        self.tree = ttk.Treeview(self.root, columns=columns, show='headings')
        for col in columns:
            self.tree.heading(col, text=col)
        self.tree.pack(pady=10, fill=tk.BOTH, expand=True)
    
    def load_data(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r', encoding='utf-8') as file:
                self.movies = json.load(file)
        else:
            self.movies = []
    
    def save_data(self):
        with open(DATA_FILE, 'w', encoding='utf-8') as file:
            json.dump(self.movies, file, ensure_ascii=False, indent=4)
    
    def populate_treeview(self, movies=None):
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        if movies is None:
            movies = self.movies
        for m in movies:
            self.tree.insert('', tk.END, values=(m['title'], m['genre'], m['year'], m['rating']))
        
        self.update_filters()
    
    def update_filters(self):
        genres = list({m['genre'] for m in self.movies})
        years = list({str(m['year']) for m in self.movies})
        genres.sort()
        years.sort()
        self.combo_genre_filter['values'] = ['Все'] + genres
        self.combo_year_filter['values'] = ['Все'] + years
        self.combo_genre_filter.set('Все')
        self.combo_year_filter.set('Все')
    
    def add_movie(self):
        title = self.entry_title.get().strip()
        genre = self.entry_genre.get().strip()
        year_str = self.entry_year.get().strip()
        rating_str = self.entry_rating.get().strip()
        
        if not title or not genre or not year_str or not rating_str:
            messagebox.showerror("Ошибка", "Пожалуйста, заполните все поля.")
            return
        
        if not year_str.isdigit():
            messagebox.showerror("Ошибка", "Год должен быть числом.")
            return
        year = int(year_str)
        
        try:
            rating = float(rating_str)
        except ValueError:
            messagebox.showerror("Ошибка", "Рейтинг должен быть числом.")
            return
        if not (0 <= rating <= 10):
            messagebox.showerror("Ошибка", "Рейтинг должен быть от 0 до 10.")
            return
        
        new_movie = {
            'title': title,
            'genre': genre,
            'year': year,
            'rating': rating
        }
        self.movies.append(new_movie)
        self.save_data()
        self.populate_treeview()
        
        self.entry_title.delete(0, tk.END)
        self.entry_genre.delete(0, tk.END)
        self.entry_year.delete(0, tk.END)
        self.entry_rating.delete(0, tk.END)
    
    def filter_movies(self, event=None):
        genre_filter = self.combo_genre_filter.get()
        year_filter = self.combo_year_filter.get()
        filtered = self.movies
        
        if genre_filter != 'Все':
            filtered = [m for m in filtered if m['genre'] == genre_filter]
        if year_filter != 'Все':
            try:
                year_val = int(year_filter)
                filtered = [m for m in filtered if m['year'] == year_val]
            except ValueError:
                pass
        self.populate_treeview(filtered)
    
    def clear_filter(self):
        self.combo_genre_filter.set('Все')
        self.combo_year_filter.set('Все')
        self.populate_treeview()

if __name__ == "__main__":
    root = tk.Tk()
    app = MovieLibrary(root)
    root.mainloop()
