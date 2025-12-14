import streamlit as st
import cv2
import tempfile
import os
import base64
from openai import OpenAI

# 1. 페이지 설정 (레이아웃을 넓게 써서 읽기 편하게 함)
st.set_page_config(page_title="이교수의 테니스 아카데미", page_icon="🎾", layout="wide")

# 2. 스타일링 (가독성을 위한 CSS)
st.markdown("""
    <style>
    .big-font { font-size:20px !important; font-weight: 500; }
    .highlight { background-color: #f0f2f6; padding: 10px; border-radius: 5px; border-left: 5px solid #ff4b4b; }
    .tip-box { background-color: #e8f4f8; padding: 15px; border-radius: 10px; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

# 3. 제목 헤더
st.markdown("""
    <h1 style='text-align: left; margin-bottom: 0px;'>🎾 이교수의 테니스 아카데미</h1>
    <h5 style='text-align: left; color: gray; margin-top: -5px;'>Theory & Practice by Prof. Lee</h5>
    <hr>
""", unsafe_allow_html=True)

# 4. API 키 설정
if "OPENAI_API_KEY" in st.secrets:
    api_key = st.secrets["OPENAI_API_KEY"]
else:
    api_key = st.text_input("OpenAI API Key를 입력하세요", type="password")

# --- 내부 함수: 영상 프레임 추출 (AI 비전용) ---
def extract_frames(video_path, num_frames=5):
    video = cv2.VideoCapture(video_path)
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    step = max(total_frames // num_frames, 1)
    base64_frames = []
    for i in range(0, total_frames, step):
        video.set(cv2.CAP_PROP_POS_FRAMES, i)
        success, frame = video.read()
        if not success: break
        height, width = frame.shape[:2]
        new_width = 512
        new_height = int(height * (new_width / width))
        frame = cv2.resize(frame, (new_width, new_height))
        _, buffer = cv2.imencode(".jpg", frame)
        base64_frames.append(base64.b64encode(buffer).decode("utf-8"))
        if len(base64_frames) >= num_frames: break
    video.release()
    return base64_frames

# 5. 탭 구성 (교육적 깊이를 더한 5단계 구성)
tabs = st.tabs([
    "🏠 아카데미 홈", 
    "📖 1강: 테니스의 철학", 
    "🖐️ 2강: 그립과 스탠스", 
    "⚡ 3강: 스트로크 메커니즘", 
    "🚀 4강: 서브 마스터 클래스", 
    "🎥 실전: AI 스윙 분석"
])

# --- 탭 1: 홈 ---
with tabs[0]:
    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader("환영합니다, 예비 테니스 마스터 여러분.")
        st.markdown("""
        <div class="big-font">
        테니스는 단순히 공을 넘기는 운동이 아닙니다.<br>
        물리학, 생체역학, 그리고 심리학이 결합된 <b>종합 예술</b>입니다.
        </div>
        """, unsafe_allow_html=True)
        
        st.write("")
        st.markdown("""
        이 앱은 단순한 스윙 분석기를 넘어, 여러분에게 테니스의 **'원리'**를 가르쳐드리기 위해 설계되었습니다.
        
        **[학습 로드맵]**
        1. **테니스의 철학:** 왜 힘을 빼야 하는가? 확률 테니스란 무엇인가?
        2. **기본기:** 그립 하나가 구질을 어떻게 바꾸는가?
        3. **메커니즘:** 몸통 회전(Kinetic Chain)은 어떻게 이루어지는가?
        4. **AI 실전:** 이론을 바탕으로 내 자세를 교정받는다.
        """)
    
    with col2:
        st.info("""
        **💡 오늘의 명언**
        
        "좋은 샷은 좋은 발(Footwork)에서 나오고,
        위대한 승리는 차분한 머리(Mental)에서 나온다."
        
        - 이교수
        """)

# --- 탭 2: 테니스의 철학 ---
with tabs[1]:
    st.header("📖 1강: 테니스를 관통하는 원리")
    
    with st.expander("1. 힘을 빼야 힘이 생긴다 (탈력의 역설)", expanded=True):
        st.markdown("""
        많은 초보자가 '강한 샷'을 치기 위해 온몸에 힘을 줍니다. 하지만 이것은 가장 큰 실수입니다.
        
        * **경직의 문제:** 근육이 긴장하면 스윙 속도가 느려지고 부상 위험이 커집니다.
        * **채찍 효과 (Whip Effect):** 테니스 라켓은 채찍과 같습니다. 손잡이를 잡은 손(그립)은 부드러워야 라켓 헤드가 가속되어 공을 때립니다.
        * **이교수의 조언:** 임팩트 순간을 제외하고는 라켓을 쥔 손에 계란을 쥐듯 힘을 빼세요.
        """)

    with st.expander("2. 확률 테니스 (Percentage Tennis)"):
        st.markdown("""
        테니스는 '누가 더 멋진 샷을 치느냐'가 아니라 **'누가 실수를 덜 하느냐'**의 게임입니다.
        
        * **네트의 높이:** 네트 중앙(0.914m)이 양쪽 끝보다 낮습니다. 중앙으로 치는 것이 안전합니다.
        * **크로스 샷의 법칙:** 크로스(대각선) 코트가 다운더라인(직선)보다 길이가 깁니다. 즉, 아웃될 확률이 낮습니다.
        * **결론:** 무리해서 라인을 노리지 마세요. 코트 안쪽 깊숙이 밀어 넣는 것이 고수의 전략입니다.
        """)

# --- 탭 3: 그립과 스탠스 ---
with tabs[2]:
    st.header("🖐️ 2강: 그립과 스탠스 (Foundation)")
    st.markdown("모든 기술의 시작은 올바른 그립과 발의 위치에서 시작됩니다.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("1. 그립 (The Grip)")
        st.markdown("""
        **📍 컨티넨탈 그립 (Continental)**
        * **방법:** 라켓을 칼날처럼 세워 악수하듯 잡습니다. (인덱스 너클: 2번 베벨)
        * **용도:** 서브, 발리, 스매싱, 슬라이스 (필수 마스터)
        
        **📍 이스턴 그립 (Eastern)**
        * **방법:** 라켓 면에 손바닥을 대고 그대로 내려 잡습니다. (인덱스 너클: 3번 베벨)
        * **용도:** 플랫 성향의 포핸드. 타점이 앞에서 형성됩니다.
        
        **📍 세미 웨스턴 (Semi-Western)**
        * **방법:** 라켓을 바닥에 놓고 위에서 덮어 잡습니다. (인덱스 너클: 4번 베벨)
        * **용도:** 현대 테니스의 표준. 강한 탑스핀을 걸기 유리합니다.
        """)
        
    with col2:
        st.subheader("2. 스탠스 (The Stance)")
        st.markdown("""
        **👣 오픈 스탠스 (Open Stance)**
        * 몸이 정면을 향한 상태.
        * **장점:** 준비 시간이 짧고, 모던 포핸드에서 허리 회전을 극대화할 수 있습니다.
        
        **👣 뉴트럴/클로즈드 스탠스 (Neutral/Closed)**
        * 옆으로 서서 치는 자세.
        * **장점:** 체중 이동(뒤→앞)을 확실하게 실을 수 있어 정확도가 높습니다. 초보자는 여기서 시작하세요.
        """)

# --- 탭 4: 스트로크 메커니즘 ---
with tabs[3]:
    st.header("⚡ 3강: 스트로크 메커니즘")
    st.markdown("공을 치는 것이 아닙니다. 공을 '보내는' 것입니다.")
    
    st.markdown("### 🎾 포핸드 (Forehand) 3단계")
    st.info("**핵심:** 팔로 치지 말고 **'몸통(Core)'**으로 치세요.")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**1. 유닛 턴 (Unit Turn)**")
        st.write("공이 오는 것을 인식하자마자, 어깨와 힙을 동시에 90도 회전합니다. 라켓은 아직 뒤로 빠지지 않아도 됩니다. 몸을 꼬아주는 것이 핵심입니다.")
    with col2:
        st.markdown("**2. 레그 드라이브 & 임팩트**")
        st.write("굽혔던 무릎을 펴면서 지면 반발력을 이용합니다. 타점은 반드시 **'앞발보다 앞'**에서 형성되어야 체중이 실립니다.")
    with col3:
        st.markdown("**3. 팔로우스루 (Follow-through)**")
        st.write("라켓을 공 쪽으로 던진다는 느낌으로 길게 뻗어주세요. 라켓 끝이 반대쪽 어깨나 허리춤으로 자연스럽게 넘어와야 합니다.")

    st.markdown("---")
    st.markdown("### 🛡️ 백핸드 (Backhand)")
    st.write("백핸드는 포핸드보다 어렵지만, 구조적으로 더 견고할 수 있습니다. **'어깨 턴'**이 포핸드보다 더 깊숙이 들어가야 합니다. (등이 보일 정도로)")

# --- 탭 5: 서브 마스터 클래스 ---
with tabs[4]:
    st.header("🚀 4강: 서브 (The Serve)")
    st.markdown("테니스에서 유일하게 내가 통제할 수 있는 샷입니다. 게임의 시작이자 가장 강력한 무기입니다.")
    
    with st.expander("Step 1: 토스 (The Toss) - 서브의 80%", expanded=True):
        st.write("""
        많은 분들이 서브가 안 들어가면 폼을 고치려 하지만, 사실 80%는 토스 문제입니다.
        * **위치:** 머리 위가 아니라, **오른쪽 눈 1시 방향 앞쪽**에 올려두세요.
        * **높이:** 라켓을 뻗었을 때 닿을락 말락 한 높이가 이상적입니다.
        * **팁:** 공을 손가락 끝으로 잡고, 엘리베이터가 올라가듯 부드럽게 올리세요.
        """)
        
    with st.expander("Step 2: 트로피 자세 (Trophy Position)"):
        st.write("""
        무릎을 굽히고 라켓을 등 뒤로 떨어뜨린 자세가 트로피 위의 동상과 같다 하여 붙여진 이름입니다.
        * 이때 몸은 활처럼 휘어져 탄력을 축적해야 합니다.
        """)
        
    with st.expander("Step 3: 프로네이션 (Pronation) - 파워의 원천"):
        st.write("""
        임팩트 순간 손목을 바깥쪽으로 채주는 동작입니다. (마치 부채질하듯이)
        * 이 동작이 없으면 서브는 그저 '후라이팬 뒤집기'가 되어 힘이 실리지 않습니다.
        """)

# --- 탭 6: AI 스윙 분석 ---
with tabs[5]:
    st.header("🎥 실전: AI 스윙 정밀 분석")
    st.markdown("""
    <div class="tip-box">
    <b>👨‍🏫 이교수의 가이드:</b><br>
    앞서 배운 이론들이 내 몸에 적용되고 있는지 확인할 시간입니다.<br>
    영상을 업로드하면 AI가 <b>주요 장면 5컷</b>을 추출하여 정밀 분석합니다.
    </div>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader("분석할 영상을 선택해주세요 (10초 이내 권장)", type=['mp4', 'mov', 'avi'])

    if uploaded_file is not None:
        st.video(uploaded_file)
        shot_type = st.radio("분석할 동작 선택", ["포핸드", "백핸드", "서브", "발리/스매싱"], horizontal=True)
        
        if st.button("이교수님, 분석 부탁드립니다 (Start)"):
            if not api_key:
                st.error("API 키가 설정되지 않았습니다. (Secrets 설정 필요)")
            else:
                client = OpenAI(api_key=api_key)
                
                with st.spinner(f"{shot_type} 동작을 프레임 단위로 해부하고 있습니다..."):
                    try:
                        # 1. 임시 파일 저장 및 프레임 추출
                        tfile = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
                        tfile.write(uploaded_file.read())
                        tfile.close()
                        
                        frames = extract_frames(tfile.name, num_frames=5)
                        os.unlink(tfile.name) # 청소

                        # 2. AI 분석 요청
                        messages = [
                            {
                                "role": "system",
                                "content": """
                                당신은 스포츠 과학자이자 테니스 마스터 '이교수'입니다. 
                                사용자의 영상을 프레임 단위로 분석하여 다음 구조로 답변하세요:
                                1. 칭찬 (Good Point): 잘된 점 하나를 찾아 격려하세요.
                                2. 문제점 진단 (Diagnosis): 가장 시급히 고쳐야 할 문제 1가지를 지적하세요. (예: 타점, 무릎 굽힘, 팔로우스루 등)
                                3. 이교수의 처방 (Prescription): 구체적인 교정 훈련법을 제시하세요.
                                말투는 정중하고 전문적이며 교육적이어야 합니다.
                                """
                            },
                            {
                                "role": "user",
                                "content": [
                                    {"type": "text", "text": f"나의 {shot_type} 영상입니다. 5장의 연속 이미지를 보고 분석해주세요."},
                                ]
                            }
                        ]
                        
                        for frame in frames:
                            messages[1]["content"].append({
                                "type": "image_url",
                                "image_url": {"url": f"data:image/jpeg;base64,{frame}"}
                            })

                        response = client.chat.completions.create(
                            model="gpt-4o",
                            messages=messages,
                            max_tokens=1500
                        )
                        
                        result = response.choices[0].message.content
                        st.success("분석이 완료되었습니다.")
                        st.markdown("### 📋 이교수의 분석 리포트")
                        st.markdown(result)
                        
                    except Exception as e:
                        st.error(f"오류가 발생했습니다: {e}")
