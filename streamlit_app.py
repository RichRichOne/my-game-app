import streamlit as st
import pandas as pd
import plotly.express as px

# 1. 页面配置：设置标题和宽屏布局
st.set_page_config(page_title="游戏项目数据看板", layout="wide")

# 2. 自定义 CSS 样式（让界面更像图22的高级感）
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 20px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

st.title("🎮 游戏项目月份数据对比看板")

# 3. 模拟数据（基于你之前的35个项目）
data = {
    "项目名称": [f"项目 {i:02d}" for i in range(1, 36)],
   import numpy as np  # 先在文件最顶部 import 下面加这一行

# ... 之前的代码保持不变 ...

# 3. 模拟数据（修正后的写法）
data = {
    "项目名称": [f"项目 {i:02d}" for i in range(1, 36)],
    "1月收入(M)": [round(np.random.uniform(5, 50), 2) for _ in range(35)],
    "2月收入(M)": [round(np.random.uniform(5, 50), 2) for _ in range(35)],
    "活跃用户(K)": [round(np.random.uniform(10, 500), 2) for _ in range(35)],
    "类别": ["RPG", "SLG", "休闲", "卡牌", "射击"] * 7
}
    "类别": ["RPG", "SLG", "休闲", "卡牌", "射击"] * 7
}
df = pd.DataFrame(data)
df["增长率"] = ((df["2月收入(M)"] - df["1月收入(M)"]) / df["1月收入(M)"] * 100).round(2)

# 4. 顶部核心指标卡（KPI Metrics）
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("累计总收入 (2月)", f"${df['2月收入(M)'].sum():.2f}M", "12.5%")
with col2:
    st.metric("平均活跃用户", f"{df['活跃用户(K)'].mean():.1f}K", "-4.2%")
with col3:
    st.metric("最高收入项目", df.loc[df['2月收入(M)'].idxmax(), '项目名称'], "TOP 1")
with col4:
    # 导出按钮放这里
    st.write("数据操作")
    st.download_button("📥 导出报表(CSV)", data=df.to_csv(index=False), file_name="game_data.csv")

st.markdown("---")

# 5. 中间部分：左右分栏图表
left_col, right_col = st.columns([1, 1])

with left_col:
    st.subheader("📊 项目收入Top 10 (2月)")
    top_10 = df.nlargest(10, "2月收入(M)")
    fig_bar = px.bar(top_10, x="2月收入(M)", y="项目名称", orientation='h', 
                     color="2月收入(M)", color_continuous_scale="Blues")
    st.plotly_chart(fig_bar, use_container_width=True)

with right_col:
    st.subheader("🎯 收入 vs 活跃用户分布")
    fig_scatter = px.scatter(df, x="活跃用户(K)", y="2月收入(M)", size="2月收入(M)", 
                             color="类别", hover_name="项目名称", text="项目名称")
    st.plotly_chart(fig_scatter, use_container_width=True)

# 6. 底部：详细数据编辑器
st.subheader("📋 项目明细数据 (支持在线编辑)")
edited_df = st.data_editor(df, use_container_width=True, num_rows="dynamic")

st.info("💡 提示：你可以直接点击上方表格修改数据，图表会实时尝试重绘（注：此模拟版仅演示界面升级）。")
