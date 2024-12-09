import tkinter as tk

def create_bar_graph(master, data, title, colors=None, max_height=100, bar_width=30, spacing=13, padding=10):
    graph_frame = tk.Frame(master, bg="#003366")
    graph_frame.pack(pady=10)

    tk.Label(graph_frame, text=title, font=("Helvetica", 16), bg="#003366", fg="white").pack()

    canvas = tk.Canvas(graph_frame, width=(bar_width + spacing) * len(data) + 2 * padding,
                       height=max_height + 50 + 2 * padding, bg="#003366")
    canvas.pack()

    max_value = max(data.values()) if data else 1
    legend_frame = tk.Frame(graph_frame, bg="#003366")
    legend_frame.pack(pady=5)

    for i, (key, value) in enumerate(data.items()):
        height = (value / max_value) * max_height
        x = i * (bar_width + spacing) + padding
        bar_color = colors[i] if colors and i < len(colors) else "#00509e"
        canvas.create_rectangle(x, max_height - height + padding, x + bar_width, max_height + padding, fill=bar_color)
        canvas.create_text(x + bar_width/2, max_height + 10 + padding, text=key, fill="white", anchor="n")
        canvas.create_text(x + bar_width/2, max_height - height - 10 + padding, text=str(round(value, 2)), fill="white", anchor="s")

        legend_label = tk.Label(legend_frame, text=f"{key}: {value}", font=("Helvetica", 12), bg="#003366", fg="white")
        legend_label.pack(side=tk.LEFT, padx=5)
        legend_label.configure(fg=bar_color)

    return graph_frame