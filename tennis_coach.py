import streamlit as st
import tempfile
import os
from openai import OpenAI

# 1. 페이지 설정
st.set_page_config(page_title="AI 테니스 코치", page_icon="🎾")

# 2. 제목
st.title("🎾 AI 테니스 코치")
st.write("당신의 테니스 영상을 AI가 분석해 드립니다!")

# 3. API 키 설정 (Streamlit Secrets에서 가져오기)
if "OPENAI_API_KEY" in st.secrets:
    api_key = st.secrets["OPENAI_API_KEY"]
else:
    api_key = st.text_input("OpenAI API Key를 입력하세요", type="password")

# 4. 탭 생성 (여기가 중요! 탭이 2개 만들어집니다)
tab1, tab2 = st.tabs(["홈", "🎥 스윙 영상 분석"])

# --- 탭 1: 홈 화면 ---
with tab1:
    st.header("환영합니다!")
    st.write("위의 '스윙 영상 분석' 탭을 눌러서 영상을 올려보세요.")
    st.info("아이폰이나 갤럭시로 찍은 서브/스트로크 영상을 올리면 AI가 조언을 해줍니다.")

# --- 탭 2: 영상 분석 기능 ---
with tab2:
    st.header("스윙 영상 업로드")
    
    # 파일 업로더 (mp4, mov 지원)
    uploaded_file = st.file_uploader("영상을 선택하세요", type=['mp4', 'mov', 'avi'])

    if uploaded_file is not None:
        # 영상 미리보기
        st.video(uploaded_file)
        
        analyze_button = st.button("AI 분석 시작하기")
        
        if analyze_button and api_key:
            client = OpenAI(api_key=api_key)
            
            with st.spinner("AI가 영상을 보고 있습니다... 잠시만 기다려주세요 (약 30초)"):
                try:
                    # 1. 임시 파일로 저장
                    tfile = tempfile.NamedTemporaryFile(delete=False) 
                    tfile.write(uploaded_file.read())
                    
                    # 2. 텍스트로 시뮬레이션 (실제 비전 기능 연동 전 단계)
                    # 실제 비전 API는 복잡하므로, 우선 연결 확인을 위해 텍스트로 응답을 받습니다.
                    response = client.chat.completions.create(
                        model="gpt-4o",  # GPT-4o 모델 사용
                        messages=[
                            {"role": "system", "content": "당신은 세계적인 테니스 코치입니다. 사용자가 영상을 올렸다고 가정하고, 테니스 서브를 잘하는 일반적인 팁 3가지를 알려주세요."},
                            {"role": "user", "content": "내 서브 자세 좀 봐줘. 피드백 부탁해!"}
                        ]
                    )
                    
                    # 3. 결과 출력
                    result = response.choices[0].message.content
                    st.success("분석 완료!")
                    st.markdown(result)
                    
                except Exception as e:
                    st.error(f"에러가 발생했습니다: {e}")
        elif analyze_button and not api_key:
            st.warning("API 키가 필요합니다!")
