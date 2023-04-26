import tkinter as tk
import traceback

def show_error_dialog():
    # Create a new Tkinter window
    root = tk.Tk()
    root.title("Crash Handler.")

    # Add a label with an error message
    error_message = tk.Label(root, text="Oops! An error occurred.")
    error_message.pack(padx=10, pady=10)

    # Add a text area to display the error traceback
    error_text = tk.Text(root, width=80, height=20, wrap="word")
    error_text.pack(padx=10, pady=10)

    # Get the error traceback and display it in the text area
    error_traceback = traceback.format_exc()
    error_text.insert(tk.END, error_traceback)

    # Add a button to close the window
    close_button = tk.Button(root, text="Close", command=root.destroy)
    close_button.pack(padx=10, pady=10)

    # Run the Tkinter event loop
    root.mainloop()

