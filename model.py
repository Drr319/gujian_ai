import torch
import torch.nn as nn
from torchvision import models

class GuJianModel(nn.Module):
    def __init__(self):
        super().__init__()
        # 主干网络
        self.backbone = models.mobilenet_v2(weights=models.MobileNet_V2_Weights.DEFAULT)
        self.backbone = nn.Sequential(*list(self.backbone.children())[:-1])
        
        # 直接把 62720 维映射到 1280 维，适配当前输出
        self.fc_adapt = nn.Linear(62720, 1280)

        # 三个任务的全连接层
        self.moisture_fc = nn.Sequential(nn.Linear(1280, 1), nn.Sigmoid())
        self.erosion_fc = nn.Sequential(nn.Linear(1280, 3))
        self.water_fc = nn.Sequential(nn.Linear(1280, 3))

    def forward(self, x):
        x = self.backbone(x)
        x = x.flatten(1)  # 展平成 [batch, 62720]
        x = self.fc_adapt(x)  # 变成 [batch, 1280]
        moisture = self.moisture_fc(x) * 100
        erosion = self.erosion_fc(x)
        water = self.water_fc(x)
        return moisture, erosion, water