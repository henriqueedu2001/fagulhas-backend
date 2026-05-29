from pathlib import Path

FILES_PATH = 'files'

async def save_file_from_endpoint(file: bytes, filename: str) -> Path:
    save_dir = Path(FILES_PATH)
    save_dir.mkdir(exist_ok=True)

    file_path = save_dir / f'{filename}'

    # reads the file and writes it chunk by chunk
    with open(file_path, 'wb') as f:
        while chunk := await file.read(1024 * 1024):  # 1MB
            f.write(chunk)

    await file.close()

    return file_path


def get_file_extension(file: bytes):
    ext = Path(file.filename).suffix
    ext = ext[1:]
    return ext