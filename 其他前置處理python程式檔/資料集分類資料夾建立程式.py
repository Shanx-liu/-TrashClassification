import os
import random
from PIL import Image
from shutil import copyfile

# ======== 可調整參數 ========
RAW_DIR = "資料集檔案庫(原)"                      # 原始資料集資料夾
OUTPUT_DIR = "資料集檔案庫(改)"                    # 輸出資料集資料夾
TARGET_SIZE = (224, 224)                  # Resize 大小
SPLIT_RATIO = (0.7, 0.2, 0.1)             # train / val / test 比例
EXT = [".jpg", ".jpeg", ".png"]           # 支援的圖片格式
# =================================


def make_dirs():
    """建立 train/val/test 資料夾結構"""
    categories = os.listdir(RAW_DIR)
    for split in ["train", "val", "test"]:
        for cat in categories:
            path = os.path.join(OUTPUT_DIR, split, cat)
            os.makedirs(path, exist_ok=True)


def resize_and_save(img_path, dst_path):
    """將圖片 resize 後存入目標路徑"""
    img = Image.open(img_path).convert("RGB")
    img = img.resize(TARGET_SIZE)
    img.save(dst_path)


def main():
    print("🚀 開始整理資料集...")

    make_dirs()

    categories = os.listdir(RAW_DIR)

    for cat in categories:
        cat_path = os.path.join(RAW_DIR, cat)
        images = [f for f in os.listdir(cat_path) if os.path.splitext(f)[1].lower() in EXT]
        random.shuffle(images)

        total = len(images)
        train_end = int(total * SPLIT_RATIO[0])
        val_end = train_end + int(total * SPLIT_RATIO[1])

        train_files = images[:train_end]
        val_files = images[train_end:val_end]
        test_files = images[val_end:]

        # --- 處理 train ---
        for f in train_files:
            src = os.path.join(cat_path, f)
            dst = os.path.join(OUTPUT_DIR, "train", cat, f)
            resize_and_save(src, dst)

        # --- 處理 val ---
        for f in val_files:
            src = os.path.join(cat_path, f)
            dst = os.path.join(OUTPUT_DIR, "val", cat, f)
            resize_and_save(src, dst)

        # --- 處理 test ---
        for f in test_files:
            src = os.path.join(cat_path, f)
            dst = os.path.join(OUTPUT_DIR, "test", cat, f)
            resize_and_save(src, dst)

        print(f"✔ 類別 {cat} 處理完成：共 {total} 張")

    print("\n 好了！你的資料集已全部整理完成！")


if __name__ == "__main__":
    main()
