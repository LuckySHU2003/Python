import tkinter as tk

COLOURS = [
    'red',
    'blue',
    'green',
    'purple',
    'brown',
    'orange',
    'pink',
    'yellow',
    'light green',
    'purple'
]

root = tk.Tk()
root.geometry('200x200')

# outer_frame keeps its contents centered within root
outer_frame = tk.Frame(root)
outer_frame.pack(expand=tk.TRUE)

def create_number(parent: tk.Frame, number: int, colour: str) -> None:
    """ Creates and packs a number label.

    Parameters:
        parent: The frame in which to create the label.
        number: The number to display on the label.
        colour: The background colour to use for the label.
    """
    label = tk.Label(
        parent,
        text=str(number),
        bg=colour,
        width=2,
        padx=5,
        pady=5
    )
    label.pack(side=tk.LEFT)

for number in range(10):
    if number % 3 == 0:
        row = tk.Frame(outer_frame)
        row.pack() # packs to tk.TOP by default
    create_number(row, number, COLOURS[number])

    

root.mainloop()
