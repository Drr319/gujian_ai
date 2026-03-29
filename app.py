import streamlit as st
import random
from PIL import Image

# --------------------------
# 模拟模型加载（替代真实模型文件）
# --------------------------
def load_model():
    def dummy_predict(img):
        # 生成符合国标 GB/T 50165-2020 的含水率（12%~18%）
        moisture = round(random.uniform(12.0, 18.0), 2)
        # 随机生成虫洞侵蚀等级
        erosion_level = random.choice(["轻微侵蚀", "中等侵蚀", "严重侵蚀"])
        # 生成防水防潮评估
        if moisture < 14:
            waterproof = "良好（符合古建筑防潮标准）"
        elif moisture < 16:
            waterproof = "一般（建议加强通风、定期检查）"
        else:
            waterproof = "较差（需立即做防水防潮处理）"
        return {
            "含水率(%)": moisture,
            "虫洞侵蚀状况": erosion_level,
            "防水防潮评估": waterproof
        }
    return dummy_predict

# 加载模型
model = load_model()

# --------------------------
# Streamlit 页面主逻辑
# --------------------------
st.set_page_config(page_title="古建筑健康分析", page_icon="🏯")
st.title("🏯 古建筑健康情况分析")

st.markdown("""
**功能说明**：
- 上传古建筑（柱子、榫卯等）图片
- 自动分析含水率（符合国标 12%~18%）
- 评估虫洞侵蚀与防水防潮状况
""")

# 上传图片
uploaded_file = st.file_uploader("选择图片文件", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    # 显示图片
    img = Image.open(uploaded_file)
    st.image(img, caption="你上传的古建筑图片", use_column_width=True)
    
    # 分析按钮
    if st.button("🔍 开始健康分析"):
        with st.spinner("正在分析图片..."):
            result = model(uploaded_file)
            
            st.subheader("📊 分析结果（符合 GB/T 50165-2020）")
            st.json(result)
            
            st.success("""
✅ 分析完成！
- 含水率结果符合《古建筑木结构维护与加固技术规范》
- 虫洞侵蚀与防水防潮建议可作为维护参考
""")

st.markdown("---")
st.caption("© 2026 古建筑健康分析工具 | 数据为模拟演示，实际检测请结合专业勘察")