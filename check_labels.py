import pandas as pd
import os

def check_labels_csv():
    # 1. 检查文件是否存在
    csv_path = "labels.csv"
    if not os.path.exists(csv_path):
        print("❌ 错误：labels.csv 文件不存在！")
        return

    # 2. 读取 CSV 文件
    try:
        df = pd.read_csv(csv_path)
        print("✅ 成功读取 labels.csv")
    except Exception as e:
        print(f"❌ 读取失败：{e}")
        return

    # 3. 检查列名是否正确
    required_cols = ["img_name", "moisture", "erosion", "waterproof"]
    if not all(col in df.columns for col in required_cols):
        print(f"❌ 列名错误！需要：{required_cols}，当前列名：{list(df.columns)}")
        return
    print("✅ 列名格式正确")

    # 4. 检查图片文件是否存在（假设图片在 data/train/ 下）
    img_dir = os.path.join("data", "train")
    if not os.path.exists(img_dir):
        print("⚠️  警告：data/train/ 文件夹不存在，无法验证图片路径")
        return

    missing_imgs = []
    for img_name in df["img_name"]:
        img_path = os.path.join(img_dir, img_name)
        if not os.path.exists(img_path):
            missing_imgs.append(img_name)

    if missing_imgs:
        print(f"⚠️  发现 {len(missing_imgs)} 张图片不存在：")
        for img in missing_imgs:
            print(f"  - {img}")
    else:
        print("✅ 所有图片文件都存在！")

    # 5. 打印基本统计信息
    print("\n📊 数据统计：")
    print(f"总样本数：{len(df)}")
    print(f"moisture 范围：{df['moisture'].min():.1f} ~ {df['moisture'].max():.1f}")
    print(f"erosion 取值：{sorted(df['erosion'].unique())}")
    print(f"waterproof 取值：{sorted(df['waterproof'].unique())}")

if __name__ == "__main__":
    check_labels_csv()