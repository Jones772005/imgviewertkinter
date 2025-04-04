import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

class ImageViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Viewer")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        self.root.configure(bg="#2E2E2E")  # Dark background

        # Image Display Label
        self.image_label = tk.Label(self.root, bg="#2E2E2E")
        self.image_label.pack(expand=True)

        # Top Frame - Browse Button
        top_frame = tk.Frame(self.root, bg="#2E2E2E")
        top_frame.pack(side=tk.TOP, pady=10)

        self.browse_btn = tk.Button(top_frame, text="Browse", command=self.browse_folder, bg="#444", fg="white")
        self.browse_btn.pack()

        # Bottom Frame - Navigation Buttons
        btn_frame = tk.Frame(self.root, bg="#2E2E2E")
        btn_frame.pack(side=tk.BOTTOM, pady=10)

        self.prev_btn = tk.Button(btn_frame, text="⬅ Previous", command=self.show_prev, state=tk.DISABLED, bg="#444", fg="white")
        self.prev_btn.grid(row=0, column=0, padx=5)

        self.next_btn = tk.Button(btn_frame, text="Next ➡", command=self.show_next, state=tk.DISABLED, bg="#444", fg="white")
        self.next_btn.grid(row=0, column=1, padx=5)

        self.slideshow_btn = tk.Button(btn_frame, text="Slideshow", command=self.toggle_slideshow, state=tk.DISABLED, bg="#444", fg="white")
        self.slideshow_btn.grid(row=0, column=2, padx=5)

        self.exit_btn = tk.Button(btn_frame, text=" Exit", command=self.root.quit, bg="#880000", fg="white")
        self.exit_btn.grid(row=0, column=3, padx=5)

        # Image Data
        self.image_list = []
        self.current_index = 0
        self.slideshow_running = False

        # Keyboard Bindings
        self.root.bind('<Left>', lambda e: self.show_prev())
        self.root.bind('<Right>', lambda e: self.show_next())
        self.root.bind('<Escape>', lambda e: self.root.quit())
        self.root.bind('<b>', lambda e: self.browse_folder())
        self.root.bind('<s>', lambda e: self.start_slideshow())
        self.root.bind('<x>', lambda e: self.stop_slideshow())

    def browse_folder(self):
        folder_selected = filedialog.askdirectory(title="Select Folder Containing Images")
        if not folder_selected:
            return

        supported_extensions = ('.png', '.jpg', '.jpeg', '.bmp')
        self.image_list = [os.path.join(folder_selected, f)
                           for f in os.listdir(folder_selected)
                           if f.lower().endswith(supported_extensions)]

        if not self.image_list:
            messagebox.showwarning("No Images", "No supported image files found in the folder.")
            return

        self.current_index = 0
        self.display_image()

        self.prev_btn.config(state=tk.NORMAL)
        self.next_btn.config(state=tk.NORMAL)
        self.slideshow_btn.config(state=tk.NORMAL)

    def display_image(self):
        try:
            img = Image.open(self.image_list[self.current_index])
            img.thumbnail((800, 600))
            self.tk_img = ImageTk.PhotoImage(img)
            self.image_label.config(image=self.tk_img)
            self.root.title(f"Image Viewer - {os.path.basename(self.image_list[self.current_index])}")
        except Exception as e:
            messagebox.showerror("Error", f"Cannot open image:\n{e}")

    def show_next(self):
        if self.image_list and self.current_index < len(self.image_list) - 1:
            self.current_index += 1
            self.display_image()
        elif self.slideshow_running:
            self.stop_slideshow()
        else:
            messagebox.showinfo("End", "This is the last image.")

    def show_prev(self):
        if self.image_list and self.current_index > 0:
            self.current_index -= 1
            self.display_image()
        else:
            messagebox.showinfo("Start", "This is the first image.")

    def toggle_slideshow(self):
        if self.slideshow_running:
            self.stop_slideshow()
        else:
            self.start_slideshow()

    def start_slideshow(self):
        if not self.image_list:
            return
        self.slideshow_running = True
        self.slideshow_btn.config(text="⏹ Stop", bg="#AA5500")
        self.run_slideshow()

    def stop_slideshow(self):
        self.slideshow_running = False
        self.slideshow_btn.config(text="▶ Slideshow", bg="#007744")

    def run_slideshow(self):
        if self.slideshow_running and self.current_index < len(self.image_list) - 1:
            self.current_index += 1
            self.display_image()
            self.root.after(2000, self.run_slideshow)
        else:
            self.stop_slideshow()

# Run App
if __name__ == "__main__":
    root = tk.Tk()
    app = ImageViewer(root)
    root.mainloop()
