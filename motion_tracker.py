import tkinter as tk

root = tk.Tk()
root.geometry('200x200')

def handle_motion(event: tk.Event) -> None:
    """ Displays the coordinates of a motion event.

    Parameters:
        event: The event object.
    """
    print(event.x, event.y)

frame = tk.Frame(root, bg='purple')
frame.pack(expand=tk.TRUE, fill=tk.BOTH)
frame.bind('<Motion>', handle_motion)

root.mainloop()
