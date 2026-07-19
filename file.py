from pathlib import Path
import json
from datetime import datetime

ASSET_EXTENSIONS = {
    ".xmf": "Mesh",
    ".xsf": "Skeleton",
    ".xaf": "Animation",
    ".xrf": "Material",
    ".png": "Texture",
    ".jpg": "Texture",
    ".jpeg": "Texture",
    ".xml": "Config/XML",
    ".ogg": "Audio",
}

def scan_assets(folder_path: str):
    root = Path(folder_path).expanduser().resolve()

    if not root.exists() or not root.is_dir():
        raise ValueError("Folder tidak ditemukan atau bukan direktori valid.")

    assets = []

    for file in root.rglob("*"):
        if not file.is_file():
            continue

        ext = file.suffix.lower()
        asset_type = ASSET_EXTENSIONS.get(ext)

        if not asset_type:
            continue

        stat = file.stat()

        assets.append({
            "name": file.name,
            "path": str(file.relative_to(root)),
            "type": asset_type,
            "extension": ext,
            "size_bytes": stat.st_size,
            "modified_at": datetime.fromtimestamp(stat.st_mtime).isoformat(timespec="seconds"),
        })

    return assets

def save_report(assets, output_file="asset_report.json"):
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(assets, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    folder = input("Masukkan path folder project IMVU kamu: ").strip()

    try:
        assets = scan_assets(folder)
        save_report(assets)

        print(f"Berhasil scan {len(assets)} asset.")
        print("Laporan disimpan ke asset_report.json")

        by_type = {}
        for asset in assets:
            by_type[asset["type"]] = by_type.get(asset["type"], 0) + 1

        print("\nRingkasan:")
        for asset_type, count in sorted(by_type.items()):
            print(f"- {asset_type}: {count}")

    except Exception as e:
        print(f"Error: {e}")
