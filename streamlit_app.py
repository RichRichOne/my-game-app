import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# --- 1. 页面配置 ---
st.set_page_config(
    page_title="游戏项目核心数据看板",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. 自定义 CSS 样式 (复刻 AI Studio 的精致感) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; background-color: #f8fafc; }
    .stat-card {
        background-color: white; padding: 1.5rem; border-radius: 0.75rem;
        border: 1px solid #e2e8f0; box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    .stat-title { color: #64748b; font-size: 0.875rem; font-weight: 500; margin-bottom: 0.5rem; }
    .stat-value { color: #1e293b; font-size: 1.875rem; font-weight: 700; }
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- 3. 数据生成 (补全你刚才断掉的部分) ---
def get_data():
    # 这里模拟 35 个项目的数据，对应你图 22 的逻辑
    np.random.seed(42)
    rows = []
    for i in range(1, 36):
        jan_rev = np.random.randint(100, 2000) * 1000
        dec_rev = np.random.randint(500, 5000) * 10000
        rows.append({
            "id": i, "项目名称": f"项目 {i:02d}",
            "1月营收": jan_rev, "12月营收": dec_rev,
            "12月DAU": np.random.randint(100, 1000) * 1000,
            "增长率": round((dec_rev - jan_rev) / jan_rev * 100, 2)
        })
    return pd.DataFrame(rows)

df = get_data()

# --- 4. 顶部标题与导出 ---
col_t1, col_t2 = st.columns([8, 2])
with col_t1:
    st.markdown("# 🎮 游戏项目核心数据看板")
    st.markdown("数据范围：2025年1月 vs 2025年12月")
with col_t2:
    st.download_button("📥 导出全量报表", df.to_csv(index=False), "report.csv", use_container_width=True)

# --- 5. 顶部指标卡 (KPI) ---
kpi1, kpi2, kpi3 = st.columns(3)
with kpi1:
    st.markdown(f'<div class="stat-card"><div class="stat-title">累计充值 (12月)</div><div class="stat-value">¥{df["12月营收"].sum()/1e6:.2f}M</div><div style="color:#ef4444">↓ 8.8% vs 上月</div></div>', unsafe_allow_html=True)
with kpi2:
    st.markdown(f'<div class="stat-card"><div class="stat-title">活跃总 DAU</div><div class="stat-value">{df["12月DAU"].sum()/1e6:.2f}M</div><div style="color:#ef4444">↓ 17.5% vs 上月</div></div>', unsafe_allow_html=True)
with kpi3:
    st.markdown(f'<div class="stat-card"><div class="stat-title">平均增长率</div><div class="stat-value">{df["增长率"].mean():.1f}%</div><div style="color:#10b981">↑ 稳步回升</div></div>', unsafe_allow_html=True)

st.write("") # 间距

# --- 6. 图表区 ---
c1, c2 = st.columns([1, 1])
with c1:
    st.subheader("📊 Top 10 营收对比")
    top_10 = df.nlargest(10, "12月营收")
    fig1 = px.bar(top_10, x="项目名称", y=["1月营收", "12月营收"], barmode="group",
                 color_discrete_sequence=['#cbd5e1', '#3b82f6'])
    fig1.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig1, use_container_width=True)

with c2:
    st.subheader("🎯 DAU 与 营收 分布")
    fig2 = px.scatter(df, x="12月DAU", y="12月营收", size="12月营收", color="增长率",
                     hover_name="项目名称", color_continuous_scale="RdBu_r")
    st.plotly_chart(fig2, use_container_width=True)

# --- 7. 数据明细表格 ---
st.subheader("📋 项目明细数据对照表")
# 使用 data_editor 让它像 Excel 一样可以编辑
edited_df = st.data_editor(df, use_container_width=True, hide_index=True)

st.success("✅ 看板已就绪。您可以直接在网页上修改明细表，或者点击右上角按钮导出结果。")
