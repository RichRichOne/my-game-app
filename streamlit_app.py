import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# --- 页面配置 ---
st.set_page_config(
    page_title="游戏项目核心数据看板",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 自定义 CSS 样式 (复刻 Tailwind 风格) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background-color: #f8fafc;
    }

    /* 顶部导航栏模拟 */
    .header-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background-color: white;
        padding: 1rem 2rem;
        border-bottom: 1px solid #e2e8f0;
        margin-bottom: 2rem;
        border-radius: 0.5rem;
    }

    /* 指标卡片样式 */
    .stat-card {
        background-color: white;
        padding: 1.5rem;
        border-radius: 0.75rem;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    .stat-card:hover {
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        transform: translateY(-2px);
    }
    .stat-title {
        color: #64748b;
        font-size: 0.875rem;
        font-weight: 500;
        margin-bottom: 0.5rem;
    }
    .stat-value {
        color: #1e293b;
        font-size: 1.875rem;
        font-weight: 700;
        display: flex;
        align-items: baseline;
    }
    .stat-comparison {
        color: #94a3b8;
        font-size: 0.875rem;
        font-weight: 400;
        margin-left: 0.5rem;
    }
    .growth-tag {
        display: inline-flex;
        align-items: center;
        padding: 0.25rem 0.625rem;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-top: 0.5rem;
    }
    .growth-up { background-color: #ecfdf5; color: #10b981; }
    .growth-down { background-color: #fef2f2; color: #ef4444; }

    /* 进度条模拟 */
    .progress-bar-bg {
        background-color: #f1f5f9;
        height: 6px;
        border-radius: 3px;
        margin-top: 1rem;
        overflow: hidden;
    }
    .progress-bar-fill { height: 100%; border-radius: 3px; }

    /* 隐藏 Streamlit 默认页眉 */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- 初始数据加载 ---
def get_initial_data():
    data = [
        {"id": 1, "name": "项目 1", "jan_new": 27708, "jan_dau": 50493, "jan_rev": 1150700, "dec_new": 6148, "dec_dau": 172481, "dec_rev": 28798955},
        {"id": 2, "name": "项目 2", "jan_new": 72053, "jan_dau": 204897, "jan_rev": 13692150, "dec_new": 5739, "dec_dau": 110790, "dec_rev": 13340874},
        {"id": 3, "name": "项目 3",
