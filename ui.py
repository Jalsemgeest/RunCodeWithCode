import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from runner import Runner
from pystray import Icon as icon, MenuItem as item, Menu as menu # pip install pystray
from PIL import Image # pip install pillow

# use pyinstaller
# python3 -m PyInstaller --onefile .\ui.py --paths=c:\users\cptli\appdata\local\packages\pythonsoftwarefoundation.python.3.10_qbz5n2kfra8p0\localcache\local-packages\python310\site-packages --noconsole

class RunnerUi:
    def __init__(self, root, tray, show_ui=False):
        self.runner = Runner()
        self.tray = tray
        self.show_runner_ui = show_ui
        self.root = root

        self.update_tray()

        if self.show_runner_ui:
            self.create_ui()

    def create_ui(self):
        if self.root != None:
            return

        self.root = tk.Tk()
        self.root.title('Runner App (Subscribe)')

        # Frame for the Listbox and its Scrollbar
        frame = tk.Frame(root)
        frame.pack(fill=tk.BOTH, expand=True)

        # Scrollbar for the Listbox
        scrollbar = tk.Scrollbar(frame, orient="vertical")
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Listbox setup
        self.listbox = tk.Listbox(frame, yscrollcommand=scrollbar.set, activestyle = 'dotbox', 
                  font = "Helvetica", selectmode=tk.SINGLE, width=80, height=10)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.listbox.yview)

        # Populate the Listbox with items
        self.update_list()

        # Bind the Listbox click event
        self.listbox.bind('<<ListboxSelect>>', self.on_item_selected)

        # Button to open the popup
        self.add_script = tk.Button(root, text='Add Script', command=self.open_add_script)
        self.add_script.pack(pady=20)
        
        self.delete_script = tk.Button(root, text='Delete Script', command=self.delete_script)
        self.delete_script.pack(pady=20)

        self.run_script_button = tk.Button(root, text='Run Script', command=self.show_run_prompt)
        self.run_script_button.pack(pady=20)

        def on_close():
            self.root.quit()
            self.root.destroy()
            self.root = None
        self.root.protocol("WM_DELETE_WINDOW", on_close)

        self.root.mainloop()

    def update_list(self):
        if self.show_runner_ui or self.root != None:
            self.listbox.delete(0, tk.END)
            for app in self.runner.list_applications():
                self.listbox.insert(tk.END, f'{app.name}')
        self.update_tray()

    def update_tray(self):
        global menu_items
        new_items = [
            item('Runner App', self.create_ui),
            item('Add App', self.open_add_script),
        ]
        apps = []
        for i in range(len(self.runner.list_applications())):
            app = self.runner.list_applications()[i]
            apps.append(item(app.name, self.indirect_call_app(i)))
        
        new_items.append(item('Apps', menu(lambda: apps)))
        new_items.append(item('Exit', stop_tray))
        menu_items = new_items

        self.tray.update_menu()

    def indirect_call_app(self, index):
        def run_app():
            self.show_run_prompt(index=index)
        return run_app

    def delete_script(self):
        if self.selected_item_index is None:
            return
        self.runner.delete_application_ui(self.selected_item_index)
        self.update_list()
        self.selected_item_index = None

    def show_run_prompt(self, index=-1):
        if index != -1:
            self.selected_item_index = index
        if self.selected_item_index is None:
            return
        app = self.runner.list_applications()[self.selected_item_index]

        self.run_popup = tk.Tk()
        self.run_popup.title(app.name)

        if app.input_type == "File":
            self.input_value = tk.Label(self.run_popup, text='No file selected', relief="sunken", width=50)
            self.input_value.pack(pady=10)

            browse_button = tk.Button(self.run_popup, text='Browse File', command=self.run_files_selector)
            browse_button.pack()
        elif app.input_type == "String":
            self.input_value = tk.Entry(self.run_popup, width=50)
            self.input_value.pack(pady=10)
        elif app.input_type == "Number":
            self.input_value = tk.Entry(self.run_popup, width=50)
            self.input_value.pack(pady=10)
        
        # Close button for the popup
        run_button = tk.Button(self.run_popup, text='Run', command=self.run_app)
        run_button.pack(pady=20)

        # Close button for the popup
        close_button = tk.Button(self.run_popup, text='Close', command=self.run_popup.destroy)
        close_button.pack(pady=20)

        self.run_popup.mainloop()

    def run_app(self):
        self.runner.run_application_ui(self.selected_item_index, self.input_value.cget("text"))
        self.run_popup.destroy()

    def run_files_selector(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.input_value.config(text=file_path)

    def on_item_selected(self, event):
        # Event triggered function when a Listbox item is selected
        widget = event.widget
        selection = widget.curselection()
        if selection:
            index = selection[0]
            item = widget.get(index)
            self.selected_item_index = index
            # messagebox.showinfo("Item Selected", f"You selected: {item}")

    def open_add_script(self):
        # Popup window for file chooser
        self.popup = tk.Tk()
        self.popup.title('File Chooser')

        # Entry for name of script
        self.new_app_name = tk.Entry(self.popup, width=50)
        self.new_app_name.pack(pady=10)

        # Radio button variables
        self.radio_var = tk.IntVar()
        self.radio_var.set(1)  # Default selection

        # Radio buttons
        tk.Radiobutton(self.popup, text="File", variable=self.radio_var, value=1).pack(anchor=tk.W)
        tk.Radiobutton(self.popup, text="String", variable=self.radio_var, value=2).pack(anchor=tk.W)
        tk.Radiobutton(self.popup, text="Number", variable=self.radio_var, value=3).pack(anchor=tk.W)

        # Entry for file path
        self.file_path_label = tk.Label(self.popup, text='No file selected', relief="sunken", width=50)
        self.file_path_label.pack(pady=10)

        # Button to browse files
        browse_button = tk.Button(self.popup, text='Browse Files', command=self.browse_files)
        browse_button.pack()

        # Close button for the popup
        save_button = tk.Button(self.popup, text='Save', command=self.save_new_script)
        save_button.pack(pady=20)

        # Close button for the popup
        close_button = tk.Button(self.popup, text='Close', command=self.popup.destroy)
        close_button.pack(pady=20)

        self.popup.mainloop()

    def save_new_script(self):
        self.new_app_name = self.new_app_name.get()
        file_type = self.radio_var.get()
        if file_type == 1:
            self.new_file_type = "File"
        elif file_type == 2:
            self.new_file_type = "String"
        elif file_type == 3:
            self.new_file_type = "Number"
        self.new_file_path = self.file_path_label.cget("text")

        self.show_adding_popup()

    def show_adding_popup(self):
        # Popup window for file chooser
        self.adding_popup = tk.Tk()
        self.adding_popup.title('Confirm Add?')

        self.file_path_label = tk.Label(self.adding_popup, text=f'We will add:\nName: {self.new_app_name}\nType:{self.new_file_type}\nPath:{self.new_file_path}', relief="sunken", width=50)
        self.file_path_label.pack(pady=10)

        # Close button for the popup
        save_button = tk.Button(self.adding_popup, text='Confirm', command=self.save_script)
        save_button.pack(pady=20)

        # Close button for the popup
        close_button = tk.Button(self.adding_popup, text='Close', command=self.popup.destroy)
        close_button.pack(pady=20)

        self.adding_popup.mainloop()

    def save_script(self):
        print("Confirmed storing")
        self.runner.add_application_ui(self.new_app_name, self.new_file_type, self.new_file_path)
        self.update_list()
        self.adding_popup.destroy()
        self.popup.destroy()

    def browse_files(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.file_path_label.config(text=file_path)

tray_ref = None
root = None

def stop_tray(icon, _):
    global root
    if root != None:
        root.quit()
        root.destroy()
        root = None
    icon.stop()

menu_items = [item('Exit', stop_tray)]

if __name__ == '__main__':
    image = Image.open('C:/Users/cptli/Documents/dev/HelpfulTools/helper-packages/transparent_transparent_happyface.png')
    tray_ref = icon(
        'App Runner',
        icon=image,
        menu=menu(lambda: menu_items)
    )
    runner_app = RunnerUi(root=root, tray=tray_ref, show_ui=False)
    tray_ref.run()