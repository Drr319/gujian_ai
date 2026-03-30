import streamlit as st
import os
import requests
from pathlib import Path

# -------------------------- 模型自动下载逻辑 --------------------------
MODEL_PATH = "gujian_model.pth"
# 👇 这里替换成你的123云盘分享链接
MODEL_URL = "https://www.123865.com/s/m6USvd-sR9Lh"

if not Path(MODEL_PATH).exists():
    st.info("首次运行，正在下载模型文件，请耐心等待...")
    try:
        response = requests.get(MODEL_URL, stream=True, timeout=600)
        response.raise_for_status()
        total_size = int(response.headers.get('content-length', 0))
        progress_bar = st.progress(0)
        
        with open(MODEL_PATH, "wb") as f:
            for idx, chunk in enumerate(response.iter_content(chunk_size=8192)):
                f.write(chunk)
                if total_size > 0:
                    progress = min(100, int((idx * 8192 / total_size) * 100))
                    progress_bar.progress(progress)
        st.success("模型下载完成！")
    except Exception as e:
        st.error(f"模型下载失败：{e}")
        st.info("请检查网络或分享链接是否有效")
# ---------------------------------------------------------------------

# 你原来的代码从这里开始，完全不动！
import time

def main():
    st.title("🏛️ 古建 AI 智能保护系统")
    st.markdown("---")

    # 左侧菜单（核心功能入口）
    with st.sidebar:
        st.title("📋 功能菜单")
        option = st.radio(
            "请选择功能：",
            ("古建筑监测", "防水防潮评估", "文物保护数据分析", "结构安全扫描")
        )

    # 首页介绍
    if option is None:
        st.subheader("🔴 系统说明")
        st.write("本系统用于古建筑保护、文物监测、安全评估、防水防潮评估等场景。")

        st.subheader("🔴 使用方法")
        st.code("""
1. 双击启动项目 (run.bat)
2. 浏览器打开 localhost:8501
3. 使用左侧菜单进行功能操作
""")

        st.subheader("🔴 核心功能")
        st.markdown("""
- ✅ 古建筑监测
- ✅ 防水防潮评估
- ✅ 文物保护数据分析
- ✅ 结构安全扫描
""")
        st.markdown("---")
        st.success("✅ 系统启动完成，可正常使用！")
        return

    # 功能页面：图片上传 + 测评
    st.subheader(f"📸 {option}")
    uploaded_file = st.file_uploader("请上传古建筑图片", type=["png", "jpg", "jpeg"])

    if uploaded_file is not None:
        st.image(uploaded_file, caption="上传的图片", use_column_width=True)
        st.info("🔍 正在进行AI分析，请稍候...")
        time.sleep(2)
        st.success(f"📊 {option} 完成！")
        st.write("**分析结果示例：**")
        st.write("- 含水率：12.5%（符合国家标准）")
        st.write("- 虫洞侵蚀：无明显侵蚀痕迹")
        st.write("- 防水防潮性能：良好")

if __name__ == "__main__":
    main()