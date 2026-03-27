import torch
from model import GuJianModel
from utils import load_image

model = GuJianModel()
model.load_state_dict(torch.load("gujian_model.pth", map_location="cpu"))
model.eval()

img = load_image("test.jpg")

with torch.no_grad():
    moisture, erosion, water = model(img)

moisture_val = moisture.item()
erosion_cls = torch.argmax(erosion).item()
water_cls = torch.argmax(water).item()

erosion_map = ["无虫洞侵蚀", "轻微侵蚀", "严重侵蚀"]
water_map = ["防水良好", "防水一般", "防水较差"]

print("="*40)
print("        古建图像AI分析结果")
print("="*40)
print(f"含水量：{moisture_val:.1f}%")
print(f"虫洞侵蚀：{erosion_map[erosion_cls]}")
print(f"防水防潮：{water_map[water_cls]}")
print("="*40)