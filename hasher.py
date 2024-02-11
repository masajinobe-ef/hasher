import os
from tkinter import Tk, filedialog
import hashlib

# Расширения файлов изображений и форматы KiCad
IMAGE_EXTENSIONS = ['.png', '.jpg', '.jpeg', '.bmp', '.gif', '.svg']
KICAD_FORMATS = ['.kicad_pcb', '.kicad_mod', '.kicad_sch']
ARCHIVE_FORMATS = ['.zip', '.tar', '.gz', '.rar', '.7z']
INI_FILES = ['.ini']
IGNORED_FILENAMES = ['fp-info-cache']


# Функция для выбора папки через диалоговое окно
def choose_directory():
    root = Tk()
    root.withdraw()  # скрыть главное окно

    folder_selected = filedialog.askdirectory()
    return folder_selected


# Функция для вычисления SHA-256 хеша файла
def calculate_sha256(file_path):
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        # Считываем блоками для эффективности
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


# Функция для обхода директории рекурсивно
def walk_directory(directory):
    files_hashes = {}

    for root, dirs, files in os.walk(directory):
        # Исключаем скрытые папки
        dirs[:] = [d for d in dirs if not d.startswith('.')]

        for file_name in files:
            file_path = os.path.join(root, file_name)
            _, file_extension = os.path.splitext(file_name)

            # Игнорируем файлы изображений, форматы KiCad, архивы, ini файлы
            # и файлы с определенными именами
            if file_extension.lower() not in IMAGE_EXTENSIONS and \
               file_extension.lower() not in KICAD_FORMATS and \
               file_extension.lower() not in ARCHIVE_FORMATS and \
               file_extension.lower() not in INI_FILES and \
               file_name not in IGNORED_FILENAMES:
                file_hash = calculate_sha256(file_path)
                files_hashes[file_path] = file_hash

    return files_hashes


# Основная функция
def main():
    folder_path = choose_directory()
    if folder_path:
        files_hashes = walk_directory(folder_path)

        # Найти сходящиеся хеши
        unique_hashes = set(files_hashes.values())
        for hash_value in unique_hashes:
            matching_files = [file_path for file_path, file_hash
                              in files_hashes.items()
                              if file_hash == hash_value]
            if len(matching_files) > 1:
                print(f"Сходятся хеши {hash_value} в следующих файлах:")
                for file_path in matching_files:
                    print(file_path)


if __name__ == "__main__":
    main()
