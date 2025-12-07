import os
import time
import shutil
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


# 🧠 Custom Event Handler Class
class FileSorterHandler(FileSystemEventHandler):
    def __init__(self, folder_to_track):
        self.folder_to_track = folder_to_track

    def on_modified(self, event):
        # Triggered when files are added or modified
        for filename in os.listdir(self.folder_to_track):
            file_path = os.path.join(self.folder_to_track, filename)

            if os.path.isfile(file_path):
                file_extension = Path(filename).suffix.lower().replace('.', '')
                if not file_extension:
                    file_extension = "no_extension"

                # Create destination folder (e.g., "PDFs", "Images")
                destination_folder = os.path.join(self.folder_to_track, file_extension.upper())
                os.makedirs(destination_folder, exist_ok=True)

                # Move file to the correct folder
                new_path = os.path.join(destination_folder, filename)
                try:
                    shutil.move(file_path, new_path)
                    print(f"✅ Moved: {filename} → {destination_folder}")
                except Exception as e:
                    print(f"⚠️ Could not move {filename}: {e}")


def start_file_sorter(folder_to_track):
    print(f"🚀 Smart File Sorter is now monitoring: {folder_to_track}")
    event_handler = FileSorterHandler(folder_to_track)
    observer = Observer()
    observer.schedule(event_handler, folder_to_track, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(2)
    except KeyboardInterrupt:
        observer.stop()
        print("\n🛑 Stopped File Sorter.")
    observer.join()


if __name__ == "__main__":
    # 🧭 Ask user for folder path
    folder_path = input("📂 Enter the folder path to monitor (e.g., C:\\Users\\YourName\\Downloads): ").strip()

    if not os.path.exists(folder_path):
        print("❌ Folder does not exist. Please check the path.")
    else:
        start_file_sorter(folder_path)
