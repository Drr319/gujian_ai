import torch
import torch.nn as nn
import torch.optim as optim
from model import GuJianModel

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = GuJianModel().to(device)

loss_moisture = nn.MSELoss()
loss_cls = nn.CrossEntropyLoss()
optimizer = optim.AdamW(model.parameters(), lr=1e-4)

print("开始训练...")
model.train()
for epoch in range(5):
    total_loss = 0.0
    for i in range(10):
        img = torch.randn(8, 3, 224, 224).to(device)
        m_label = torch.rand(8, 1).to(device) * 100
        e_label = torch.randint(0, 3, (8,)).to(device)
        w_label = torch.randint(0, 3, (8,)).to(device)

        optimizer.zero_grad()
        m_pred, e_pred, w_pred = model(img)
        loss = loss_moisture(m_pred, m_label) + loss_cls(e_pred, e_label) + loss_cls(w_pred, w_label)
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
    print(f"Epoch {epoch+1}, 平均损失: {total_loss/10:.4f}")

torch.save(model.state_dict(), "gujian_model.pth")
print("训练完成！模型已保存为 gujian_model.pth")