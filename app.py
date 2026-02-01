import streamlit as st
import requests
import pandas as pd

# 页面配置（适配手机）
st.set_page_config(
    page_title="我的基金持仓工具",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 你的持仓数据（已根据截图填充）
holdings = [
    {
        "code": "000971",
        "name": "中欧新蓝筹灵活配置混合A",
        "current_value": 23.31,
        "profit": 15.34,
        "profit_rate": 153.36
    },
    {
        "code": "012164",
        "name": "中欧红利优享灵活配置混合C",
        "current_value": 10711.07,
        "profit": 906.51,
        "profit_rate": 9.85
    },
    {
        "code": "004394",
        "name": "中欧资源精选混合C",
        "current_value": 489.12,
        "profit": 28.81,
        "profit_rate": 6.26
    },
    {
        "code": "003096",
        "name": "中欧医疗健康混合C",
        "current_value": 2438.70,
        "profit": -454.54,
        "profit_rate": -15.73
    },
    {
        "code": "011593",
        "name": "易方达国防军工混合C",
        "current_value": 9590.36,
        "profit": 1645.15,
        "profit_rate": 20.71
    }
]

# 实时估值接口
def get_fund_valuation(fund_code):
    url = f"https://fundmobapi.eastmoney.com/FundMobiApi/JS/FundEstimateApi.ashx?fundcode={fund_code}"
    try:
        response = requests.get(url, timeout=5)
        data = response.text.replace("jsonp(", "").replace(")", "").split(",")
        if len(data) >= 3:
            return {
                "estimate_value": float(data[1]),
                "estimate_change": float(data[2].replace("%", ""))
            }
        return None
    except:
        return None

# 页面标题
st.title("📊 我的基金持仓工具")
st.divider()

# 持仓总览
total_value = sum(f["current_value"] for f in holdings)
total_profit = sum(f["profit"] for f in holdings)

col1, col2 = st.columns(2)
with col1:
    st.metric("总持有金额（元）", f"{total_value:.2f}")
with col2:
    st.metric(
        "总持有收益（元）",
        f"{total_profit:.2f}",
        delta=f"{total_profit/total_value*100:.2f}%" if total_value > 0 else "0%",
        delta_color="normal"
    )

st.divider()

# 刷新按钮
if st.button("🔄 刷新实时估值"):
    st.rerun()

# 基金列表展示
fund_data = []
for fund in holdings:
    val = get_fund_valuation(fund["code"])
    fund_data.append({
        "基金名称": fund["name"],
        "持有金额（元）": f"{fund['current_value']:.2f}",
        "持有收益（元）": f"{fund['profit']:.2f}" if fund['profit'] < 0 else f"+{fund['profit']:.2f}",
        "收益率（%）": f"{fund['profit_rate']:.2f}" if fund['profit_rate'] < 0 else f"+{fund['profit_rate']:.2f}",
        "实时估值": f"{val['estimate_value']:.4f}" if val else "加载失败",
        "估值涨跌幅（%）": f"{val['estimate_change']:.2f}" if val and val['estimate_change'] < 0 else f"+{val['estimate_change']:.2f}" if val else "加载失败"
    })

# 生成表格
df = pd.DataFrame(fund_data)
st.dataframe(
    df,
    column_config={
        "持有收益（元）": st.column_config.TextColumn(
            "持有收益（元）",
            width="medium"
        ),
        "估值涨跌幅（%）": st.column_config.TextColumn(
            "估值涨跌幅（%）",
            width="medium"
        )
    },
    hide_index=True,
    use_container_width=True
)

# 底部提示
st.caption("💡 实时估值来自第三方接口，非官方最终净值，仅供参考")
