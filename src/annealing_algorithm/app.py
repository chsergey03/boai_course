from solution import Solution
from algorithm import make_annealing

import os

import tkinter as tk
from tkinter import *

from PIL import Image, ImageTk

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)


def start(
        arg: tuple[Solution, list[float], list[int], list[int]],
        field_canvas: Canvas,
        graphs_canvas: Canvas,
        graph_canvas_ref: list) -> None:
    result = make_annealing(*arg)
    
    if len(result) == 0:
        return None
    
    field_canvas.create_rectangle(
        0,
        0,
        845,
        845,
        fill="white",
        outline="white"
    )
    
    draw_solution(field_canvas, result[0])
    
    draw_graphs(
        graphs_canvas,
        graph_canvas_ref,
        result[1],
        result[2],
        result[3]
    )
    
    return None

def draw_solution(
        field_canvas: Canvas,
        solution: Solution) -> None:
    colors = ("#BE855B", "#EFD2AA", "#004D40")
    
    start_position = (10, 10)

    board_size = solution.n_queens
    queens = solution.plan

    for i in range(board_size):
        for j in range(board_size):
            x1 = start_position[0] + square_size[0] * j
            y1 = start_position[1] + square_size[1] * i
            x2 = start_position[0] + square_size[0] * (j + 1)
            y2 = start_position[1] + square_size[1] * (i + 1)
            
            field_canvas.create_rectangle(
                x1,
                y1,
                x2,
                y2,
                fill=colors[(i + j) % 2],
                outline=colors[2]
            )
    
    for i in range(board_size):
        field_canvas.create_image(
            start_position[0] + square_size[0] * i,
            start_position[1] + square_size[1] * queens[i],
            anchor="nw",
            image=queen
        )


def draw_graphs(
        graphs_canvas: Canvas,
        graph_canvas_ref: list,
        temperatures: list[float],
        energies: list[int],
        bad_solutions: list[int]) -> None:
    DPI = 100.0

    fig, ax = plt.subplots(
        figsize=(graphs_canvas.winfo_width() / DPI, 4),
        dpi=DPI
    )

    ax.plot(
        list(range(len(temperatures))),
        temperatures,
        label="Температура",
        color="blue"
    )
    
    ax.plot(
        list(range(len(energies))),
        energies,
        label="Энергия",
        color="red"
    )
    
    ax.plot(
        list(range(len(bad_solutions))),
        bad_solutions,
        label="Количество плохих решений",
        color="green"
    )

    ax.set_xlabel("Индекс итерации")
    ax.set_ylabel("Значения")

    ax.set_title("График изменения температуры и энергии")

    ax.legend()
    
    if graph_canvas_ref[0] is not None:
        graph_canvas_ref[0].get_tk_widget().destroy()

    graph_canvas_ref[0] = FigureCanvasTkAgg(fig, master=graphs_canvas)
    graph_canvas_ref[0].draw()

    graph_canvas_ref[0].get_tk_widget().pack(fill=tk.BOTH, expand=True)


if __name__ == '__main__':
    root = Tk()
    root.title("Алгоритм отжига")
    root.state("zoomed")
    
    square_size = (15, 15)
    
    queen = ImageTk.PhotoImage(Image.open("queen.png").resize(square_size))

    n_queens = IntVar(value=8)
    init_temperature = DoubleVar(value=30.0)
    final_temperature = DoubleVar(value=0.5)
    cooling_rate = DoubleVar(value=0.99)
    n_steps = IntVar(value=100)

    label_1 = Label(text="Кол-во ферзей")
    label_2 = Label(text="Начальная температура")
    label_3 = Label(text="Финальная температура")
    label_4 = Label(text="Значение α")
    label_5 = Label(text="Кол-во итераций")

    entry_1 = Entry(textvariable=n_queens)
    entry_2 = Entry(textvariable=init_temperature)
    entry_3 = Entry(textvariable=final_temperature)
    entry_4 = Entry(textvariable=cooling_rate)
    entry_5 = Entry(textvariable=n_steps)

    field_canvas = Canvas(background="white", width=845, height=845)
    graphs_canvas = Canvas(background="white", width=520, height=400)
    graph_canvas_ref = [None]

    click = lambda : start(
        [n_queens.get(),
         init_temperature.get(),
         final_temperature.get(),
         cooling_rate.get(),
         n_queens.get()],
        field_canvas,
        graphs_canvas,
        graph_canvas_ref
    )

    button = Button(text="Получить решение", command=click)

    label_1.pack(anchor="nw")
    entry_1.pack(anchor="nw", padx=5)
    
    label_2.pack(anchor="nw")
    entry_2.pack(anchor="nw", padx=5)
    
    label_3.pack(anchor="nw")
    entry_3.pack(anchor="nw", padx=5)
    
    label_4.pack(anchor="nw")
    
    entry_4.pack(anchor="nw", padx=5)
    
    label_5.pack(anchor="nw")
    entry_5.pack(anchor="nw", padx=5)
    
    button.pack(anchor="nw", padx=7, pady=5)
    
    field_canvas.place(anchor="nw", x=150, y=5)
    
    graphs_canvas.place(anchor="nw", x=150 + 845 + 10, y=5)

    root.mainloop()