import streamlit as st
import datetime

# 1. 페이지 레이아웃 및 환경 설정
st.set_page_config(
    page_title="영한(Young) 더치페이 계산기 Pro",
    page_icon="💸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. 커스텀 CSS 스타일링 (카드 디자인, 버튼 스타일, 폰트 보정)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Noto Sans KR', sans-serif;
    }
    
    /* 메인 배경 및 컨테이너 */
    .main {
        background-color: #f4f6f9;
    }
    
    /* 카드 디자인 */
    .custom-card {
        background-color: #ffffff;
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.05);
        margin-bottom: 24px;
        border: 1px solid #eef2f6;
    }
    
    .custom-card h3 {
        margin-top: 0;
        color: #1e293b;
        font-weight: 700;
    }
    
    /* 강조 포인트 칼라 */
    .accent-text {
        color: #4F46E5;
        font-weight: bold;
    }
    
    /* 카카오톡 공유 영역 전용 */
    .share-box {
        background-color: #FEE500;
        color: #191919;
        border-radius: 12px;
        padding: 20px;
        font-family: monospace;
        white-space: pre-wrap;
        border: 1px solid #E2D000;
        font-size: 14px;
        line-height: 1.6;
    }
</style>
""", unsafe_allow_html=True)

# 3. 절사/올림 단위 변환 헬퍼 함수
def adjust_amount(amount, option):
    if option == "원 단위 그대로 유지":
        return amount
    elif option == "10원 미만 버림 (1원 단위 절사)":
        return (amount // 10) * 10
    elif option == "100원 미만 버림 (10원 단위 절사)":
        return (amount // 100) * 100
    elif option == "1000원 미만 버림 (100원 단위 절사)":
        return (amount // 1000) * 1000
    elif option == "10원 단위로 올림":
        return ((amount + 9) // 10) * 10
    elif option == "100원 단위로 올림":
        return ((amount + 99) // 100) * 100
    elif option == "1000원 단위로 올림":
        return ((amount + 999) // 1000) * 1000
    return amount

# 4. 사이드바 - 정산용 계좌번호 입력
st.sidebar.image("http://googleusercontent.com/image_collection/image_retrieval/4463309851671466293_0", use_container_width=True)
st.sidebar.markdown("### 🏦 정산 수령 정보")
st.sidebar.info("여기에 계좌 정보를 적어두면 카카오톡 정산 메시지에 자동으로 포함되어 복사하기 편해집니다!")

bank_name = st.sidebar.text_input("은행명", value="카카오뱅크")
account_number = st.sidebar.text_input("계좌번호", value="3333-01-1234567")
account_holder = st.sidebar.text_input("예금주", value="홍길동")
meeting_name = st.sidebar.text_input("모임 이름", value="주말 즐거운 모임 🍻")
meeting_date = st.sidebar.date_input("모임 날짜", datetime.date.today())

# 5. 메인 헤더 영역
col_header_left, col_header_right = st.columns([1.5, 1])

with col_header_left:
    st.title("💸 Young한 더치페이 계산기 Pro")
    st.markdown("""
    모임 후 정산할 때마다 머리 아프셨죠?  
    **차수별 멤버 제외, 깔끔한 원 단위 절사, 그리고 카톡 공유 문구 완성**까지 한 번에 끝내세요!  
    왼쪽 사이드바에 **수령 계좌**를 입력하면 원클릭 공유 템플릿이 자동으로 빌드됩니다.
    """)
    st.markdown("---")

with col_header_right:
    # 검색된 감성적인 파티/정산 이미지 노출
    st.image("http://googleusercontent.com/image_collection/image_retrieval/12683678613035568405_0", caption="즐거운 모임의 마무리를 깔끔하게!", use_container_width=True)

# 6. 정산 모드 선택 (탭 메뉴)
tab1, tab2 = st.tabs(["⚡ 간편 N분의 1 정산", "🍻 차수별 디테일 정산"])

# ---------------------------------------------------------
# Tab 1: 간편 정산 (N분의 1)
# ---------------------------------------------------------
with tab1:
    st.markdown('<div class="custom-card"><h3>🔢 간편 정산하기</h3><p>전체 비용을 균등하게 인원수대로 나눕니다.</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        total_amount = st.number_input("총 지출 금액 (원)", min_value=0, step=1000, value=78500, key="simple_total")
    with col2:
        num_people = st.number_input("함께한 인원수 (명)", min_value=1, step=1, value=5, key="simple_people")
        
    rounding_option = st.selectbox(
        "정산 금액 끝자리 단위 조정",
        ["원 단위 그대로 유지", "10원 미만 버림 (1원 단위 절사)", "100원 미만 버림 (10원 단위 절사)", "1000원 미만 버림 (100원 단위 절사)", "10원 단위로 올림", "100원 단위로 올림", "1000원 단위로 올림"],
        key="simple_round"
    )
    
    if st.button("🚀 간편 계산하기", type="primary", key="btn_simple"):
        if num_people > 0:
            exact_per_person = total_amount / num_people
            final_per_person = adjust_amount(int(exact_per_person), rounding_option)
            total_distributed = final_per_person * num_people
            difference = total_amount - total_distributed
            
            st.markdown("---")
            
            # 메트릭 표시
            m_col1, m_col2, m_col3 = st.columns(3)
            with m_col1:
                st.metric(label="1인당 송금액", value=f"{final_per_person:,} 원")
            with m_col2:
                st.metric(label="실제 총 정산액", value=f"{total_distributed:,} 원")
            with m_col3:
                st.metric(label="차액 (방장 부담 혹은 이득)", value=f"{difference:,} 원")
                
            # 카카오톡 공유 텍스트 빌드
            kakao_text = f"""[💰 {meeting_name} 정산 요청]

📅 일시: {meeting_date}
🏦 입금 계좌: {bank_name} {account_number} (예금주: {account_holder})

✨ 정산 인원: {num_people}명
💵 1인당 보낼 금액: {final_per_person:,}원

모두 고생하셨습니다! 따뜻한 송금 부탁드립니다 ⚡"""

            st.markdown("### 📋 카카오톡 공유 문구")
            st.caption("아래 노란색 상자의 텍스트를 드래그해서 복사(Ctrl+C)한 뒤 단톡방에 붙여넣기 하세요!")
            st.markdown(f'<div class="share-box">{kakao_text}</div>', unsafe_allow_html=True)
            st.balloons()
            
    st.markdown('</div>', unsafe_allow_html=True)


# ---------------------------------------------------------
# Tab 2: 차수별 상세 정산 (멀티 차수)
# ---------------------------------------------------------
with tab2:
    st.markdown('<div class="custom-card"><h3>🍻 차수별/멤버별 맞춤 정산</h3><p>1차만 참석한 사람, 2차부터 합류한 사람 등 복잡한 조건에 맞춰 정확하게 계산해 줍니다.</p>', unsafe_allow_html=True)
    
    # 참여자 입력
    members_input = st.text_input(
        "참여자들의 이름을 쉼표(,)로 구분해서 적어주세요.", 
        value="범준, 범수, 수민, 가윤, 유현,  승원",
        key="detail_members"
    )
    members = [m.strip() for m in members_input.split(",") if m.strip()]
    
    if len(members) < 2:
        st.warning("⚠️ 정확한 정산을 위해 최소 2명 이상의 이름을 입력해 주세요.")
    else:
        st.success(f"✔️ 정산 대상 ({len(members)}명): {', '.join(members)}")
        
        # 몇 차까지 진행되었는지 선택
        num_rounds = st.number_input("진행된 차수 선택 (최대 5차)", min_value=1, max_value=5, value=2, step=1)
        
        # 차수별 데이터 수집을 위한 딕셔너리
        rounds_data = {}
        
        # 멤버별 누적 정산금액 딕셔너리
        personal_debts = {member: 0 for member in members}
        
        st.markdown("---")
        
        # 각 차수별 동적 UI 생성
        for r in range(int(num_rounds)):
            st.markdown(f"#### 📍 {r+1}차 정산 내용 입력")
            col_r1, col_r2 = st.columns([1, 2])
            
            with col_r1:
                r_amount = st.number_input(f"{r+1}차 총 결제액 (원)", min_value=0, step=1000, value=0, key=f"r_amount_{r}")
            with col_r2:
                r_members = st.multiselect(
                    f"{r+1}차에 참여한 사람을 골라주세요",
                    options=members,
                    default=members,
                    key=f"r_members_{r}"
                )
            
            # 실시간 차수별 계산
            if r_amount > 0 and len(r_members) > 0:
                per_person_raw = r_amount / len(r_members)
                rounds_data[r] = {
                    "amount": r_amount,
                    "participants": r_members,
                    "per_person_raw": per_person_raw
                }
            st.markdown('<div style="height: 10px; border-bottom: 1px dashed #ddd; margin-bottom: 20px;"></div>', unsafe_allow_html=True)
            
        # 정산 단위 절사 방법 설정
        detail_rounding = st.selectbox(
            "정산 금액 끝자리 단위 조정 (차수 계산 후 최종 금액에 적용)",
            ["원 단위 그대로 유지", "10원 미만 버림 (1원 단위 절사)", "100원 미만 버림 (10원 단위 절사)", "1000원 미만 버림 (100원 단위 절사)", "10원 단위로 올림", "100원 단위로 올림", "1000원 단위로 올림"],
            key="detail_round"
        )
        
        if st.button("📊 상세 정산 결과 도출하기", type="primary", key="btn_detail_calc"):
            # 차수별 금액 합산 처리
            for r_idx, info in rounds_data.items():
                for p in info["participants"]:
                    personal_debts[p] += info["per_person_raw"]
            
            # 최종 절사 규칙 적용
            final_debts_adjusted = {}
            for p, amt in personal_debts.items():
                final_debts_adjusted[p] = adjust_amount(int(amt), detail_rounding)
                
            # 정산 리포트 및 메시지 작성
            st.markdown("### 🏆 최종 정산 결과 리포트")
            
            # 시각적으로 이쁜 결과 레이아웃 구성
            res_col1, res_col2 = st.columns(2)
            
            with res_col1:
                st.markdown("#### 👤 개인별 송금할 금액")
                for person, amount in final_debts_adjusted.items():
                    st.info(f"🙋‍♂️ **{person}** : {amount:,} 원")
                    
            with res_col2:
                st.markdown("#### 📝 차수별 요약 정보")
                for r_idx, info in rounds_data.items():
                    st.write(f"- **{r_idx+1}차**: 총 {info['amount']:,}원 / {len(info['participants'])}명 참여 (1인당 {int(info['per_person_raw']):,}원)")
            
            # 카카오톡 텍스트 빌드
            members_summary = ""
            for person, amount in final_debts_adjusted.items():
                members_summary += f"- {person}: {amount:,}원\n"
                
            rounds_summary_text = ""
            for r_idx, info in rounds_data.items():
                rounds_summary_text += f"   * {r_idx+1}차 ({info['amount']:,}원): {', '.join(info['participants'])}\n"

            kakao_detail_text = f"""[💰 {meeting_name} 차수별 정산 요청]

📅 일시: {meeting_date}
🏦 입금 계좌: {bank_name} {account_number} (예금주: {account_holder})

📋 정산 요약 및 참여현황:
{rounds_summary_text}
💵 멤버별 최종 송금액:
{members_summary}
모두 즐거웠습니다! 확인하시고 빠른 송금 부탁드려요 💸"""

            st.markdown("---")
            st.markdown("### 📋 카카오톡 단톡방 공유 문구")
            st.caption("아래 박스의 문구를 전체 선택 후 복사하여 사용해 보세요.")
            st.markdown(f'<div class="share-box">{kakao_detail_text}</div>', unsafe_allow_html=True)
            st.balloons()
            
    st.markdown('</div>', unsafe_allow_html=True)