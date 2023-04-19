import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter.scrolledtext import ScrolledText
import keyword
import black
import io
import autopep8
import os


class CdEditor(tk.Tk):
    def __init__(self):
        super().__init__()

        self.opened_file = None

        self._create_menu()
        self._create_asset_viewer()
        self._create_code_editor()

        self._orig = self._w + "_orig"
        self.tk.call("rename", self._w, self._orig)
        self.tk.createcommand(self._w, self._proxy)
        

    def _create_widgets(self):
        
        self._create_asset_viewer()
        self._create_code_editor()


    def _proxy(self, command, *args):
        cmd = (self._orig, command) + args
        result = self.tk.call(cmd)

        if command in ("insert", "delete", "replace"):
            self.event_generate("<<Change>>", when="tail")

        return result
    


    def _create_menu(self):
        menubar = tk.Menu(self)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Open", command=self._open_file)
        filemenu.add_command(label="Save", command=self._save_file)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="File", menu=filemenu)
        self.config(menu=menubar)

    def _open_file(self):
        filepath = filedialog.askopenfilename(filetypes=[("All files", "*.*")])
        if not filepath:
            return

        with open(filepath, "r") as file:
            self.code_editor.delete(1.0, "end")
            self.code_editor.insert("insert", file.read())

    def _save_file(self):
        filepath = filedialog.asksaveasfilename(filetypes=[("All files", "*.*")])
        if not filepath:
            return

        with open(filepath, "w") as file:
            file.write(self.code_editor.get(1.0, "end"))
            

    def _create_asset_viewer(self):
        self.asset_viewer = ttk.Treeview(self)
        self.asset_viewer.heading("#0", text="Assets")
        self.asset_viewer.pack(side="left", fill="y")

        self.asset_viewer.bind("<Double-1>", self.on_asset_double_click)
        self.asset_viewer.bind("<<TreeviewOpen>>", self.on_directory_expand)

        current_directory = os.getcwd()
        self._populate_asset_viewer(current_directory, '')

    def _populate_asset_viewer(self, path, parent):
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            if os.path.isdir(item_path):
                node = self.asset_viewer.insert(parent, 'end', text=item, values=(item_path,))
                self.asset_viewer.insert(node, 'end')
            elif os.path.isfile(item_path):
                self.asset_viewer.insert(parent, 'end', text=item, values=(item_path,))

    def run_current_file(self):
        if self.opened_file:
            os.system(f'python {self.opened_file}')


    def on_directory_expand(self, event):
        selected_item = self.asset_viewer.focus()
        self.asset_viewer.delete(*self.asset_viewer.get_children(selected_item))
        directory_path = self.asset_viewer.item(selected_item)['values'][0]
        self._populate_asset_viewer(directory_path, selected_item)

    def on_asset_double_click(self, event):
        item_id = self.asset_viewer.selection()[0]
        file_path = self.asset_viewer.item(item_id)['values'][0]
        if os.path.isfile(file_path):
            self.open_file_in_editor(file_path)

    def open_file_in_editor(self, file_path):
        self.code_editor.delete("1.0", "end")
        with open(file_path, "r") as file:
            content = file.read()
            self.code_editor.insert("1.0", content)
        self.opened_file = file_path
        self.code_editor.on_change()


    def _create_code_editor(self):
        self.code_editor_frame = tk.Frame(self)
        self.code_editor_frame.pack(side="left", fill="both", expand=True)

        self.code_editor = SyntaxHighlightingText(self.code_editor_frame)
        self.code_editor.config(wrap="none")
        self.code_editor.pack(fill="both", expand=True)

        self.save_button = tk.Button(self.code_editor_frame, text="Save", command=self.save_file)
        self.save_button.pack(side="bottom")

        self.run_button = tk.Button(self.code_editor_frame, text="Run", command=self.run_current_file)
        self.run_button.pack(side="bottom")

    def save_file(self):
        if self.opened_file:
            content = self.code_editor.get("1.0", "end-1c")
            with open(self.opened_file, "w") as file:
                file.write(content)

class SyntaxHighlightingText(tk.Text):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configure_tags()

        self.configure_tags()
        self.bind("<<Change>>", self.on_change)
        self.bind("<KeyRelease>", self.on_key_release)

    def configure_tags(self):
        self.tag_configure("KEYWORD", foreground="blue")
        self.tag_configure("STRING", foreground="green")
        self.tag_configure("COMMENT", foreground="red")

    def on_change(self, event=None):
        self.remove_tags("1.0", "end")

        self.highlight_pattern(r'\b(?:%s)\b' % '|'.join(keyword.kwlist), "KEYWORD")
        self.highlight_pattern(r'".*?"', "STRING")
        self.highlight_pattern(r'#.*', "COMMENT")

    def on_key_release(self, event=None):
        self.on_change()

    def remove_tags(self, start, end):
        for tag in self.tag_names():
            self.tag_remove(tag, start, end)

    def highlight_pattern(self, pattern, tag):
        import re
        start = self.index("1.0")
        end = self.index("end")
        text = self.get(start, end)

        for match in re.finditer(pattern, text):
            first, last = match.span()
            self.tag_add(tag, f"{start}+{first}c", f"{start}+{last}c")

    def format_code(text_widget):
        source_code = text_widget.get("1.0", "end-1c")
        try:
            formatted_code = black.format_file_contents(source_code, mode=black.FileMode())
        except black.NothingChanged:
            formatted_code = source_code

        formatted_code = autopep8.fix_code(formatted_code)
        text_widget.delete("1.0", "end")
        text_widget.insert("1.0", formatted_code)

if __name__ == "__main__":
    app = CdEditor()
    app.mainloop()
