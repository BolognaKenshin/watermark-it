import os
import tkinter as tk
from tkinter import filedialog, font, ttk
from tkinterdnd2 import TkinterDnD, DND_FILES
from tkinter.colorchooser import askcolor
from PIL import Image, ImageTk, ImageDraw, ImageFont
import magic

main_window = TkinterDnD.Tk()
main_window.title("Carl's Watermark App")
main_window.minsize(width=1200, height=700)

current_color = (0, 0, 0, 255)

window_dict = {
"watermark_window": None,
"text_window": None,
"logo_window": None,
}

main_window.grid_columnconfigure(index=0, weight=1)
main_window.grid_columnconfigure(index=1, weight=1)
main_window.grid_columnconfigure(index=2, weight=1)


# App Functions

# Adjusts canvas to size of image, then displays image - Connected to "Upload" button
# Function will close other open windows when called
def upload_image(photo_canvas):
    if window_dict["watermark_window"] or window_dict["text_window"]:
        window_dict["watermark_window"].destroy()
        window_dict["text_window"].destroy()
    if window_dict["text_window"] or window_dict["text_window"]:
        window_dict["watermark_window"].destroy()
        window_dict["text_window"].destroy()
    if window_dict["logo_window"] or window_dict["text_window"]:
        window_dict["watermark_window"].destroy()
        window_dict["text_window"].destroy()
    uploaded_image_path = tk.filedialog.askopenfilename()
    if uploaded_image_path:
        file_type = magic.from_file(uploaded_image_path, mime=True)
        if file_type.startswith('image'):
            image = Image.open(uploaded_image_path)
            image_width, image_height = image.size
            photo_canvas.config(width=image_width, height=image_height)

            # pillow_image is meant to be original_image stored for drawing and undoing changes
            photo_canvas.pillow_image = image

            photo = ImageTk.PhotoImage(image)
            photo_canvas.image = photo
            photo_canvas.create_image(2, 2, image=photo, anchor="nw")
            watermark_options()
        else:
            print("That's not a valid file format.")


# Same as upload_image function, but works with drag-and-drop
# Function will close other open windows when called
def on_drop(event, photo_canvas):
    if window_dict["watermark_window"] or window_dict["text_window"]:
        window_dict["watermark_window"].destroy()
        window_dict["text_window"].destroy()
    if window_dict["text_window"] or window_dict["text_window"]:
        window_dict["watermark_window"].destroy()
        window_dict["text_window"].destroy()
    if window_dict["logo_window"] or window_dict["text_window"]:
        window_dict["watermark_window"].destroy()
        window_dict["text_window"].destroy()
    file_path = event.data.strip("{}")
    if file_path:
        file_type = magic.from_file(file_path, mime=True)
        if file_type.startswith('image'):
            image = Image.open(file_path)
            image_width, image_height = image.size
            photo_canvas.config(width=image_width, height=image_height)

            # pillow_image is meant to be original_image stored for drawing and undoing changes
            photo_canvas.pillow_image = image

            photo = ImageTk.PhotoImage(image)
            photo_canvas.image = photo
            photo_canvas.create_image(2, 2, image=photo, anchor="nw")
            watermark_options()
        else:
            print("That's not a valid file format.")


# Generated the watermark options window, text or logo
def watermark_options():
    watermark_window = tk.Toplevel(main_window)
    watermark_window.minsize(width=200, height=50)
    watermark_window.title("Add Text or Logo")
    add_text_button = tk.Button(watermark_window,
                                text="Add Text",
                                command=text_options)
    add_logo_button = tk.Button(watermark_window,
                                text="Add Logo",
                                command=logo_options)
    window_dict["watermark_window"] = watermark_window
    add_text_button.grid(column=0, row=1, padx=75, pady=25)
    add_logo_button.grid(column=1, row=1, padx=75, pady=25)


# Generates the text options window - Stores them in dictionary, passes to add_text() via text_submit button
# Color gets passed separate from the dictionary as the askcolor box doesn't pass values the same way
def text_options():
    global current_color
    if window_dict["watermark_window"]:
        window_dict["watermark_window"].destroy()
    text_window = tk.Toplevel(main_window)
    window_dict["text_window"] = text_window
    text_window.title("Text Options")
    text_window.minsize(width=250, height=600)

    # Text Entry
    text_box = tk.Entry(text_window)
    text_box.grid(row=0, column=0, sticky="w", padx=10)
    text_submit = tk.Button(text_window, text="Add Text", command=lambda: add_text(user_text_selections,
                                                                                   current_color,
                                                                                   available_fonts,
                                                                                   font_display_names))
    text_submit.grid(row=0, column=1, sticky="w", padx=10)

    # Font Selection
    available_fonts = [font for font in os.listdir("./fonts") if font.endswith((".ttf", ".otf"))]
    font_display_names = [font.replace(".ttf", "").replace(".otf", "") for font in available_fonts]
    font_menu = ttk.Combobox(text_window, values=font_display_names, height=10, state="readonly")
    for font in available_fonts:
        font_menu.insert(tk.END, font)
    font_menu.set("Boldness")
    font_menu.grid(row=1, column=0, sticky="w", padx=10, pady=15)
    font_sizes = [f'{str(size)}px' for size in range(10, 401, 2)]
    font_size_menu = ttk.Combobox(text_window, values=font_sizes, height=10, state="readonly")
    font_size_menu.set("10px")
    font_size_menu.grid(row=2, column=0, padx=10, pady=15)

    # Color Selection - Updates global current_color variable, passes it to add_text() in text_submit button
    add_color_button = tk.Button(text_window, text="Add Color", command=select_color)
    add_color_button.grid(row=3, column=0, sticky="w", padx=10, pady=15)
    opacity_label = tk.Label(text_window, text="Opacity")
    opacity_slider = tk.Scale(text_window, from_=0, to=255, orient="horizontal")
    opacity_slider.set(255)
    opacity_label.grid(row=4, column=0)
    opacity_slider.grid(row=5, column=0)

    # Stores the widgets as values, so they can be passed to add_text and retrieved via .get()
    user_text_selections = {
        "text": text_box,
        "font": font_menu,
        "font_size": font_size_menu,
        "opacity": opacity_slider,
    }


# Adding formatted text - Received from text_options()
def add_text(text_options, current_color, fonts, font_display_names):
    text = text_options["text"].get()
    font = text_options["font"].get()
    font_size = int(text_options["font_size"].get().strip("px"))
    opacity = text_options["opacity"].get()
    text_color = (current_color[0], current_color[1], current_color[2], opacity)
    font_index = font_display_names.index(font)
    font_file = ImageFont.truetype(f'fonts/{fonts[font_index]}', size=font_size)
    new_image = photo_canvas.pillow_image.copy().convert("RGBA")
    draw = ImageDraw.Draw(new_image)
    draw.text((10, 10), text=text, font=font_file, fill=text_color)
    updated_image = ImageTk.PhotoImage(new_image)
    photo_canvas.display_image = updated_image
    photo_canvas.create_image(2, 2, image=updated_image, anchor="nw")


# Generated the logo options window - Contains the window's widgets
def logo_options():
    if window_dict["watermark_window"]:
        window_dict["watermark_window"].destroy()
    logo_window = tk.Toplevel(main_window)
    logo_window.title("Text Options")
    logo_window.minsize(width=250, height=600)
    window_dict["logo_window"] = logo_window

# Select a color for text or logo
def select_color():
    global current_color
    color = askcolor()[0]
    current_color = (color[0], color[1], color[2], 255)
    print(current_color)
    window_dict["text_window"].lift()






# Main App - Components
my_label = tk.Label(text="Carl's Watermark App", font=("Arial", 24, "bold"))
landscape_image = Image.open("./sunset-golden.jpg")
landscape_width, landscape_height = landscape_image.size
landscape_photo = ImageTk.PhotoImage(landscape_image)
drag_label = tk.Label(text="Drag your image", font=("Arial", 18))
or_label = tk.Label(text="Or", font=("Arial", 12))
photo_canvas = tk.Canvas(bg="black", width=landscape_width, height=landscape_height)
upload_button = tk.Button(text="Upload", font=("Arial", 14), command=lambda: upload_image(photo_canvas))
photo_canvas.create_image(2, 2, image=landscape_photo, anchor="nw")

# Main App - Grid
my_label.grid(column=1, row=0)
drag_label.grid(column=1, row=2)
or_label.grid(column=1, row=3)
upload_button.grid(column=1, row=4)
photo_canvas.grid(column=1, row=5)



main_window.drop_target_register(DND_FILES)
main_window.dnd_bind('<<Drop>>', lambda event: on_drop(event, photo_canvas))
main_window.mainloop()