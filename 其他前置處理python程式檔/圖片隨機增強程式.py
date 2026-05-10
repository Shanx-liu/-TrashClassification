import os
import random
from PIL import Image, ImageOps, ImageDraw

# === 參數設定 ===
input_dir = "照明光源"      # 原始圖片資料夾
output_dir = "照明光源(增強)" # 輸出資料夾
augment_per_image = 5           # 每張圖要產生幾張增強版

os.makedirs(output_dir, exist_ok=True)

def random_flip(img):
    """隨機水平 / 垂直翻轉"""
    if random.random() < 0.5:
        img = ImageOps.mirror(img)
    if random.random() < 0.5:
        img = ImageOps.flip(img)
    return img

def random_rotate(img):
    """隨機旋轉 -30 到 30 度"""
    angle = random.uniform(-30, 30)
    return img.rotate(angle, expand=True)

def random_crop(img):
    """隨機裁切掉 10%-30% 的邊界"""
    w, h = img.size
    crop_ratio = random.uniform(0.1, 0.3)
    left = random.uniform(0, w * crop_ratio)
    top = random.uniform(0, h * crop_ratio)
    right = random.uniform(w * (1 - crop_ratio), w)
    bottom = random.uniform(h * (1 - crop_ratio), h)
    return img.crop((left, top, right, bottom)).resize((w, h))

def random_erasing(img):
    """隨機遮擋 (random erasing)"""
    w, h = img.size
    erase_w = int(w * random.uniform(0.05, 0.2))
    erase_h = int(h * random.uniform(0.05, 0.2))

    x = random.randint(0, w - erase_w)
    y = random.randint(0, h - erase_h)

    draw = ImageDraw.Draw(img)
    color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
    draw.rectangle((x, y, x + erase_w, y + erase_h), fill=color)

    return img

def augment_image(img):
    """流程：隨機翻轉 → 隨機旋轉 → 隨機裁切 → 隨機遮擋"""
    img = random_flip(img)
    img = random_rotate(img)
    img = random_crop(img)
    img = random_erasing(img)
    return img

# === 主程式 ===
for filename in os.listdir(input_dir):
    if filename.lower().endswith((".jpg", ".png", ".jpeg", ".bmp")):
        img_path = os.path.join(input_dir, filename)
        img = Image.open(img_path).convert("RGB")

        for i in range(augment_per_image):
            aug_img = augment_image(img.copy())
            save_name = f"{os.path.splitext(filename)[0]}_aug_{i}.jpg"
            aug_img.save(os.path.join(output_dir, save_name))

print("資料增強完成！")
