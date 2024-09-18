import tkinter as tk



class App:
    """ A GUI that lets a user to toggle the background via a button press. """
    def __init__(self, root: tk.Tk):
        """ Constructs the application.

        Parameters:
            root: The window into which to put widgets
        """
        self._is_purple = True

        self._frame = tk.Frame(root, bg='purple')
        self._frame.pack(expand=tk.TRUE, fill=tk.BOTH)

        button = tk.Button(
            self._frame,
            text='Press Me',
            command=self._change_colour
        )
        button.pack(expand=tk.TRUE)

    def _change_colour(self):
        """ Toggles the colour of the background. """
        self._is_purple = not self._is_purple

        if self._is_purple:
            self._frame.config(bg="purple")
        else:
            self._frame.config(bg="yellow")
        
if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('200x200')
    app = App(root)
    root.mainloop()
