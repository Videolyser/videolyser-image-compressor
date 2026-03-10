from pathlib import Path
import shutil
import webbrowser
import customtkinter as ctk
from PIL import Image


ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


class ImageCompressorApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Videolyser Image Compressor v1.0")
        self.geometry("520x470")
        self.resizable(False, False)

        self.base_dir = Path(__file__).parent
        self.output_dir = self.base_dir / "output"
        self.processed_dir = self.base_dir / "processed"

        self.setup_ui()

    def setup_ui(self):
        self.title_label = ctk.CTkLabel(
            self,
            text="Image Compressor",
            font=("Arial", 22, "bold")
        )
        self.title_label.pack(pady=(20, 15))

        self.width_entry = self.create_input("Maximum width (pixels):", "1280")

        self.format_label = ctk.CTkLabel(self, text="Output format:", font=("Arial", 12))
        self.format_label.pack(padx=30, anchor="w")

        self.format_option = ctk.CTkSegmentedButton(self, values=["WEBP", "JPEG", "PNG"])
        self.format_option.pack(pady=(0, 15), padx=30, fill="x")
        self.format_option.set("WEBP")

        self.quality_label = ctk.CTkLabel(self, text="Quality: 75%", font=("Arial", 12))
        self.quality_label.pack(padx=30, anchor="w")

        self.quality_slider = ctk.CTkSlider(self, from_=1, to=100, command=self.update_quality_label)
        self.quality_slider.pack(pady=(0, 20), padx=30, fill="x")
        self.quality_slider.set(75)

        self.start_btn = ctk.CTkButton(
            self,
            text="PROCESS ALL IMAGES",
            font=("Arial", 14, "bold"),
            height=50,
            fg_color="#27AE60",
            hover_color="#219150",
            command=self.process_images
        )
        self.start_btn.pack(pady=15, padx=30, fill="x")

        self.status_label = ctk.CTkLabel(self, text="Ready.", text_color="gray")
        self.status_label.pack(pady=10)

        self.info_label = ctk.CTkLabel(
            self,
            text="Supported formats: JPG, JPEG, PNG, WEBP, BMP, TIF, TIFF\nCompressed files go to output. Originals move to processed.",
            font=("Arial", 11),
            text_color="gray",
            justify="center"
        )
        self.info_label.pack(pady=(0, 10))

        self.link_button = ctk.CTkButton(
            self,
            text="videolyser.de",
            font=("Arial", 11, "underline"),
            fg_color="transparent",
            hover_color=("gray85", "gray20"),
            text_color=("#1f6aa5", "#6aa6ff"),
            width=120,
            height=28,
            command=self.open_website
        )
        self.link_button.pack(pady=(0, 12))

    def create_input(self, label_text, default_val):
        label = ctk.CTkLabel(self, text=label_text, font=("Arial", 12))
        label.pack(padx=30, anchor="w")

        entry = ctk.CTkEntry(self, height=35)
        entry.pack(pady=(0, 10), padx=30, fill="x")
        entry.insert(0, default_val)
        return entry

    def update_quality_label(self, value):
        self.quality_label.configure(text=f"Quality: {int(value)}%")

    def open_website(self):
        webbrowser.open("https://www.videolyser.de/")

    def find_images(self):
        allowed_extensions = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tif", ".tiff"}
        return [
            file_path
            for file_path in self.base_dir.iterdir()
            if file_path.is_file() and file_path.suffix.lower() in allowed_extensions
        ]

    def process_images(self):
        image_list = self.find_images()
        image_count = len(image_list)

        if image_count == 0:
            self.status_label.configure(
                text="No images found in the app folder.",
                text_color="#E74C3C"
            )
            return

        self.output_dir.mkdir(exist_ok=True)
        self.processed_dir.mkdir(exist_ok=True)

        try:
            max_width = int(self.width_entry.get())
            output_format = self.format_option.get().lower()
            quality = int(self.quality_slider.get())

            for index, image_path in enumerate(image_list, start=1):
                self.status_label.configure(
                    text=f"Processing image {index}/{image_count}: {image_path.name}",
                    text_color="white"
                )
                self.update()

                img = Image.open(image_path)

                if img.width > max_width:
                    new_height = int(img.height * (max_width / img.width))
                    img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)

                if output_format == "jpeg" and img.mode in ("RGBA", "P"):
                    img = img.convert("RGB")

                output_filename = f"{image_path.stem}.{output_format}"
                output_path = self.output_dir / output_filename

                save_kwargs = {"optimize": True}

                if output_format in ("jpeg", "webp"):
                    save_kwargs["quality"] = quality

                img.save(output_path, output_format.upper(), **save_kwargs)

                shutil.move(str(image_path), str(self.processed_dir / image_path.name))

            self.status_label.configure(
                text=f"Done. {image_count} image(s) processed successfully.",
                text_color="#2ECC71"
            )

        except ValueError:
            self.status_label.configure(
                text="Please enter a valid number for maximum width.",
                text_color="#E74C3C"
            )
        except Exception as error:
            self.status_label.configure(
                text=f"Error: {error}",
                text_color="#E74C3C"
            )


if __name__ == "__main__":
    app = ImageCompressorApp()
    app.mainloop()
