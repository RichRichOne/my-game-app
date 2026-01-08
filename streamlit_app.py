import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np  # 1. 导入指令必须在这里，文件最顶部

# 2. 页面配置
st.set_page_config(page_title="游戏项目数据看板", layout="wide")

# 3. 模拟数据（修正后的写法，确保不再报错）
data = {
    "项目名称": [f"项目 {i:02d}" for i in range(1, 36)],
    "1月收入(M)": [round(np.random.uniform(5, 50), 2) for _ in range(35)],
    "2月收入(M)": [round(np.random.uniform(5, 50), 2) for _ in range(35)],
    "活跃用户(K)": [round(np.random.uniform(10, 500), 2) for _ in range(35)],
    "类别": ["RPG", "SLG", "休闲", "卡牌", "射击"] * 7
}
df = pd.DataFrame(data)
df["增长率"] = ((df["2月收入(M)"] - df["1月收入(M)"]) / df["1月收入(M)"] * 100).round(2)

# 4. 界面标题
st.title("🎮 游戏项目月份数据对比看板")

# 5. 顶部核心指标卡
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("累计总收入 (2月)", f"${df['2月收入(M)'].sum():.2f}M", "12.5%")
with col2:
    st.metric("平均活跃用户", f"{df['活跃用户(K)'].mean():.1f}K", "-4.2%")
with col3:
    st.metric("最高收入项目", df.loc[df['2月收入(M)'].idxmax(), '项目名称'], "TOP 1")
with col4:
    st.write("数据操作")
    st.download_button("📥 导出报表(CSV)", data=df.to_csv(index=False), file_name="game_data.csv")

st.markdown("---")

# 6. 图表展示
left_col, right_col = st.columns(2)
with left_col:
    st.subheader("📊 项目收入Top 10")
    top_10 = df.nlargest(10, "2月收入(M)")
    fig_bar = px.bar(top_10, x="2月收入(M)", y="项目名称", orientation='h', color="2月收入(M)")
    st.plotly_chart(fig_bar, use_container_width=True)

with right_col:
    st.subheader("🎯 收入 vs 活跃分布")
    fig_scatter = px.scatter(df, x="活跃用户(K)", y="2月收入(M)", size="2月收入(M)", color="类别")
    st.plotly_chart(fig_scatter, use_container_width=True)

# 7. 数据明细
st.subheader("📋 项目明细数据 (支持在线编辑)")
st.data_editor(df, use_container_width=True)
