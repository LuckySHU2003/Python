import tkinter as tk

def handle_submit():
    """ Callback for button press. """
    print(entry.get())

root = tk.Tk()
root.geometry('300x100')

entry = tk.Entry(root)
entry.pack(side=tk.LEFT, expand=tk.TRUE)

button = tk.Button(root, text='Submit', command=handle_submit)
button.pack(side=tk.LEFT, expand=tk.TRUE)

root.mainloop()
