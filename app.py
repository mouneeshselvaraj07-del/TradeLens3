import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeClassifier

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(page_title="TradeLens - AI Seller Assistant", layout="wide")

# -----------------------------
# Session State
# -----------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.mobile = ""
    st.session_state.gender = ""

# -----------------------------
# Sample Amazon-like Product Data
# -----------------------------
products_data = [
    # Mobiles
    {"category":"iPhone 14","type":"Mobile","brand":"Apple","cost_price":70000,"rating":4.8,"location":"Delhi"},
    {"category":"Galaxy S23","type":"Mobile","brand":"Samsung","cost_price":60000,"rating":4.5,"location":"Mumbai"},
    {"category":"Pixel 7","type":"Mobile","brand":"Google","cost_price":50000,"rating":4.6,"location":"Bangalore"},
    {"category":"OnePlus 11","type":"Mobile","brand":"OnePlus","cost_price":45000,"rating":4.4,"location":"Chennai"},
    # Laptops
    {"category":"XPS 13","type":"Laptop","brand":"Dell","cost_price":75000,"rating":4.7,"location":"Delhi"},
    {"category":"MacBook Air M2","type":"Laptop","brand":"Apple","cost_price":120000,"rating":4.9,"location":"Mumbai"},
    {"category":"ThinkPad X1","type":"Laptop","brand":"Lenovo","cost_price":85000,"rating":4.6,"location":"Bangalore"},
    {"category":"ROG Zephyrus","type":"Laptop","brand":"Asus","cost_price":95000,"rating":4.5,"location":"Chennai"},
    # Shoes
    {"category":"Air Max 270","type":"Shoes","brand":"Nike","cost_price":12000,"rating":4.7,"location":"Kolkata"},
    {"category":"UltraBoost","type":"Shoes","brand":"Adidas","cost_price":11000,"rating":4.6,"location":"Mumbai"},
    {"category":"Classic Leather","type":"Shoes","brand":"Reebok","cost_price":8000,"rating":4.5,"location":"Delhi"},
    {"category":"Suede Platform","type":"Shoes","brand":"Puma","cost_price":9000,"rating":4.4,"location":"Bangalore"},
    # Headphones
    {"category":"WH-1000XM5","type":"Headphones","brand":"Sony","cost_price":25000,"rating":4.8,"location":"Chennai"},
    {"category":"AirPods Pro","type":"Headphones","brand":"Apple","cost_price":25000,"rating":4.7,"location":"Delhi"},
    {"category":"Galaxy Buds 2","type":"Headphones","brand":"Samsung","cost_price":15000,"rating":4.5,"location":"Mumbai"},
    {"category":"Bose QC45","type":"Headphones","brand":"Bose","cost_price":30000,"rating":4.9,"location":"Bangalore"},
]

# Duplicate for more products
data = pd.DataFrame(products_data*5)
np.random.seed(42)
data["demand_score"] = np.random.randint(1,4,size=len(data))
data["returns"] = np.random.randint(0,2,size=len(data))
data["selling_price"] = data["cost_price"]*1.2
data["month"] = np.random.choice(["Jan","Feb","Mar","Apr","May"], size=len(data))

# ML Models
price_model = LinearRegression().fit(data[["cost_price"]], data["selling_price"])
risk_model = DecisionTreeClassifier().fit(data[["cost_price"]], data["returns"])

# -----------------------------
# Custom CSS
# -----------------------------
st.markdown("""
<style>
body {background-color: #F9F9F9; font-family: 'Inter', sans-serif;}
div.stButton>button:first-child {background-color:#4A90E2; color:white; border-radius:8px; height:40px; width:180px; border:none; font-weight:500; font-size:14px;}
div.stButton>button:hover {background-color:#3B78C2; cursor:pointer;}
.card {background-color:#FFFFFF; border-radius:12px; padding:16px; margin:12px; box-shadow:0 4px 12px rgba(0,0,0,0.1); transition: transform 0.2s;}
.card:hover {transform: scale(1.02);}
.top-right {position: fixed; top: 10px; right: 20px; background-color:#FFFFFF; padding:8px 12px; border-radius:8px; box-shadow:0 2px 6px rgba(0,0,0,0.1);}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# PAGE 1 - LOGIN
# -----------------------------
if not st.session_state.logged_in:
    st.title("🚀 TradeLens - AI Seller Login")
    users = {"admin":"1234","seller":"abcd"}
    username = st.text_input("Username", placeholder="Enter username")
    password = st.text_input("Password", type="password", placeholder="Enter password")
    mobile = st.text_input("Mobile Number", placeholder="Enter mobile number")
    gender = st.selectbox("Gender", ["Male","Female"])
    
    login_clicked = st.button("Login")
    if login_clicked:
        if username in users and users[username]==password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.mobile = mobile
            st.session_state.gender = gender
            st.success(f"Welcome {username}!")
            st.experimental_rerun = False  # placeholder, no call
        else:
            st.error("❌ Invalid username or password")

# -----------------------------
# PAGE 2 - DASHBOARD
# -----------------------------
if st.session_state.logged_in:
    # Top-right logged-in info
    st.markdown(f"<div class='top-right'>Logged in: {st.session_state.username} | {st.session_state.mobile} | {st.session_state.gender}</div>", unsafe_allow_html=True)

    tabs = st.tabs(["Home", "Dashboard"])

    # -----------------------------
    # Tab 1 - Home / Products
    # -----------------------------
    with tabs[0]:
        st.header("🌟 TradeLens - Products & AI Suggestions")

        search_text = st.text_input("Search Products (e.g., mobile, laptop, shoes, headphones)")

        # Filter by search
        if search_text:
            filtered_data = data[data["type"].str.lower().str.contains(search_text.lower())]
        else:
            filtered_data = data

        st.subheader(f"Showing {len(filtered_data)} products")
        cols = st.columns(3)
        for i, row in filtered_data.iterrows():
            col = cols[i%3]
            with col:
                st.markdown("<div class='card'>", unsafe_allow_html=True)
                st.markdown(f"**{row['category']}** ({row['type']})")
                st.markdown(f"Brand: {row['brand']}")
                st.markdown(f"Rating: {row['rating']} ⭐")
                st.markdown(f"Location: {row['location']}")
                st.markdown(f"Cost Price: ₹{row['cost_price']}")

                # AI Predictions
                predicted_price = price_model.predict([[row["cost_price"]]])[0]
                profit = predicted_price - row["cost_price"]
                risk = risk_model.predict([[row["cost_price"]]])[0]
                risk_text = "High Risk ⚠" if risk==1 else "Low Risk ✅"
                sell_suggestion = "✅ Sell" if profit>0 and risk==0 else "❌ Don't Sell"

                st.markdown(f"Predicted Price: ₹{round(predicted_price,2)}")
                st.markdown(f"Expected Profit: ₹{round(profit,2)}")
                st.markdown(f"Return Risk: {risk_text}")
                st.markdown(f"Suggestion: {sell_suggestion}")
                st.markdown("</div>", unsafe_allow_html=True)

    # -----------------------------
    # Tab 2 - Dashboard
    # -----------------------------
    with tabs[1]:
        st.header("📊 Dashboard Insights")
        col1, col2 = st.columns(2)

        if len(filtered_data) > 0:
            predicted_prices = price_model.predict(filtered_data[["cost_price"]])
            profits = predicted_prices - filtered_data["cost_price"]
            risks = risk_model.predict(filtered_data[["cost_price"]])

            demo_values = [
                filtered_data["cost_price"].iloc[0],
                predicted_prices[0],
                profits[0]
            ]
            trend_data = filtered_data.groupby("month")["demand_score"].mean().reset_index()
            risk_map = pd.DataFrame({
                "Category": filtered_data["category"],
                "Cost Price": filtered_data["cost_price"],
                "Return Risk": np.where(filtered_data["returns"]==1,1,0)
            })
        else:
            predicted_prices = np.array([0])
            profits = np.array([0])
            risks = np.array([0])
            demo_values = [0,0,0]
            trend_data = pd.DataFrame({"month":["Jan"],"demand_score":[0]})
            risk_map = pd.DataFrame({
                "Category": ["None"],
                "Cost Price": [0],
                "Return Risk": [0]
            })

        with col1:
            st.bar_chart(pd.DataFrame({"Values": demo_values}, index=["Cost","Selling Price","Profit"]))
            st.line_chart(trend_data.set_index("month"))

        with col2:
            st.dataframe(risk_map.style.background_gradient(cmap="Reds"))