import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# 1. 强制设定深色主题和高保真 CSS 样式
st.set_page_config(page_title="游戏项目核心数据看板", layout="wide")

st.markdown("""
    <style>
    /* 全局深蓝色背景 */
    .stApp { background: #0e1117; color: #ffffff; }
    /* 顶部导航模拟 */
    .nav-bar { background: #161b22; padding: 10px; border-radius: 5px; margin-bottom: 20px; }
    /* KPI 卡片美化：增加发光边框 */
    div[data-metric-container] {
        background: #1c2128;
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.5);
    }
    label[data-testid="stMetricLabel"] { color: #8b949e !important; font-size: 1rem !important; }
    div[data-testid="stMetricValue"] { color: #58a6ff !important; font-weight: bold !important; }
    /* 隐藏所有多余组件 */
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# 2. 模拟图 22 中的 35 个项目数据
np.random.seed(42)
projects = [f"项目 {i}" for i in range(1, 36)]
data = {
    "项目名称": projects,
    "1月营收": np.random.randint(5000000, 100000000, 35),
    "12月营收": np.random.randint(5000000, 100000000, 35),
    "1月DAU": np.random.randint(100000, 2000000, 35),
    "12月DAU": np.random.randint(100000, 2000000, 35),
}
df = pd.DataFrame(data)

# 3. 页面标题
st.markdown("### 📊 游戏项目核心数据看板 <span style='font-size:0.8rem; color:#8b949e'>1月 vs 12月 核心数据追踪</span>", unsafe_allow_html=True)

# 4. 顶部 KPI 指标卡（复刻图 22 第一行）
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("累计充值", "454.14M ₹", "-8.8%", delta_color="inverse")
with col2:
    st.metric("累计新增", "927.5K", "-47.4%", delta_color="inverse")
with col3:
    st.metric("平均 DAU", "4.11M", "-17.5%", delta_color="inverse")

st.markdown("<br>", unsafe_allow_html=True)

# 5. 中间图表区（分左右两栏）
c1, c2 = st.columns([4, 6])

with c1:
    st.markdown("**Top 15 项目动态排名 - 充值金额 (₹)**")
    top_15 = df.nlargest(15, "12月营收")
    fig_bar = px.bar(top_10, x="项目名称", y=["1月营收", "12月营收"], barmode="group",
                     template="plotly_dark", color_discrete_sequence=['#8b949e', '#1f6feb'])
    fig_bar.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(t=20, b=20, l=0, r=0))
    st.plotly_chart(fig_bar, use_container_width=True)

with c2:
    st.markdown("**全量项目增长与体量分布**")
    fig_scatter = px.scatter(df, x="12月DAU", y="12月营收", size="12月营收", color="项目名称",
                             template="plotly_dark", showlegend=False)
    fig_scatter.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_scatter, use_container_width=True)

# 6. 底部明细（复刻图 22 底部表格）
st.markdown("**全项目明细对比 (1月 vs 12月)**")
st.data_editor(df, use_container_width=True, hide_index=True)

# 7. 侧边栏功能（导出与设置）
with st.sidebar:
    st.title("控制中心")
    st.download_button("📥 导出分析报告 (CSV)", df.to_csv(index=False), "game_report.csv")
    st.info("💡 提示：此看板已根据 AI Studio UI 深度定制。直接修改上方表格数据，图表将实时更新。")
