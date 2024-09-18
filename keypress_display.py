import tkinter as tk

root = tk.Tk()
root.geometry('200x200')

def handle_keypress(event: tk.Event) -> None:
    """ Displays key pressed, in 3 different formats.

    Parameters:
        event: The event object.
    """
    label.config(text=f"{event.char}, {event.keysym}, {event.keycode}")

label = tk.Label(root, text="Press a key")
label.pack(expand=tk.TRUE)

root.bind('<Key>', handle_keypress)

root.mainloop()
