# streamlit_ocean_dashboard_full.py
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import PchipInterpolator

# -----------------------------
# 페이지 상태 초기화
# -----------------------------
if 'page' not in st.session_state:
    st.session_state.page = "main"

# -----------------------------
# 메인 메뉴
# -----------------------------
def main_menu():
    st.set_page_config(page_title="🌊 해양 환경 대시보드", layout="wide")
    st.title("🌊 해양 환경 메인 메뉴")

    st.write(
        "최근 해수면과 해수온 상승으로 인해 바다 생태계가 심각하게 변화하고 있습니다."
    )
    st.write(
        "🌡️ 기후 위기의 심각성 및 ‘해수온 상승’이라는 근본 원인 탐구가 필요합니다.\n"
        "산호 백화, 해양 생물 서식지 파괴, 어류 폐사 등 다양한 문제가 발생하고 있습니다."
    )
    st.markdown("---")

    col1, col2 = st.columns([1,2])

    # -----------------------------
    # 왼쪽 메뉴: 백화현상
    # -----------------------------
    with col1:
        st.subheader("📌 탐색 메뉴")
        if st.button("1980년~2024년 백화현상 보기"):
            st.session_state.page = "bleach"

    # -----------------------------
    # 오른쪽: 해수면/해수온 시각화
    # -----------------------------
    with col2:
        st.subheader("🌊 해수면 & 해수온 상승")
        years = np.arange(1980,2025)
        sea_level = np.linspace(0,13.6,len(years))  # mm
        sea_temp = np.linspace(0,0.78,len(years))   # °C

        fig, ax1 = plt.subplots(figsize=(8,4))

        # 해수면
        color1 = "#1f77b4"
        ax1.set_xlabel("연도")
        ax1.set_ylabel("해수면 상승 (mm)", color=color1)
        line1, = ax1.plot(years, sea_level, color=color1, linewidth=3, label="해수면 상승 (mm)")
        ax1.set_ylim(0,15)
        ax1.tick_params(axis='y', labelcolor=color1)
        ax1.grid(alpha=0.3)

        # 해수면 값 표시 (5년 간격)
        for x, y in zip(years[::5], sea_level[::5]):
            ax1.text(x, y+0.3, f"{y:.1f}", color=color1, fontsize=9, ha="center")

        # 해수온
        ax2 = ax1.twinx()
        color2 = "#ff7f0e"
        ax2.set_ylabel("해수온 상승 (°C)", color=color2)
        line2, = ax2.plot(years, sea_temp, color=color2, linestyle="--", linewidth=3, label="해수온 상승 (°C)")
        ax2.set_ylim(0,1)
        ax2.tick_params(axis='y', labelcolor=color2)

        # 해수온 값 표시 (5년 간격)
        for x, y in zip(years[::5], sea_temp[::5]):
            ax2.text(x, y+0.02, f"{y:.2f}", color=color2, fontsize=9, ha="center")

        # 범례
        ax1.legend([line1,line2], ["해수면 상승 (mm)","해수온 상승 (°C)"], loc="upper left", fontsize=10)

        st.pyplot(fig)

        st.markdown(
            """
            - 1980년~2024년 동안 해수면은 약 13.6mm 상승했습니다.
            - 해수온은 약 0.78°C 상승했습니다.
            - 이러한 변화는 산호백화, 해양 생물 서식지 파괴, 어류 폐사 등 다양한 생태계 문제를 야기합니다.
            """
        )

    st.markdown("---")
    with st.expander("🌱 환경 보호 실천 방안", expanded=True):
        st.markdown(
            """
            **1️⃣ 탄소 배출 감소**  
            - 재생에너지 확대, 전기차·대중교통 활성화  
            - 산업·건물 에너지 효율 개선  

            **2️⃣ 해양 보호구역 확대**  
            - 어업·관광 제한 및 산호 복원 구역 조성  

            **3️⃣ 산호 복원 프로젝트**  
            - 건강한 산호를 양식 후 손상 지역에 이식  

            **4️⃣ 시민 참여 캠페인**  
            - 플라스틱 줄이기, 해안가 정화 봉사  
            - SNS 챌린지로 보호 인식 확대
            """
        )

# -----------------------------
# 백화현상 페이지
# -----------------------------
def bleach_page():
    st.title("📌 1980년~2024년 산호 백화 현황")
    
    if st.button("⬅️ 메인 메뉴로 돌아가기"):
        st.session_state.page = "main"
        return

    years_known = np.array([1980, 1998, 2010, 2015, 2024])
    bleach_known = np.array([5,21,37,68,84])
    years_all = np.arange(1980,2025)

    interp = PchipInterpolator(years_known, bleach_known)
    bleach = np.clip(interp(years_all),0,100)
    remain = 100 - bleach

    df = pd.DataFrame({
        "연도": years_all,
        "죽은 산호(%)": np.round(bleach,2),
        "남은 산호(%)": np.round(remain,2)
    })

    st.markdown(
        """
        📌 **설명:**  
        - 1980년 이후 지구 산호초의 백화율은 꾸준히 증가하고 있습니다.  
        - 2024년에는 약 84%가 백화를 겪은 것으로 추정됩니다.  
        - 기후 변화 완화와 해양 생태계 보호가 시급합니다.
        """
    )

    selected_year = st.select_slider(
        "연도를 선택하세요:",
        options=years_all,
        value=2000
    )
    row = df[df["연도"]==selected_year].iloc[0]

    st.markdown(f"### 📌 {selected_year}년 산호 상태")
    st.markdown(f"<h2 style='color:red'>죽은 산호: {row['죽은 산호(%)']}%</h2>", unsafe_allow_html=True)
    st.markdown(f"<h2 style='color:blue'>남은 산호: {row['남은 산호(%)']}%</h2>", unsafe_allow_html=True)

    fig, ax = plt.subplots(figsize=(8,4))
    ax.plot(years_all, bleach, color="red", linewidth=3, label="죽은 산호(%)")
    ax.plot(years_all, remain, color="blue", linewidth=3, label="남은 산호(%)")

    # 선택 연도 강조
    ax.scatter(selected_year, row["죽은 산호(%)"], color="red", s=80)
    ax.scatter(selected_year, row["남은 산호(%)"], color="blue", s=80)

    # 모든 5년 간격 수치 표시
    for x, y in zip(years_all[::5], bleach[::5]):
        ax.text(x, y+2, f"{y:.0f}%", color="red", fontsize=9, ha="center")
    for x, y in zip(years_all[::5], remain[::5]):
        ax.text(x, y+2, f"{y:.0f}%", color="blue", fontsize=9, ha="center")

    # 선택 연도 수치 상단 강조
    ax.text(selected_year, row["죽은 산호(%)"]+5, f"{row['죽은 산호(%)']}%", color="red", fontsize=12, fontweight='bold', ha="center")
    ax.text(selected_year, row["남은 산호(%)"]+5, f"{row['남은 산호(%)']}%", color="blue", fontsize=12, fontweight='bold', ha="center")

    ax.set_xlabel("연도", fontsize=12)
    ax.set_ylabel("비율(%)", fontsize=12)
    ax.set_ylim(0,105)
    ax.set_xlim(1979,2025)
    ax.grid(alpha=0.3)
    ax.legend(fontsize=10)
    st.pyplot(fig)

# -----------------------------
# 페이지 상태 표시
# -----------------------------
if st.session_state.page=="main":
    main_menu()
elif st.session_state.page=="bleach":
    bleach_page()