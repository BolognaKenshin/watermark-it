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
"upload_logo_window": None,
}

main_window.grid_columnconfigure(index=0, weight=1)
main_window.grid_columnconfigure(index=1, weight=1)
main_window.grid_columnconfigure(index=2, weight=1)


# App Functions

# Adjusts canvas to size of image, then displays image - Connected to "Upload" button
# Function will close other open windows when called
def upload_image(photo_canvas):
    if window_dict["watermark_window"]:
        window_dict["watermark_window"].destroy()
        window_dict["watermark_window"] = None
    if window_dict["text_window"]:
        window_dict["text_window"].destroy()
        window_dict["text_window"] = None
    if window_dict["logo_window"]:
        window_dict["logo_window"].destroy()
        window_dict["logo_window"] = None
    if window_dict["upload_logo_window"]:
        window_dict["upload_logo_window"].destroy()
        window_dict["upload_logo_window"] = None
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
            photo_canvas.original_image = photo
            photo_canvas.delete(photo_canvas.image_id)
            photo_canvas.image_id = photo_canvas.create_image(2, 2, image=photo, anchor="nw")
            watermark_options()
        else:
            print("That's not a valid file format.")


# Same as upload_image function, but works with drag-and-drop
# Function will close other open windows when called
def on_drop(event, photo_canvas):
    if window_dict["watermark_window"]:
        window_dict["watermark_window"].destroy()
        window_dict["watermark_window"] = None
    if window_dict["text_window"]:
        window_dict["text_window"].destroy()
        window_dict["text_window"] = None
    if window_dict["logo_window"]:
        window_dict["logo_window"].destroy()
        window_dict["logo_window"] = None
    if window_dict["upload_logo_window"]:
        window_dict["upload_logo_window"].destroy()
        window_dict["upload_logo_window"] = None
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
            photo_canvas.original_image = photo
            photo_canvas.delete(photo_canvas.image_id)
            photo_canvas.image_id = photo_canvas.create_image(2, 2, image=photo, anchor="nw")
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
                                command=upload_logo_window)
    window_dict["watermark_window"] = watermark_window
    add_text_button.grid(column=0, row=1, padx=75, pady=25)
    add_logo_button.grid(column=1, row=1, padx=75, pady=25)


# Generates the text options window - Stores them in dictionary, passes to add_text() via text_submit button
# Color gets passed separate from the dictionary as the askcolor box doesn't pass values the same way
def text_options():
    global current_color
    if window_dict["watermark_window"]:
        window_dict["watermark_window"].destroy()
        window_dict["watermark_window"] = None
    text_window = tk.Toplevel(main_window)
    window_dict["text_window"] = text_window
    text_window.title("Text Options")
    text_window.minsize(width=250, height=600)

    # Text Entry - Position
    text_box = tk.Entry(text_window)
    text_box.grid(row=0, column=0, sticky="w", padx=10)
    text_submit = tk.Button(text_window, text="Add Text", command=lambda: add_text(user_text_selections,
                                                                                   current_color,
                                                                                   available_fonts,
                                                                                   font_display_names))
    text_submit.grid(row=0, column=1, sticky="w", padx=10)
    copyright_button = tk.Button(text_window, text="Add ©", command=lambda: add_copyright(text_box))
    copyright_button.grid(row=1, column=1, sticky="w", padx=10)
    font_sizes = [f'{str(size)}px' for size in range(10, 401, 2)]
    font_size_menu = ttk.Combobox(text_window, values=font_sizes, height=10, state="readonly")
    font_size_menu.set("14px")

    text_x_label = tk.Label(text_window, text="X Coordinates")
    text_x_slider = tk.Scale(text_window, from_=0, to=photo_canvas.winfo_width(), orient="horizontal", showvalue=False)
    text_y_label = tk.Label(text_window, text="Y Coordinates")
    text_y_slider = tk.Scale(text_window, from_=6, to=photo_canvas.winfo_height(), orient="horizontal", showvalue=False)
    text_x_label.grid(row=1, column=0, sticky="w", padx=10)
    text_x_slider.grid(row=2, column=0, sticky="w", padx=10)
    text_y_label.grid(row=3, column=0, sticky="w", padx=10)
    text_y_slider.grid(row=4, column=0, sticky="w", padx=10)

    # Font Selection
    available_fonts = [font for font in os.listdir("./fonts") if font.endswith((".ttf", ".otf"))]
    font_display_names = [font.replace(".ttf", "").replace(".otf", "") for font in available_fonts]
    font_menu = ttk.Combobox(text_window, values=font_display_names, height=10, state="readonly")
    for font in available_fonts:
        font_menu.insert(tk.END, font)
    font_menu.set("Boldness")
    font_menu.grid(row=5, column=0, sticky="w", padx=10, pady=15)

    font_size_menu.grid(row=6, column=0, padx=10)

    # Tiling

    single_tile_button = tk.Button(text_window, text="•", font=(20), width=4, height=2, command=lambda: user_text_selections.update({"tiling": "single"}))
    square_tile_button = tk.Button(text_window, text="•   •\n•   •", font=(20), width=4, height=2, command=lambda: user_text_selections.update({"tiling": "square"}))
    diamond_tile_button = tk.Button(text_window, text="•\n•       •\n•", font=(20), width=4, height=2, command=lambda: user_text_selections.update({"tiling": "diamond"}))
    single_tile_button.grid(row=7, column=0, padx=10, pady=10)
    square_tile_button.grid(row=7, column=1, padx=10, pady=10)
    diamond_tile_button.grid(row=7, column=2, padx=10, pady=10)

    # Text Rotation
    text_angle_label = tk.Label(text_window, text="Text Angle")
    text_angle_slider = tk.Scale(text_window, from_=-180, to=180, orient="horizontal")
    text_angle_label.grid(row=8, column=0, padx=10, sticky="w")
    text_angle_slider.grid(row=9, column=0, padx=10, sticky="w")

    # Color - Opacity Selection - Updates global current_color variable, passes it to add_text() in text_submit button
    add_color_button = tk.Button(text_window, text="Add Color", command=select_color)
    add_color_button.grid(row=10, column=0, sticky="w", padx=10, pady=15)
    opacity_label = tk.Label(text_window, text="Opacity")
    opacity_slider = tk.Scale(text_window, from_=0, to=255, orient="horizontal", showvalue=False)
    opacity_slider.set(255)
    opacity_label.grid(row=11, column=0, sticky="w", padx=10)
    opacity_slider.grid(row=12, column=0, sticky="w", padx=10)
    save_image_button = tk.Button(text_window, text="Save Image", command=save_watermarked_image)
    save_image_button.grid(row=13, column=0, sticky="w", padx=10, pady=10)
    undo_changes_button = tk.Button(text_window, text="Undo Changes", command=undo_changes)
    undo_changes_button.grid(row=13, column=1, sticky="w", padx=10, pady=10)

    # Stores the widgets as values, so they can be passed to add_text and retrieved via .get()
    # Button widget values aren't passed via this dictionary
    user_text_selections = {
        "angle": text_angle_slider,
        "font": font_menu,
        "font_size": font_size_menu,
        "opacity": opacity_slider,
        "text": text_box,
        "tiling": "single",
        "x": text_x_slider,
        "y": text_y_slider,
    }

# Add Copyright - Changes a copyright attribute of the photo_canvas object, to be referenced in text_options
def add_copyright(text_box):
    text = text_box.get()
    if photo_canvas.copyright == False:
        photo_canvas.copyright = True
        text_box.insert(tk.END, " ©")
    elif photo_canvas.copyright == True:
        text = text.strip(" ©")
        text_box.delete(0, tk.END)
        text_box.insert(0, text)
        photo_canvas.copyright = False


# Adding formatted text - Received from text_options()
def add_text(text_options, current_color, fonts, font_display_names):
    text = text_options["text"].get()
    tiling = text_options["tiling"]
    font = text_options["font"].get()
    x = text_options["x"].get()
    y = text_options["y"].get()
    font_size = int(text_options["font_size"].get().strip("px"))
    angle = int(text_options["angle"].get())
    opacity = text_options["opacity"].get()
    photo_canvas.opacity = opacity
    text_color = (current_color[0], current_color[1], current_color[2], opacity)
    font_index = font_display_names.index(font)
    font_file = ImageFont.truetype(f'fonts/{fonts[font_index]}', size=font_size)

    # Apply tiling

    if tiling == "single":
        new_image = Image.new("RGBA",
                              size=(font_size * int((len(text) + 1) * .6), font_size * int((len(text) + 1) * .6)),
                              color=(0, 0, 0, 0))
        draw = ImageDraw.Draw(new_image)
        draw.text(xy=(new_image.width / 2, new_image.height / 2), text=text, font=font_file, fill=text_color,
                  anchor="mm")
        rotated_image = apply_angle(new_image, angle)
        photo_canvas.watermark_pillow = rotated_image
        updated_image = ImageTk.PhotoImage(rotated_image)
        photo_canvas.watermark_image = updated_image
        photo_canvas.watermark_x = x + ((font_size * .5) * (len(text) / 2))
        photo_canvas.watermark_y = (photo_canvas.winfo_height() - y)
        photo_canvas.watermark_id = photo_canvas.create_image(
            (x + ((font_size * .5) * (len(text) / 2)), (photo_canvas.winfo_height() - y)), image=updated_image)
        create_bounding_box()

    elif tiling == "square":
        tile_width = photo_canvas.winfo_width() * 2
        tile_height = photo_canvas.winfo_height() * 2
        new_image = Image.new("RGBA",
                              size=(tile_width, tile_height),
                              color=(0, 0, 0, 0))
        draw = ImageDraw.Draw(new_image)
        for y in range(0, tile_height, font_size * 5):
            for x in range(0, tile_width, font_size * 5):
                draw.text(xy=(x, y), text=text, font=font_file, fill=text_color, anchor="mm")
        rotated_image = apply_angle(new_image, angle)
        photo_canvas.watermark_pillow = rotated_image
        updated_image = ImageTk.PhotoImage(rotated_image)
        photo_canvas.watermark_image = updated_image
        photo_canvas.watermark_x = (photo_canvas.winfo_width() / 2) - 1
        photo_canvas.watermark_y = (photo_canvas.winfo_height() / 2) - 1
        photo_canvas.watermark_id = photo_canvas.create_image(
            (photo_canvas.winfo_width() / 2), (photo_canvas.winfo_height() / 2), image=updated_image, anchor="center")
        create_bounding_box()
    elif tiling == "diamond":
        slide_line = True
        tile_width = photo_canvas.winfo_width() * 2
        tile_height = photo_canvas.winfo_height() * 3

        new_image = Image.new("RGBA",
                              size=(tile_width, tile_height),
                              color=(0, 0, 0, 0))
        draw = ImageDraw.Draw(new_image)


        for y in range(0, tile_height, font_size * 5):
            if slide_line:
                for x in range(int(font_size * 2.5), tile_width, font_size * 5):
                    draw.text(xy=(x, y), text=text, font=font_file, fill=text_color, anchor="mm")
                slide_line = False
            else:
                for x in range(0, tile_width, font_size * 5):
                    draw.text(xy=(x, y), text=text, font=font_file, fill=text_color, anchor="mm")
                slide_line = True

        rotated_image = apply_angle(new_image, angle)
        photo_canvas.watermark_pillow = rotated_image
        updated_image = ImageTk.PhotoImage(rotated_image)
        photo_canvas.watermark_image = updated_image
        photo_canvas.watermark_x = (photo_canvas.winfo_width() / 2) - 1
        photo_canvas.watermark_y = (photo_canvas.winfo_height() / 2) - 1
        photo_canvas.watermark_id = photo_canvas.create_image(
            photo_canvas.winfo_width() / 2, photo_canvas.winfo_height() / 2, image=updated_image, anchor="center")
        create_bounding_box()

# Drag and drop logo or upload via button
def upload_logo_window():
    if window_dict["watermark_window"]:
        window_dict["watermark_window"].destroy()
        window_dict["watermark_window"] = None
    upload_logo_window = tk.Toplevel(main_window)
    window_dict["upload_logo_window"] = upload_logo_window
    upload_logo_window.minsize(width=500, height=250)
    upload_logo_window.title("Upload Logo")
    drag_label = tk.Label(upload_logo_window, text="Drag your logo here", font=("Arial", 14))
    or_label = tk.Label(upload_logo_window, text="Or", font=("Arial", 10))
    logo_upload = tk.Button(upload_logo_window, text="Upload", command=upload_logo)
    drag_label.grid(row=0, column=0)
    or_label.grid(row=1, column=0)
    logo_upload.grid(row=2, column=0)
    upload_logo_window.drop_target_register(DND_FILES)
    upload_logo_window.dnd_bind('<<Drop>>', lambda event: logo_on_drop(event))
    upload_logo_window.grab_set()

# Uploads logo png
def upload_logo():
    logo_path = tk.filedialog.askopenfilename()
    photo_canvas.logo_path = logo_path
    if logo_path:
        file_type = magic.from_file(logo_path, mime=True)
        if file_type.startswith('image/png'):
            logo = Image.open(logo_path)
            photo_canvas.logo_pillow = logo
            logo_photo = ImageTk.PhotoImage(logo)
            photo_canvas.watermark_image = logo_photo
            photo_canvas.watermark_id = photo_canvas.create_image(0, 0, image=logo_photo, anchor="nw")
            logo_options()
            create_bounding_box()
        else:
            print("Not a valid .png file.")

# Upload logo via drag and drop
def logo_on_drop(event):
    logo_path = event.data.strip("{}")
    photo_canvas.logo_path = logo_path
    if logo_path:
        file_type = magic.from_file(logo_path, mime=True)
        if file_type.startswith('image/png'):
            logo = Image.open(logo_path)
            photo_canvas.logo_pillow = logo
            logo_photo = ImageTk.PhotoImage(logo)
            photo_canvas.watermark_image = logo_photo
            photo_canvas.watermark_id = photo_canvas.create_image(0, 0, image=logo_photo, anchor="nw")
            logo_options()
            create_bounding_box()
        else:
            print("Not a valid .png file.")



# Generates the logo options window - Contains the window's widgets
def logo_options():
    if window_dict["watermark_window"]:
        window_dict["watermark_window"].destroy()
        window_dict["watermark_window"] = None
    if window_dict["upload_logo_window"]:
        window_dict["upload_logo_window"].destroy()
        window_dict["upload_logo_window"] = None
    if window_dict["text_window"]:
        window_dict["text_window"].destroy()
        window_dict["text_window"] = None
    logo_window = tk.Toplevel(main_window)
    logo_window.title("Logo Options")
    logo_window.minsize(width=250, height=600)
    logo_window.grid_columnconfigure(0, weight=1)
    logo_window.grid_columnconfigure(1, weight=1)
    logo_window.grid_columnconfigure(2, weight=1)
    window_dict["logo_window"] = logo_window
    size_label = tk.Label(logo_window, text="Logo Size")
    logo_size_scale = tk.Scale(logo_window, from_=-500, to=500, length=150, orient="horizontal")
    logo_size_scale.set(0)
    size_label.grid(row=0, column=1)
    logo_size_scale.grid(row=1, column=1, padx=50)

    logo_x_label = tk.Label(logo_window, text="X Coordinates")
    logo_x_slider = tk.Scale(logo_window, from_=0, to=photo_canvas.winfo_width(), orient="horizontal", showvalue=False)
    logo_y_label = tk.Label(logo_window, text="Y Coordinates")
    logo_y_slider = tk.Scale(logo_window, from_=0, to=photo_canvas.winfo_height(), orient="horizontal", showvalue=False)
    logo_x_label.grid(row=2, column=1)
    logo_x_slider.grid(row=3, column=1, padx=75)
    logo_y_label.grid(row=4, column=1)
    logo_y_slider.grid(row=5, column=1, padx=75)

    logo_angle_label = tk.Label(logo_window, text="Text Angle")
    logo_angle_slider = tk.Scale(logo_window, from_=-180, to=180, orient="horizontal")
    logo_angle_label.grid(row=6, column=1)
    logo_angle_slider .grid(row=7, column=1)

    single_tile_button = tk.Button(logo_window, text="•", font=(20), width=4, height=2, command=lambda: user_logo_selections.update({"tiling": "single"}))
    square_tile_button = tk.Button(logo_window, text="•   •\n•   •", font=(20), width=4, height=2, command=lambda: user_logo_selections.update({"tiling": "square"}))
    diamond_tile_button = tk.Button(logo_window, text="•\n•       •\n•", font=(20), width=4, height=2, command=lambda: user_logo_selections.update({"tiling": "diamond"}))
    single_tile_button.grid(row=8, column=1, pady=10, sticky="W")
    square_tile_button.grid(row=8, column=1, padx=5, pady=10)
    diamond_tile_button.grid(row=8, column=1, pady=10, sticky="E")
    undo_changes_button = tk.Button(logo_window, text="Undo Changes", command=undo_changes)
    undo_changes_button.grid(row=9, column=1, padx=10, pady=10)
    apply_changes_button = tk.Button(logo_window, text="Apply Changes", command=lambda: edit_logo(user_logo_selections))
    apply_changes_button.grid(row=10, column=1, padx=10, pady=10)

    user_logo_selections = {"angle": logo_angle_slider,
                            "size": logo_size_scale,
                            "tiling": "single",
                            "x": logo_x_slider,
                            "y": logo_y_slider,}

# Applies logo settings
def edit_logo(user_logo_selections):
    angle = user_logo_selections["angle"].get()
    logo_size_scale = user_logo_selections["size"].get()
    tiling = user_logo_selections["tiling"]
    x = user_logo_selections["x"].get()
    y = user_logo_selections["y"].get()
    new_image = Image.open(photo_canvas.logo_path)
    if logo_size_scale > 0:
        logo_size_scale = (logo_size_scale * .01 + 1)
        logo_width, logo_height = new_image.size
        edited_logo_pillow = new_image.resize((int(logo_width * logo_size_scale), int(logo_height * logo_size_scale)), resample=Image.Resampling.BICUBIC)
    elif logo_size_scale < 0:
        logo_size_scale = (abs(logo_size_scale) * .01 + 1)
        logo_width, logo_height = new_image.size
        edited_logo_pillow = new_image.resize((int(logo_width / logo_size_scale), int(logo_height / logo_size_scale)), resample=Image.Resampling.LANCZOS)
    else:
        edited_logo_pillow = new_image

    if tiling == "single":
        rotated_logo = apply_angle(edited_logo_pillow, angle)
        photo_canvas.logo_pillow = rotated_logo
        logo_photo = ImageTk.PhotoImage(rotated_logo)
        photo_canvas.watermark_image = logo_photo
        photo_canvas.watermark_id = photo_canvas.create_image(x, (photo_canvas.winfo_height() - y), image=logo_photo,
                                                              anchor="center")
        create_bounding_box()
    if tiling == "square":
        tile_width = photo_canvas.winfo_width() * 2
        tile_height = photo_canvas.winfo_height() * 2
        tile_image = Image.new("RGBA", size=(tile_width, tile_height), color=(0, 0, 0, 0))
        for y in range(0, tile_height, int(edited_logo_pillow.width * 1.5)):
            for x in range(0, tile_width, int(edited_logo_pillow.width * 1.5)):
                tile_image.paste(edited_logo_pillow, (x, y), edited_logo_pillow)
        rotated_logo = apply_angle(tile_image, angle)
        photo_canvas.logo_pillow = rotated_logo
        logo_photo = ImageTk.PhotoImage(rotated_logo)
        photo_canvas.watermark_image = logo_photo
        photo_canvas.watermark_id = photo_canvas.create_image(0, 0, image=logo_photo,
                                                              anchor="center")
        create_bounding_box()

    elif tiling == "diamond":
        slide_line = True
        tile_width = photo_canvas.winfo_width() * 2
        tile_height = photo_canvas.winfo_height() * 3
        tile_image = Image.new("RGBA", size=(tile_width, tile_height), color=(0, 0, 0, 0))
        for y in range(0, tile_height, int(edited_logo_pillow.width * 1.5)):
            if slide_line:
                for x in range(int(edited_logo_pillow.width * .75), tile_width, int(edited_logo_pillow.width * 1.5)):
                    tile_image.paste(edited_logo_pillow, (x, y), edited_logo_pillow)
                slide_line = False
            else:
                for x in range(0, tile_width, int(edited_logo_pillow.width * 1.5)):
                    tile_image.paste(edited_logo_pillow, (x, y), edited_logo_pillow)
                slide_line = True
        rotated_logo = apply_angle(tile_image, angle)
        photo_canvas.logo_pillow = rotated_logo
        logo_photo = ImageTk.PhotoImage(rotated_logo)
        photo_canvas.watermark_image = logo_photo
        photo_canvas.watermark_id = photo_canvas.create_image(
            (photo_canvas.winfo_width() / 2), (photo_canvas.winfo_height() / 2), image=logo_photo,
            anchor="center")
        create_bounding_box()



# Select a color for text or logo
def select_color():
    global current_color
    color = askcolor()[0]
    current_color = (color[0], color[1], color[2], 255)
    window_dict["text_window"].lift()

# Rotation

def apply_angle(image, angle):
    rotated_image = image.rotate(angle, resample=Image.Resampling.BICUBIC, expand=False)
    return rotated_image

# Drag-And-Drop Text
# Creates the bounding-box used to register clicks
def create_bounding_box():
    if photo_canvas.bbox_id:
        photo_canvas.delete(photo_canvas.bbox_id)
    bbox = photo_canvas.bbox(photo_canvas.image_id)
    if bbox:
        x1, y1, x2, y2 = bbox
        photo_canvas.bbox_id = photo_canvas.create_rectangle(x1, y1, x2, y2, fill="", width=0)
        photo_canvas.tag_bind(photo_canvas.bbox_id, "<B1-Motion>", clicked_text)

# Recognizes when user clicks their mouse within the bounding box and holds the button down
def clicked_text(event):
    photo_canvas.watermark_x = event.x
    photo_canvas.watermark_y = event.x
    if photo_canvas.bbox_id:
        bbox = photo_canvas.bbox(photo_canvas.image_id)
        x1, y1, x2, y2 = bbox
        if event.x >= x1 and event.x <= x2 and event.y >= y1 and event.y <= y2:
            photo_canvas.tag_bind(photo_canvas.bbox_id, "<ButtonRelease-1>", move_clicked_text)

# Moves the text to the new space where the user released their mouse button
def move_clicked_text(event):
    photo_canvas.watermark_x = event.x
    photo_canvas.watermark_y = event.y
    new_watermark_image = photo_canvas.watermark_image
    photo_canvas.delete(photo_canvas.watermark_id)
    photo_canvas.watermark_id = photo_canvas.create_image(event.x, event.y, image=new_watermark_image)
    create_bounding_box()
    if window_dict["text_window"]:
        window_dict["text_window"].lift()
    elif window_dict["logo_window"]:
        window_dict["logo_window"].lift()

# Undo Changes
def undo_changes():
    try:
        photo_canvas.delete(photo_canvas.watermark_id)
        photo_canvas.delete(photo_canvas.bbox_id)
    except AttributeError:
        pass


# Save watermarked image
def save_watermarked_image():
    background = photo_canvas.pillow_image.convert("RGBA")
    watermarked_image = background.copy().convert("RGBA")
    watermark = photo_canvas.watermark_pillow
    x = int(photo_canvas.watermark_x)
    y = int(photo_canvas.watermark_y)
    watermarked_image.paste(watermark,
                            ((x - watermark.width // 2) - 1, (y - watermark.height // 2) - 1), watermark)
    save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[(".png", "*.png"),
                                                                                 (".jpg", "*.jpg*"),
                                                                                 (".jpeg", "*.jpeg")])

    watermarked_image.save(save_path)


# Main App - Components
my_label = tk.Label(text="Carl's Watermark App", font=("Arial", 24, "bold"))
landscape_image = Image.open("./sunset-golden.jpg")
landscape_width, landscape_height = landscape_image.size
landscape_photo = ImageTk.PhotoImage(landscape_image)
drag_label = tk.Label(text="Drag your image", font=("Arial", 18))
or_label = tk.Label(text="Or", font=("Arial", 12))
photo_canvas = tk.Canvas(bg=None, width=landscape_width, height=landscape_height)
upload_button = tk.Button(text="Upload", font=("Arial", 14), command=lambda: upload_image(photo_canvas))
photo_canvas.image_id = photo_canvas.create_image(photo_canvas.winfo_width() / 2, photo_canvas.winfo_height() / 2, image=landscape_photo, anchor="nw")
photo_canvas.bbox_id = None
photo_canvas.copyright = False

# Main App - Grid
my_label.grid(column=1, row=0)
drag_label.grid(column=1, row=2)
or_label.grid(column=1, row=3)
upload_button.grid(column=1, row=4)
photo_canvas.grid(column=1, row=5)


main_window.drop_target_register(DND_FILES)
main_window.dnd_bind('<<Drop>>', lambda event: on_drop(event, photo_canvas))
main_window.mainloop()