import streamlit as st
import pandas as pd
import plotly.express as px


# ==========================================
# ตั้งค่าหน้าเว็บไซต์
# ==========================================

st.set_page_config(
    page_title="แดชบอร์ดเปรียบเทียบสินเชื่อรถยนต์",
    page_icon="🚗",
    layout="wide"
)


# ==========================================
# ปรับแต่งหน้าเว็บไซต์
# ==========================================

st.markdown("""
<style>

.stApp {
    background-color: #FFFFFF;
}

/* หัวข้อทั้งหมด */
h1, h2, h3, h4, h5, h6 {
    color: #000000 !important;
}

/* ข้อความทั่วไป */
p {
    color: #000000 !important;
}

/* Caption */
[data-testid="stCaptionContainer"] {
    color: #000000 !important;
}

/* Metric */
[data-testid="stMetric"] {
    background-color: #FFFFFF;
    padding: 10px;
}

[data-testid="stMetricLabel"] {
    color: #000000 !important;
}

[data-testid="stMetricValue"] {
    color: #000000 !important;
}

[data-testid="stMetricDelta"] {
    color: #000000 !important;
}

/* ตาราง */
[data-testid="stDataFrame"] {
    color: #000000 !important;
}

</style>
""", unsafe_allow_html=True)


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
# หาค่าที่ต้องใช้ใน Dashboard
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

st.title(
    "🚗 แดชบอร์ดเปรียบเทียบสินเชื่อรถยนต์ "
    "(Car Loan Comparison)"
)

st.caption(
    "อ่านข้อมูลจาก car.csv คำนวณดอกเบี้ยรวม "
    "ยอดชำระรวม และค่างวดผ่อนต่อเดือน "
    "พร้อมบันทึกข้อมูลลง car_output.csv"
)


st.divider()


# ==========================================
# แสดงข้อมูลสำคัญ
# ==========================================

col1, col2, col3, col4 = st.columns(4)


# ------------------------------------------
# ราคารถยนต์
# ------------------------------------------

with col1:

    st.metric(
        "ราคารถยนต์",
        f"฿{car_price:,.2f}"
    )


# ------------------------------------------
# ดอกเบี้ยรวมต่ำสุด
# ------------------------------------------

with col2:

    st.metric(
        "ดอกเบี้ยรวมต่ำสุด",
        f"฿{lowest_interest:,.2f}",
        f"↑ บริษัท {lowest_interest_company}"
    )


# ------------------------------------------
# ค่างวดต่อเดือนต่ำสุด
# ------------------------------------------

with col3:

    st.metric(
        "ค่างวด/เดือนต่ำสุด",
        f"฿{lowest_monthly:,.2f}",
        f"↑ บริษัท {lowest_monthly_company}"
    )


# ------------------------------------------
# ดอกเบี้ยรวมเฉลี่ย
# ------------------------------------------

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

chart_col1, chart_col2 = st.columns(2)


# ==========================================
# กราฟที่ 1 ดอกเบี้ยรวม
# ==========================================

with chart_col1:

    st.write(
        "**เปรียบเทียบดอกเบี้ยรวมของแต่ละบริษัท (บาท)**"
    )

    interest_chart = px.bar(
        df,
        x="company_name",
        y="total_rate",
        text="total_rate",
        color="total_rate",
        color_continuous_scale=[
            "#F8E9E5",
            "#E8B8B2",
            "#7A0019"
        ]
    )

    # ตัวเลขบนแท่งกราฟ
    interest_chart.update_traces(
        texttemplate="%{text:,.2f}",
        textposition="outside",
        textfont=dict(
            color="black"
        )
    )

    # ตั้งค่าสีตัวอักษรทั้งหมดในกราฟ
    interest_chart.update_layout(
        xaxis_title="บริษัทสินเชื่อ",
        yaxis_title="ดอกเบี้ยรวม (บาท)",

        coloraxis_colorbar_title="ดอกเบี้ย",

        plot_bgcolor="white",
        paper_bgcolor="white",

        font=dict(
            color="black"
        ),

        xaxis=dict(
            tickfont=dict(
                color="black"
            ),
            title_font=dict(
                color="black"
            )
        ),

        yaxis=dict(
            tickfont=dict(
                color="black"
            ),
            title_font=dict(
                color="black"
            )
        ),

        coloraxis_colorbar=dict(
            tickfont=dict(
                color="black"
            ),
            title_font=dict(
                color="black"
            )
        ),

        margin=dict(
            l=20,
            r=20,
            t=30,
            b=20
        )
    )

    st.plotly_chart(
        interest_chart,
        use_container_width=True
    )


# ==========================================
# กราฟที่ 2 ค่างวดต่อเดือน
# ==========================================

with chart_col2:

    st.write(
        "**เปรียบเทียบค่างวดผ่อนต่อเดือน (บาท/เดือน)**"
    )

    monthly_chart = px.bar(
        df,
        x="company_name",
        y="monthly_payment",
        text="monthly_payment",
        color="company_name",
        color_discrete_map={
            "A": "#72C3A5",
            "B": "#F58A61",
            "C": "#8FA0CC",
            "D": "#D67FC0",
            "E": "#A8D84E"
        }
    )

    # ตัวเลขบนแท่งกราฟ
    monthly_chart.update_traces(
        texttemplate="%{text:,.2f}",
        textposition="outside",
        textfont=dict(
            color="black"
        )
    )

    # ตั้งค่าสีตัวอักษรทั้งหมดในกราฟ
    monthly_chart.update_layout(
        xaxis_title="บริษัทสินเชื่อ",
        yaxis_title="ค่างวด/เดือน (บาท)",

        plot_bgcolor="white",
        paper_bgcolor="white",

        font=dict(
            color="black"
        ),

        xaxis=dict(
            tickfont=dict(
                color="black"
            ),
            title_font=dict(
                color="black"
            )
        ),

        yaxis=dict(
            tickfont=dict(
                color="black"
            ),
            title_font=dict(
                color="black"
            )
        ),

        legend=dict(
            font=dict(
                color="black"
            ),
            title_font=dict(
                color="black"
            )
        ),

        margin=dict(
            l=20,
            r=20,
            t=30,
            b=20
        )
    )

    st.plotly_chart(
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


# สร้างสำเนาข้อมูลสำหรับแสดง
display_df = df.copy()


# ==========================================
# จัดรูปแบบข้อมูล
# ==========================================

display_df["rate"] = display_df["rate"].map(
    lambda x: f"{x:.2f}%"
)

display_df["total_rate"] = display_df["total_rate"].map(
    lambda x: f"{x:,.2f}"
)

display_df["total_payment"] = display_df["total_payment"].map(
    lambda x: f"{x:,.2f}"
)

display_df["monthly_payment"] = display_df["monthly_payment"].map(
    lambda x: f"{x:,.2f}"
)


# ==========================================
# เปลี่ยนชื่อหัวตาราง
# ==========================================

display_df.columns = [
    "บริษัท",
    "ดอกเบี้ย/ปี",
    "ระยะเวลา (ปี)",
    "ดอกเบี้ยรวม (บาท)",
    "ยอดชำระรวม (บาท)",
    "ค่างวด/เดือน (บาท)"
]


# ==========================================
# แสดงตาราง
# ==========================================

st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True
)


st.divider()


# ==========================================
# สรุปข้อมูล
# ==========================================

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
