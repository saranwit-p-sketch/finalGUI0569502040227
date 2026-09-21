import streamlit as st
import pandas as pd
import plotly.express as px

# ตั้งค่าหน้าเว็บให้เป็นแบบกว้าง (Wide Mode)
st.set_page_config(
    page_title="Car Loan Comparison",
    layout="wide"
)

# --- ส่วนหัวข้อหลัก ---
st.title("🏎️ แดชบอร์ดเปรียบเทียบสินเชื่อรถยนต์ (Car Loan Comparison)")
st.caption("อ่านข้อมูลจาก `car.csv` คำนวณดอกเบี้ยรวม ยอดชำระรวม และค่างวดผ่อนต่อเดือน พร้อมบันทึกลง `car_output.csv`[cite: 1]")

# กำหนดราคารถยนต์พื้นฐาน
CAR_PRICE = 1000000.00

# --- การอ่านข้อมูลและการคำนวณ ---
try:
    df = pd.read_csv('car.csv')
    
    # ทำความสะอาดข้อมูลดอกเบี้ย (แปลงจาก '2.50%' เป็น float 0.025)
    df['ดอกเบี้ย_num'] = df['ดอกเบี้ย/ปี'].str.rstrip('%').astype('float') / 100
    
    # คำนวณตามหลักดอกเบี้ยคงที่ (Flat Rate):
    # ดอกเบี้ยรวม = ราคารถ * อัตราดอกเบี้ย * ระยะเวลา (ปี)
    df['ดอกเบี้ยรวม (บาท)'] = CAR_PRICE * df['ดอกเบี้ย_num'] * df['ระยะเวลา (ปี)']
    
    # ยอดชำระรวม = ราคารถ + ดอกเบี้ยรวม
    df['ยอดชำระรวม (บาท)'] = CAR_PRICE + df['ดอกเบี้ยรวม (บาท)']
    
    # ผ่อน/เดือน = ยอดชำระรวม / (ระยะเวลาปี * 12)
    df['ผ่อน/เดือน (บาท)'] = df['ยอดชำระรวม (บาท)'] / (df['ระยะเวลา (ปี)'] * 12)
    
    # บันทึกผลลัพธ์ลงไฟล์ car_output.csv
    output_df = df[['บริษัท', 'ดอกเบี้ย/ปี', 'ระยะเวลา (ปี)', 'ดอกเบี้ยรวม (บาท)', 'ยอดชำระรวม (บาท)', 'ผ่อน/เดือน (บาท)']]
    output_df.to_csv('car_output.csv', index=False, encoding='utf-8-sig')

    # หาค่าสถิติสำหรับสร้าง Metric Cards
    min_interest_row = df.loc[df['ดอกเบี้ยรวม (บาท)'].idxmin()]
    min_monthly_row = df.loc[df['ผ่อน/เดือน (บาท)'].idxmin()]
    avg_interest = df['ดอกเบี้ยรวม (บาท)'].mean()

    # --- 1. Metric Cards แสดงข้อมูลสรุปด้านบน ---
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("ราคารถยนต์", f"฿{CAR_PRICE:,.2f}")
        
    with col2:
        st.metric(
            "ดอกเบี้ยรวมต่ำสุด", 
            f"฿{min_interest_row['ดอกเบี้ยรวม (บาท)']:,.2f}", 
            delta=f"↑ บริษัท {min_interest_row['บริษัท']}",
            delta_color="normal"
        )
        
    with col3:
        st.metric(
            "ผ่อน/เดือน ต่ำสุด", 
            f"฿{min_monthly_row['ผ่อน/เดือน (บาท)']:,.2f}", 
            delta=f"↑ บริษัท {min_monthly_row['บริษัท']} ({min_monthly_row['ระยะเวลา (ปี)']} ปี)",
            delta_color="normal"
        )
        
    with col4:
        st.metric("ดอกเบี้ยรวมเฉลี่ย", f"฿{avg_interest:,.2f}")

    st.markdown("---")

    # --- 2. ส่วนแสดงกราฟเปรียบเทียบ ---
    st.subheader("📊 เปรียบเทียบดอกเบี้ยรวม ยอดชำระรวม และค่างวดผ่อนต่อเดือน")
    
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        # กราฟแท่งเปรียบเทียบดอกเบี้ยรวม
        fig_interest = px.bar(
            df, 
            x='บริษัท', 
            y='ดอกเบี้ยรวม (บาท)',
            color='ระยะเวลา (ปี)',
            title="เปรียบเทียบดอกเบี้ยรวมตลอดสัญญา (บาท)",
            text_auto=',.2f',
            color_continuous_scale='Reds'
        )
        fig_interest.update_layout(yaxis_title="ดอกเบี้ยรวม (บาท)", xaxis_title="บริษัทข้อเสนอ")
        st.plotly_chart(fig_interest, use_container_width=True)

    with chart_col2:
        # กราฟแท่งเปรียบเทียบค่างวดผ่อนต่อเดือน
        fig_monthly = px.bar(
            df, 
            x='บริษัท', 
            y='ผ่อน/เดือน (บาท)',
            color='บริษัท',
            title="เปรียบเทียบค่างวดผ่อนชำระต่อเดือน (บาท/เดือน)",
            text_auto=',.2f'
        )
        fig_monthly.update_layout(yaxis_title="ผ่อน/เดือน (บาท)", xaxis_title="บริษัทข้อเสนอ")
        st.plotly_chart(fig_monthly, use_container_width=True)

    st.markdown("---")

    # --- 3. ส่วนแสดงตารางข้อมูล ---
    st.subheader("📋 ตารางเปรียบเทียบเงื่อนไขสินเชื่อรถยนต์")
    
    # แสดงตารางพร้อมเน้นสีช่องข้อมูล
    st.dataframe(
        output_df.style.format({
            'ดอกเบี้ยรวม (บาท)': '฿{:,.2f}',
            'ยอดชำระรวม (บาท)': '฿{:,.2f}',
            'ผ่อน/เดือน (บาท)': '฿{:,.2f}'
        }),
        use_container_width=True
    )

except FileNotFoundError:
    st.error("ไม่พบไฟล์ `car.csv` กรุณาตรวจสอบว่ามีไฟล์นี้อยู่ใน Directory เดียวกับโปรแกรมหรือไม่")
