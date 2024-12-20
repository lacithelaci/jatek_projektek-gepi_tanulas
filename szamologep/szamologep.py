import tkinter as tk
from typing import Union, Callable


def button_click(number: Union[int, str]) -> None:
    current: str = entry.get()
    entry.delete(0, tk.END)
    entry.insert(tk.END, current + str(number))


def button_clear() -> None:
    entry.delete(0, tk.END)


def button_equal() -> None:
    try:
        result: Union[int, float] = eval(entry.get())
        entry.delete(0, tk.END)
        entry.insert(tk.END, result)
    except Exception:
        entry.delete(0, tk.END)
        entry.insert(tk.END, "Error")


root: tk.Tk = tk.Tk()
root.title("Calculator")

entry: tk.Entry = tk.Entry(root, width=35, borderwidth=5)
entry.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

buttons = [
    ("1", 1), ("2", 2), ("3", 3), ("+", "+"),
    ("4", 4), ("5", 5), ("6", 6), ("-", "-"),
    ("7", 7), ("8", 8), ("9", 9), ("*", "*"),
    ("0", 0), ("C", button_clear), ("=", button_equal), ("/", "/")
]

row: int = 1
col: int = 0
for button in buttons:
    text: str = button[0]
    value: Union[int, str, Callable[[], None]] = button[1]
    if text == "=":
        tk.Button(root, text=text, padx=79, pady=20, command=value).grid(row=row, column=col, columnspan=2)
        break
    tk.Button(root, text=text, padx=40, pady=20, command=lambda value=value: button_click(value)).grid(row=row, column=col)
    col += 1
    if col > 3:
        col = 0
        row += 1

root.mainloop()
