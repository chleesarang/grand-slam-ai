import streamlit as st
import cv2  # 영상을 자르는 도구
import tempfile
import os
import base64
from openai import OpenAI

# 1. 페이지 설정
st.set_page_config(page_title="이교수의 AI 테니스", page_icon="🎾", layout="wide")

# 2. 제목 설정
st.markdown("""
    <h1 style='text-align: left; margin-bottom: 0px;'>🎾 AI 테니스 코치</h1>
    <h5 style='text-align: left; color: gray; margin-top: -10px;'>by 이교수</h5>
    <hr>
""", unsafe_allow_html=True)

# 3. API 키 설정
if "OPENAI_API_KEY" in st.secrets:
    api_key = st.secrets["OPENAI_API_KEY"]
else:
    api_key = st.text_input("OpenAI API Key를 입력하세요", type="password")

# --- 내부 함수: 영상을 이미지 프레임으로 변환 ---
def extract_frames(video_path, num_frames=5):
    """영상에서 균등한 간격으로 프레임을 추출하여 base64로 변환"""
    video = cv2.VideoCapture(video_path)
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    step = max(total_frames // num_frames, 1)
    
    base64_frames = []
    for i in range(0, total_frames, step):
        video.set(cv2.CAP_PROP_POS_FRAMES, i)
        success, frame = video.read()
        if not success:
            break
        # 이미지가 너무 크면 비용이 많이 드므로 리사이징 (폭 512px)
        height, width = frame.shape[:2]
        new_width = 512
        new_height = int(height * (new_width / width))
        frame = cv2.resize(frame, (new_width, new_height))
        
        _, buffer = cv2.imencode(".jpg", frame)
        base64_frames.append(base64.b64encode(buffer).decode("utf-8"))
        
        if len(base64_frames) >= num_frames:
            break
    video.release()
    return base64_frames

# 4. 탭 구성
tab1, tab2, tab3, tab4 = st.tabs(["🏠 홈", "📖 핵심 기술 가이드", "🖐️ 그립 완전 정복", "🎥 AI 스윙 분석"])

# (탭 1, 2, 3 내용은 동일하게 유지 - 공간 절약을 위해 생략했지만 기존 내용 그대로 둡니다)
with tab1:
    st.subheader("환영합니다! 이교수의 테니스 연구소입니다.")
    st.write("이제 AI가 당신의 영상을 **실제로 보고** 분석합니다.")

with tab2:
    st.header("테니스 3대 핵심 기술")
    st.write("포핸드, 백핸드, 서브의 기본 원리를 익히세요.")

with tab3:
    st.header("상황별 그립 가이드")
    st.write("컨티넨탈, 이스턴, 세미 웨스턴 그립을 상황에 맞게 잡으세요.")

# --- 탭 4: 진짜 AI 스윙 분석 ---
with tab4:
    st.header("🎥 AI 스윙 정밀 분석 (Real Vision)")
    st.info("💡 영상을 올리면 AI가 주요 장면 5컷을 보고 정밀 분석합니다. (API 비용 발생)")

    uploaded_file = st.file_uploader("분석할 영상을 선택해주세요", type=['mp4', 'mov', 'avi'])

    if uploaded_file is not None:
        st.video(uploaded_file)
        shot_type = st.radio("어떤 샷인가요?", ["포핸드", "백핸드", "서브", "발리"], horizontal=True)
        
        if st.button("AI 분석 시작 (Real Vision)"):
            if not api_key:
                st.error("API 키가 필요합니다. Secrets에 설정하거나 위에 입력하세요.")
            else:
                client = OpenAI(api_key=api_key)
                
                with st.spinner(f"영상을 프레임 단위로 분석 중입니다... (약 15~30초 소요)"):
                    try:
                        # 1. 영상을 임시 파일로 저장
                        tfile = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
                        tfile.write(uploaded_file.read())
                        tfile.close()
                        
                        # 2. 영상에서 이미지 추출 (OpenCV 사용)
                        frames = extract_frames(tfile.name, num_frames=5)
                        
                        # 3. 임시 파일 삭제
                        os.unlink(tfile.name)

                        # 4. AI에게 이미지와 질문 전송
                        # 이미지를 리스트로 묶어서 보냄
                        messages = [
                            {
                                "role": "system",
                                "content": "당신은 세계적인 테니스 코치 '이교수'입니다. 제공된 이미지들은 사용자의 스윙 영상에서 추출한 연속된 장면입니다. 자세, 라켓의 위치, 시선 등을 정밀하게 분석하여 교정할 점 3가지를 알려주세요."
                            },
                            {
                                "role": "user",
                                "content": [
                                    {"type": "text", "text": f"이것은 나의 {shot_type} 동작입니다. 자세를 분석해주세요."},
                                ]
                            }
                        ]
                        
                        # 추출된 프레임들을 메시지에 추가
                        for frame in frames:
                            messages[0]["content"] += " (이미지 첨부됨)" # 시스템 메시지 보강
                            messages[1]["content"].append({
                                "type": "image_url",
                                "image_url": {"url": f"data:image/jpeg;base64,{frame}"}
                            })

                        response = client.chat.completions.create(
                            model="gpt-4o",
                            messages=messages,
                            max_tokens=1000
                        )
                        
                        result = response.choices[0].message.content
                        st.success("분석 완료!")
                        st.markdown("### 📋 이교수의 정밀 분석 리포트")
                        st.markdown(result)
                        
                    except Exception as e:
                        st.error(f"오류가 발생했습니다: {e}")
