import customtkinter
import os
import threading
import time
import hashlib

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

ANTIVIRUS_DATABASE = {
    "WannaCry": {
        "md5": "e6f91ff771d39df4642a8d03b7a6ed6d",
        "sha1": "60c92b271456ac5e64b0b2306b7b63e97b5e4c91",
        "sha256": "db349b97c37d22f5ea1d1841e3c89eb4fc1f16f654f6e729b1f03cbb3d8e1b55"
    },
    "Petya/NotPetya": {
        "md5": "71b6a493388e7d0b40c83ce903bc6b04",
        "sha1": "392b7f45a6e59ebfd6dc7b38ecbdd21b41959b45",
        "sha256": "027f9f3d2aa8f3ec56e8f1f953ed7e6db88e41fcfb5b2b03a1cd700afc5fa2f8"
    },
    "Zeus": {
        "md5": "2b9931ad7df285d9742dbb96f5f33196",
        "sha1": "b6a3f4cc044b24518b9b94f5cf019dedb8671047",
        "sha256": ""
    }
}

class AntivirusApp(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("VinApp")
        self.geometry(f"{1100}x580")
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Antivirus", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.scan_button = customtkinter.CTkButton(self.sidebar_frame, text="Scan Entire Computer", command=self.start_scan)
        self.scan_button.grid(row=1, column=0, padx=20, pady=10)

        self.exit_button = customtkinter.CTkButton(self.sidebar_frame, text="Exit", command=self.exit_app)
        self.exit_button.grid(row=2, column=0, padx=20, pady=10)

        self.textbox = customtkinter.CTkTextbox(self, width=800, height=400)
        self.textbox.grid(row=0, column=1, columnspan=3, padx=(20, 20), pady=(20, 20), sticky="nsew")
        self.textbox.insert("0.0", "Log output:\n")

        self.progressbar = customtkinter.CTkProgressBar(self)
        self.progressbar.grid(row=1, column=1, columnspan=3, padx=(20, 20), pady=(20, 20), sticky="ew")
        self.progressbar.set(0)

        self.loading_label = customtkinter.CTkLabel(self, text="", font=("Arial", 16))
        self.loading_label.grid(row=2, column=1, columnspan=3, padx=(20, 20), pady=(10, 10), sticky="nsew")

    def start_scan(self):
        threading.Thread(target=self.scan_files).start()
        threading.Thread(target=self.animate_loading).start()

    def scan_files(self):
        self.textbox.insert("end", "Scanning all files...\n")
        root_dirs = ['C:/'] if os.name == 'nt' else ['/']
        total_files = 0
        scanned_files = 0

        for root in root_dirs:
            for _, _, filenames in os.walk(root):
                total_files += len(filenames)

        try:
            for root in root_dirs:
                for dirpath, _, filenames in os.walk(root):
                    for file in filenames:
                        filepath = os.path.join(dirpath, file)
                        scanned_files += 1
                        self.progressbar.set(scanned_files / total_files)

                        try:
                            file_hashes = self.get_file_hashes(filepath)
                            for threat_name, hashes in ANTIVIRUS_DATABASE.items():
                                if (file_hashes['md5'] == hashes['md5'] or
                                    file_hashes['sha1'] == hashes['sha1'] or
                                    file_hashes['sha256'] == hashes['sha256']):
                                    self.textbox.insert("end", f"Threat detected ({threat_name}): {filepath}\n")
                        except Exception as e:
                            self.textbox.insert("end", f"Error scanning {filepath}: {e}\n")
        except Exception as e:
            self.textbox.insert("end", f"Critical error: {e}\n")

        self.textbox.insert("end", "Scanning complete.\n")
        self.progressbar.set(1)
        self.loading_label.configure(text="Scan Complete!")

    def get_file_hashes(self, filepath):
        hashes = {
            'md5': hashlib.md5(),
            'sha1': hashlib.sha1(),
            'sha256': hashlib.sha256()
        }
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hashes['md5'].update(chunk)
                hashes['sha1'].update(chunk)
                hashes['sha256'].update(chunk)

        return {key: h.hexdigest() for key, h in hashes.items()}

    def animate_loading(self):
        animation_frames = ["|", "/", "-", "\\"]
        while self.progressbar.get() < 1:
            for frame in animation_frames:
                if self.progressbar.get() >= 1:
                    break
                self.loading_label.configure(text=f"Scanning... {frame}")
                time.sleep(0.2)

    def exit_app(self):
        self.destroy()

if __name__ == "__main__":
    app = AntivirusApp()
    app.mainloop()
