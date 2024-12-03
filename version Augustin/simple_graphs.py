import tkinter as tk

def create_bar_graph(master, data, title, max_height=200, bar_width=30, spacing=10):
    graph_frame = tk.Frame(master, bg="#003366")
    graph_frame.pack(pady=10)

    tk.Label(graph_frame, text=title, font=("Helvetica", 16), bg="#003366", fg="white").pack()

    canvas = tk.Canvas(graph_frame, width=(bar_width + spacing) * len(data), height=max_height + 30, bg="#003366")
    canvas.pack()

    max_value = max(data.values()) if data else 1
    for i, (key, value) in enumerate(data.items()):
        height = (value / max_value) * max_height
        x = i * (bar_width + spacing)
        canvas.create_rectangle(x, max_height - height, x + bar_width, max_height, fill="#00509e")
        canvas.create_text(x + bar_width/2, max_height + 10, text=key, fill="white", anchor="n")
        canvas.create_text(x + bar_width/2, max_height - height - 10, text=str(round(value, 2)), fill="white", anchor="s")

    return graph_frame