import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# 1. 科技感 UI 配置
st.set_page_config(page_title="游戏项目核心看板", layout="wide")

st.markdown("""
    <style>
    .stApp { background: #0e1117; color: #ffffff; }
    [data-metric-container] {
        background: #1c2128;
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 20px;
    }
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# 2. 核心功能：允许用户上传自己的 Excel/CSV 存档
with st.sidebar:
    st.title("💾 存档管理")
    uploaded_file = st.file_uploader("导入已有数据", type=["csv", "xlsx"])
    st.markdown("---")
    st.info("使用说明：在下方表格修改数据后，点击左侧按钮下载保存。下次使用可在此处重新上传。")

# 3. 初始化数据 (如果没有上传，则使用默认的 35 个项目)
if uploaded_file is not None:
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)
else:
    # 这里的模拟数据你可以替换成你真实的 35 条数据
    np.random.seed(42)
    data = {
        "项目名称": [f"项目 {i}" for i in range(1, 36)],
        "1月营收": np.random.randint(50, 100, 35) * 1000000,
        "12月营收": np.random.randint(50, 100, 35) * 1000000,
        "12月DAU": np.random.randint(10, 50, 35) * 100000,
    }
    df = pd.DataFrame(data)

# 4. 标题与 KPI（1:1 复刻图 22）
st.markdown("### 📊 游戏项目核心数据看板")
c1, c2, c3 = st.columns(3)
c1.metric("累计充值", "454.14M ₹", "-8.8%", delta_color="inverse")
c2.metric("累计新增", "927.5K", "-47.4%", delta_color="inverse")
c3.metric("平均 DAU", "4.11M", "-17.5%", delta_color="inverse")

# 5. 图表区（修正了图 27 的变量错误）
col_left, col_right = st.columns([4, 6])

with col_left:
    st.markdown("**Top 15 项目动态排名**")
    # 关键修正：确保变量名一致
    top_data = df.nlargest(15, "12月营收")
    fig_bar = px.bar(top_data, x="项目名称", y=["1月营收", "12月营收"], barmode="group",
                     template="plotly_dark", color_discrete_sequence=['#8b949e', '#1f6feb'])
    st.plotly_chart(fig_bar, use_container_width=True)

with col_right:
    st.markdown("**全量项目增长体量分布**")
    fig_scatter = px.scatter(df, x="12月DAU", y="12月营收", size="12月营收", color="项目名称",
                             template="plotly_dark", showlegend=False)
    st.plotly_chart(fig_scatter, use_container_width=True)

# 6. 编辑器与导出（单机工具的核心）
st.markdown("**📋 全项目明细对比 (可在下方直接改数)**")
edited_df = st.data_editor(df, use_container_width=True, hide_index=True)

# 侧边栏提供下载
with st.sidebar:
    st.download_button("📤 导出/保存当前数据", edited_df.to_csv(index=False), "game_data_save.csv")
