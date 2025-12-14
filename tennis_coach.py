import streamlit as st
import google.generativeai as genai
from PIL import Image
import os

# --- 페이지 설정 ---
st.set_page_config(
    page_title="Grand Slam AI Coach",
    page_icon="🏆",
    layout="wide"
)

# --- 헤더 ---
st.markdown("""
    <div style='text-align:center; padding-bottom: 20px;'>
        <h1 style='color:#1E88E5;'>🏆 Grand Slam AI Coach</h1>
        <p style='font-size:1.2rem;'>친구들과 함께 쓰는 월드 클래스 테니스 코치</p>
    </div>
    """, unsafe_allow_html=True)

# --- 사이드바: 자동 로그인 설정 ---
with st.sidebar:
    st.header("⚙️ 설정")
    
    # [핵심] 서버에 키가 있으면 자동 통과, 없으면 입력창 뜸
    if "GOOGLE_API_KEY" in st.secrets:
        api_key = st.secrets["GOOGLE_API_KEY"]
        st.success("✅ 정품 라이센스 인증됨")
    else:
        api_key = st.text_input("API Key 입력 (주인장 전용)", type="password")

    # 키가 없으면 여기서 멈춤
    if not api_key:
        st.warning("⚠️ API 키가 확인되지 않았습니다.")
        st.stop()

    genai.configure(api_key=api_key)

    st.markdown("---")
    st.subheader("👤 내 정보 설정")
    player_level = st.selectbox("내 레벨", ["입문 (테린이)", "초급 (2.5-3.0)", "중급 (3.5-4.0)", "상급 (4.5+)", "선수급"], index=2)
    play_style = st.selectbox("내 스타일", ["올라운더", "공격형 베이스라이너", "수비형 베이스라이너", "서브 앤 발리"], index=0)

# --- AI 설정 ---
try:
    model_text = genai.GenerativeModel('gemini-pro')
    model_vision = genai.GenerativeModel('gemini-pro-vision')
except Exception as e:
    st.error(f"모델 로딩 실패: {e}")

# --- AI 페르소나 ---
grand_slam_prompt = f"""
당신은 'Grand Slam AI'입니다. 세계 최고의 테니스 코치입니다.
사용자 레벨: {player_level}, 스타일: {play_style}.

원칙:
1. 부상 방지를 최우선으로 생각하세요.
2. 구체적인 동작(Drill)을 추천하세요.
3. 친근하지만 전문적인 말투를 쓰세요.
"""

def generate_response(prompt, image=None):
    full_prompt = [grand_slam_prompt, prompt]
    with st.spinner("코치가 분석 중입니다... 🎾"):
        try:
            if image:
                response = model_vision.generate_content(full_prompt + [image])
            else:
                response = model_text.generate_content(full_prompt)
            return response.text
        except Exception as e:
            return f"오류가 발생했습니다: {e}"

# --- 메인 화면 탭 ---
tab1, tab2, tab3 = st.tabs(["📸 자세 분석", "🧠 경기 전략", "💪 트레이닝"])

with tab1:
    st.header("자세 교정 & 분석")
    st.write("서브, 포핸드 등 고민되는 자세 사진을 올려보세요.")
    img = st.file_uploader("사진 업로드", type=["jpg", "png", "jpeg"])
    if img:
        st.image(img, use_column_width=True)
        if st.button("분석 시작"):
            st.markdown(generate_response("이 자세를 분석하고 교정해줘.", Image.open(img)))

with tab2:
    st.header("상대방 공략법")
    enemy = st.text_area("상대방 스타일을 적어주세요 (예: 발 빠른 수비형)")
    if st.button("공략법 보기"):
        st.markdown(generate_response(f"상대 특징: {enemy}. 이 상대를 이길 전략을 짜줘."))

with tab3:
    st.header("피지컬 & 멘탈")
    query = st.text_input("고민 입력 (예: 테니스 엘보 예방 운동)")
    if st.button("코칭 받기"):
        st.markdown(generate_response(query))
