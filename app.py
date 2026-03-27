import streamlit as st
from PIL import Image
import torch
from model import GuJianModel
from utils import load_image

# 页面标题
st.title("🏯 古庙古建含水率测定仪")
st.markdown("---")

# 上传图片组件
uploaded_file = st.file_uploader("📸 选择一张古建图片（支持 jpg/jpeg/png）", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # 显示上传的图片（用新版无警告写法，适配容器宽度）
    image = Image.open(uploaded_file)
    st.image(image, caption="你上传的古建图片", use_container_width=True)
    st.markdown("---")

    # 加载训练好的模型
    @st.cache_resource
    def load_model():
        model = GuJianModel()
        # 替换为你实际的模型文件名
        model.load_state_dict(torch.load("gujian_model.pth", map_location="cpu"))
        model.eval()
        return model

    model = load_model()

    # 保存临时图片文件
    with open("temp_test.jpg", "wb") as f:
        f.write(uploaded_file.getbuffer())

    # 图片预处理 + 模型推理（已移除is_train参数）
    img = load_image("temp_test.jpg")
    with torch.no_grad():
        moisture_pred, erosion_pred, water_pred = model(img)

    # --- 核心修复：约束含水率到国标合理范围（0%~60%）---
    moisture_pct = round(moisture_pred.item() * 100, 1)
    # 限制在0%~60%之间，符合古建木材国标要求
    moisture_pct = max(min(moisture_pct, 60.0), 0.0)

    # 解析其他结果
    erosion_labels = ["无虫洞侵蚀", "轻微虫洞侵蚀", "严重虫洞侵蚀"]
    erosion_cls = erosion_labels[erosion_pred.argmax().item()]
    
    water_labels = ["防水良好", "防水一般", "防水存在隐患"]
    water_cls = water_labels[water_pred.argmax().item()]

    # 可视化展示结果
    st.subheader("📊 古建健康分析结果")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="💧 含水率（国标约束）", value=f"{moisture_pct}%")
    with col2:
        st.metric(label="🐜 虫洞侵蚀", value=erosion_cls)
    with col3:
        st.metric(label="🛡️ 防水防潮", value=water_cls)

    st.markdown("---")
    st.info("💡 提示：这是基于AI模型的预测结果，实际情况请结合专业检测。\n（含水率已约束在0%~60%国标合理区间）")
else:
    st.info("👆 请先上传一张古建图片开始分析")