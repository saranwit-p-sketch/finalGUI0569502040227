import streamlit as st
import pandas as pd

# ==========================================
# ตั้งค่าหน้าเว็บไซต์
# ==========================================

st.set_page_config(
    page_title="แดชบอร์ดเปรียบเทียบสินเชื่อรถยนต์",
    page_icon="🚗",
    layout="wide"
)

# ==========================================
# อ่านข้อมูลจาก car_output.csv
# ==========================================

df = pd.read_csv("car_output.csv")

# ==========================================
# กำหนดราคารถยนต์
# ==========================================

car_price = 1000000

# ==========================================
# คำนวณยอดชำระรวม
# ==========================================

df["total_payment"] = car_price + df["total_rate"]

# ==========================================
# คำนวณค่างวดต่อเดือน
# ==========================================

df["monthly_payment"] = (
    df["total_payment"] / (df["year"] * 12)
)

# ==========================================
# หาข้อมูลสรุป
# ==========================================

lowest_interest = df["total_rate"].min()

lowest_monthly = df["monthly_payment"].min()

average_interest = df["total_rate"].mean()

lowest_interest_company = df.loc[
    df["total_rate"].idxmin(),
    "company_name"
]

lowest_monthly_company = df.loc[
    df["monthly_payment"].idxmin(),
    "company_name"
]

# ==========================================
# หัวข้อ Dashboard
# ==========================================

st.title("🚗 แดชบอร์ดเปรียบเทียบสินเชื่อรถยนต์")

st.write(
    "เปรียบเทียบอัตราดอกเบี้ย ยอดชำระรวม "
    "และค่างวดผ่อนต่อเดือนของแต่ละบริษัท"
)

st.divider()

# ==========================================
# แสดงข้อมูลสรุป 4 ช่อง
# ==========================================

col1, col2, col3, col4 = st.columns(4)

# ช่องที่ 1
with col1:
    st.metric(
        "ราคารถยนต์",
        f"฿{car_price:,.2f}"
    )

# ช่องที่ 2
with col2:
    st.metric(
        "ดอกเบี้ยต่ำสุด",
        f"฿{lowest_interest:,.2f}",
        f"↑ บริษัท {lowest_interest_company}"
    )

# ช่องที่ 3
with col3:
    st.metric(
        "ค่างวด/เดือนต่ำสุด",
        f"฿{lowest_monthly:,.2f}",
        f"↑ บริษัท {lowest_monthly_company}"
    )

# ช่องที่ 4
with col4:
    st.metric(
        "ดอกเบี้ยรวมเฉลี่ย",
        f"฿{average_interest:,.2f}"
    )

st.divider()

# ==========================================
# หัวข้อกราฟ
# ==========================================

st.subheader(
    "📊 เปรียบเทียบดอกเบี้ยรวม ยอดชำระรวม "
    "และค่างวดผ่อนต่อเดือน"
)

# ==========================================
# แบ่งพื้นที่กราฟเป็น 2 ช่อง
# ==========================================

col1, col2 = st.columns(2)

# ==========================================
# กราฟที่ 1 : ดอกเบี้ยรวม
# ==========================================

with col1:

    st.write("**เปรียบเทียบดอกเบี้ยรวมของแต่ละบริษัท (บาท)**")

    interest_chart = df.set_index(
        "company_name"
    )[["total_rate"]]

    st.bar_chart(
        interest_chart,
        use_container_width=True
    )

# ==========================================
# กราฟที่ 2 : ค่างวดต่อเดือน
# ==========================================

with col2:

    st.write("**เปรียบเทียบค่างวดผ่อนต่อเดือน (บาท/เดือน)**")

    monthly_chart = df.set_index(
        "company_name"
    )[["monthly_payment"]]

    st.bar_chart(
        monthly_chart,
        use_container_width=True
    )

st.divider()

# ==========================================
# ตารางเปรียบเทียบ
# ==========================================

st.subheader(
    "📋 ตารางเปรียบเทียบเงื่อนไขสินเชื่อรถยนต์"
)

# คัดลอกข้อมูลเพื่อใช้แสดงผล
display_df = df.copy()

# จัดรูปแบบอัตราดอกเบี้ย
display_df["rate"] = display_df["rate"].map(
    lambda x: f"{x:.2f}%"
)

# จัดรูปแบบดอกเบี้ยรวม
display_df["total_rate"] = display_df["total_rate"].map(
    lambda x: f"{x:,.2f}"
)

# จัดรูปแบบยอดชำระรวม
display_df["total_payment"] = display_df["total_payment"].map(
    lambda x: f"{x:,.2f}"
)

# จัดรูปแบบค่างวดต่อเดือน
display_df["monthly_payment"] = display_df["monthly_payment"].map(
    lambda x: f"{x:,.2f}"
)

# เปลี่ยนชื่อคอลัมน์เป็นภาษาไทย
display_df.columns = [
    "บริษัท",
    "ดอกเบี้ย/ปี",
    "ระยะเวลา (ปี)",
    "ดอกเบี้ยรวม (บาท)",
    "ยอดชำระรวม (บาท)",
    "ค่างวด/เดือน (บาท)"
]

# แสดงตาราง
st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True
)

# ==========================================
# สรุป
# ==========================================

st.divider()

st.subheader("📝 สรุปข้อมูล")

st.write(
    f"ราคารถยนต์ที่ใช้ในการคำนวณ : "
    f"**฿{car_price:,.2f}**"
)

st.write(
    f"บริษัทที่มีดอกเบี้ยรวมต่ำสุด : "
    f"**บริษัท {lowest_interest_company}** "
    f"จำนวน **฿{lowest_interest:,.2f}**"
)

st.write(
    f"บริษัทที่มีค่างวดต่อเดือนต่ำสุด : "
    f"**บริษัท {lowest_monthly_company}** "
    f"จำนวน **฿{lowest_monthly:,.2f} ต่อเดือน**"
)

st.write(
    f"ดอกเบี้ยรวมเฉลี่ยของทุกบริษัท : "
    f"**฿{average_interest:,.2f}**"
)
