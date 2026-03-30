import streamlit as st
import requests
import pandas as pd
import os
from datetime import date

BACKEND_URL = os.getenv("BACKEND_URL", "http://backend-service:8000")

st.set_page_config(page_title="Membership Manager", layout="wide")

st.title("🏆 Membership Management System")
st.markdown("---")

# Sidebar for adding new members
st.sidebar.header("➕ Add New Member")
with st.sidebar.form("add_member_form"):
    full_name = st.text_input("Full Name")
    sub_level = st.selectbox("Subscription Level", ["Basic", "Silver", "Gold", "Platinum"])
    expiry = st.date_input("Expiry Date", min_value=date.today())
    submit = st.form_submit_button("Create Member")

    if submit:
        if full_name:
            member_data = {
                "full_name": full_name,
                "subscription_level": sub_level,
                "expiry_date": expiry.isoformat()
            }
            try:
                response = requests.post(f"{BACKEND_URL}/members", json=member_data)
                if response.status_code == 200:
                    st.sidebar.success(f"Added {full_name}!")
                else:
                    st.sidebar.error(f"Failed to add member: {response.text}")
            except Exception as e:
                st.sidebar.error(f"Connection error: {e}")
        else:
            st.sidebar.warning("Please enter a name.")

# Main area for viewing members
st.header("📋 Registered Members")
if st.button("🔄 Refresh Data"):
    try:
        response = requests.get(f"{BACKEND_URL}/members")
        if response.status_code == 200:
            data = response.json()
            if data:
                df = pd.DataFrame(data)
                # Cleanup display
                df = df.rename(columns={
                    "id": "ID",
                    "full_name": "Full Name",
                    "subscription_level": "Level",
                    "expiry_date": "Expiration"
                })
                st.dataframe(df, use_container_width=True)
            else:
                st.info("No members found in the database.")
        else:
            st.error(f"Error fetching data: {response.status_code}")
    except Exception as e:
        st.error(f"Cannot connect to Backend at {BACKEND_URL}: {e}")
else:
    st.info("Click 'Refresh Data' to load the member list.")

st.markdown("---")
st.caption(f"Connected to backend: {BACKEND_URL}")
