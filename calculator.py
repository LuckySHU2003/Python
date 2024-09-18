import tkinter as tk

class Calculator:
    """ A simple GUI-based calculator app. """
    def __init__(self, root: tk.Tk) -> None:
        """ Constructs a new calculator.

        Parameters:
            root: The window to put this calculator inside.
        """
        self._displayed_text = ""

        # Set up screen to display the text a user types
        screen = tk.Frame(root, bg="blue")
        screen.pack(fill=tk.X)

        self._display = tk.Label(screen, bg="black", fg="white")
        self._display.pack(side=tk.LEFT)

        # Set up left-most grid of buttons (for entering numbers)
        number_frame = tk.Frame(root)
        number_frame.pack(side=tk.LEFT, expand=tk.TRUE)

        for i, char in enumerate("012345678.9C"):
            if i % 3 == 0:
                row = tk.Frame(number_frame)
                row.pack()
                
            button = self._create_button(row, char)
            button.pack(side=tk.LEFT)

        # Configure the command on the last button (the 'C' button) to clear
        # the display instead of adding a 'C' to the displayed string
        button.config(command=self._clear)

        # Set up right-most grid of buttons (operators)
        operator_frame = tk.Frame(root)
        operator_frame.pack(side=tk.LEFT, expand=tk.TRUE)

        for operator in "+-*=":
            button = self._create_button(operator_frame, operator)
            button.pack()

        # Configure the command on the last button (the '=' button) to evaluate
        # the displayed text instead of adding a '=' to the displayed string
        button.config(command=self._evaluate)

    def _create_button(self, parent: tk.Frame, char: str) -> tk.Button:
        """ Creates and returns a new button, with a default behaviour of
            adding the character shown on the button to the displayed text.

        Parameters:
            parent: the frame in which to put the new button.
            char: the character to display on the button (and to add to the
                  displayed text when the button is pressed).

        Returns:
            A new button, that has not yet been packed.
        """
        def add_number():
            """ Default callback for calculator buttons, which adds the
                appropriate character to the display.
            """
            self._displayed_text += char
            self._display.config(text=self._displayed_text)

        button = tk.Button(parent, text=char, command=add_number)
        return button

    def _clear(self):
        """ Clears the display. """
        self._displayed_text = ""
        self._display.config(text=self._displayed_text)

    def _evaluate(self):
        """ Evaluates the expression in the display and replaces the displayed
            text with the result.
        """
        # Note: eval is VERY bad practice, due to security risks
        # You should avoid using this function at all costs
        # and never use it in your assignments.
        self._displayed_text = str(eval(self._displayed_text))
        self._display.config(text=self._displayed_text)
        
if __name__ == '__main__':    
    root = tk.Tk()
    root.geometry('300x200')
    app = Calculator(root)
    root.mainloop()


