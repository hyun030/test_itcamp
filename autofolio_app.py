import streamlit as st
import time

# --- 페이지 설정 ---
st.set_page_config(
    page_title="FitFolio - AI 포트폴리오",
    page_icon="✨",
    layout="wide"
)

# --- CSS 스타일 ---
# 이전 코드의 CSS를 st.markdown을 사용해 문자열로 주입 (오류 해결)
st.markdown("""
<style>
    /* --- 기본 및 레이아웃 스타일 --- */
    :root {
        --primary-color: #5A67D8;
        --primary-hover: #434190;
        --secondary-color: #F7FAFC;
        --text-color: #2D3748;
        --subtext-color: #718096;
        --border-color: #E2E8F0;
        --highlight-bg: #E9D8FD;
        --highlight-text: #5A67D8;
        --green-light: #C6F6D5;
        --green-dark: #38A169;
    }
    /* Streamlit의 메인 콘텐츠 영역에 대한 스타일 조정 */
    .main .block-container {
        max-width: 1200px;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        padding: 0.8rem 1.8rem;
        font-weight: 700;
        background-color: var(--primary-color);
        color: white;
        border: none;
    }
    .stButton>button:hover {
        background-color: var(--primary-hover);
        color: white;
        border: none;
    }
    .stButton>button:disabled {
        background-color: #A0AEC0;
        cursor: not-allowed;
    }
    h1, h2, h3, h4 { font-weight: 900; letter-spacing: -0.5px; }
    .text-center { text-align: center; }

    /* --- 페이지별 스타일 --- */
    .landing-container { text-align: center; padding: 4rem 1rem; }
    .landing-container h1 { font-size: 3rem; margin-bottom: 1rem; }
    .landing-container .highlight { color: var(--primary-color); }
    .landing-container p { font-size: 1.2rem; color: var(--subtext-color); max-width: 600px; margin: 0 auto 2rem; }

    .connect-card {
        display: flex; align-items: center; padding: 1.5rem; border: 1px solid var(--border-color);
        border-radius: 10px; background-color: white; margin-bottom: 1rem;
    }
    .connect-card .icon { width: 40px; height: 40px; margin-right: 1.5rem; }
    .connect-card .info { flex-grow: 1; }
    .connect-card .info h3 { font-size: 1.2rem; margin-bottom: 0.2rem; margin-top: 0; }
    .connect-card .info p { color: var(--subtext-color); font-size: 0.9rem; margin-bottom: 0; }
    
    .input-form { max-width: 500px; margin: 0 auto; background: white; padding: 2rem; border-radius: 12px; }

    .spinner-container { text-align: center; padding: 5rem 0; }
    
    .result-header { text-align: center; margin-bottom: 3rem; }
    .result-header h2 { font-size: 2.5rem; }
    .result-header .company-name { color: var(--primary-color); }

    .card {
        background: white; border-radius: 12px; padding: 2rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        margin-bottom: 1.5rem;
    }
    .portfolio-section h3 {
        font-size: 1.5rem; margin-bottom: 1rem; padding-bottom: 0.5rem;
        border-bottom: 2px solid var(--border-color); display: flex; align-items: center;
    }
    .portfolio-section h3 .icon-emoji { margin-right: 0.75rem; }
    
    #ai-summary-card { background-color: #F0F4FF; border-left: 4px solid var(--primary-color); }
    
    .skills-grid { display: flex; flex-wrap: wrap; gap: 0.8rem; }
    .skill-tag {
        padding: 0.5rem 1rem; border-radius: 20px;
        background-color: var(--secondary-color); font-weight: 500;
    }
    .skill-tag.highlighted {
        background-color: var(--highlight-bg); color: var(--highlight-text); font-weight: 700;
    }
    
    .project-card { border: 1px solid var(--border-color); padding: 1.5rem; border-radius: 10px; margin-bottom: 1.5rem; }
    .ai-rewrite {
        margin-top: 1.5rem; padding: 1rem; background-color: #F0FFF4;
        border-left: 4px solid var(--green-dark); border-radius: 4px;
    }
    .rewrite-header { display: flex; align-items: center; font-weight: 700; color: var(--green-dark); margin-bottom: 0.5rem; }
</style>
""", unsafe_allow_html=True)


# --- 세션 상태(Session State) 초기화 ---
# 페이지 전환을 관리하기 위해 사용
if 'page' not in st.session_state:
    st.session_state.page = 'landing'
if 'connected_platforms' not in st.session_state:
    st.session_state.connected_platforms = set()
if 'company' not in st.session_state:
    st.session_state.company = ''
if 'job' not in st.session_state:
    st.session_state.job = ''

# --- 더미 데이터 (시뮬레이션용) ---
USER_PROFILE = {
    'skills': ['Python', 'PyTorch', 'TensorFlow', 'LLM', 'On-Device AI', 'React', 'Data Analysis'],
    'projects': [
        {
            'title': '모바일 기기용 이미지 분류 모델 경량화',
            'description': 'TensorFlow Lite를 사용하여 CNN 모델의 크기를 줄이고, 모바일 환경에서의 추론 속도를 30% 개선한 프로젝트입니다.',
            'relatedSkills': ['Python', 'TensorFlow', 'On-Device AI']
        },
        {
            'title': '소셜 미디어 감성 분석 모델',
            'description': 'LSTM 기반의 딥러닝 모델을 사용하여 소셜 미디어 텍스트의 긍정/부정을 분류하는 프로젝트를 진행했습니다.',
            'relatedSkills': ['Python', 'PyTorch', 'LLM']
        },
    ]
}

# --- 페이지 전환 함수 ---
def change_page(page_name):
    st.session_state.page = page_name

# --- 각 페이지를 그리는 함수들 ---

def show_landing_page():
    st.markdown("""
    <div class="landing-container">
        <h1>당신의 커리어, <span class="highlight">AI가 맞춤 설계</span>합니다.</h1>
        <p>FitFolio는 흩어진 당신의 경험을 모아 지원하는 기업에 맞춰 포트폴리오를 자동으로 재구성해주는 가장 스마트한 방법입니다.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("내 포트폴리오 만들기"):
        change_page('connect')
        st.rerun()

def show_connect_page():
    st.markdown('<h2 class="text-center">1. 데이터 연동하기</h2>', unsafe_allow_html=True)
    
    platforms = {
        "github": {"name": "GitHub", "desc": "프로젝트와 코드를 가져옵니다.", "icon": "https://simpleicons.org/icons/github.svg"},
        "linkedin": {"name": "LinkedIn", "desc": "경력과 학력을 가져옵니다.", "icon": "https://simpleicons.org/icons/linkedin.svg"},
        "tistory": {"name": "블로그 (Tistory)", "desc": "작성한 글과 전문성을 가져옵니다.", "icon": "https://simpleicons.org/icons/tistory.svg"},
        "behance": {"name": "Behance", "desc": "디자인 작업물을 가져옵니다.", "icon": "https://simpleicons.org/icons/behance.svg"},
    }

    for key, val in platforms.items():
        is_connected = key in st.session_state.connected_platforms
        button_text = "연동 완료 ✔" if is_connected else "연동하기"
        
        st.markdown(f"""
        <div class="connect-card">
            <img src="{val['icon']}" class="icon">
            <div class="info">
                <h3>{val['name']}</h3>
                <p>{val['desc']}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # 버튼을 카드 밖에 배치하여 클릭 이벤트 처리
        if st.button(button_text, key=key, disabled=is_connected):
            st.session_state.connected_platforms.add(key)
            st.rerun() # 버튼 클릭 시 화면 새로고침

    st.markdown("<br>", unsafe_allow_html=True)
    
    is_ready = len(st.session_state.connected_platforms) > 0
    if st.button("다음 단계로", disabled=not is_ready):
        change_page('input')
        st.rerun()

def show_input_page():
    st.markdown('<h2 class="text-center">2. 포트폴리오 맞춤화</h2>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="input-form">', unsafe_allow_html=True)
        company = st.text_input("지원 회사명", placeholder="예: 삼성전자")
        job = st.text_input("지원 직무", placeholder="예: AI 연구원")
        
        if st.button("AI 맞춤 포트폴리오 생성"):
            if not company or not job:
                st.warning("회사명과 직무를 모두 입력해주세요.")
            else:
                st.session_state.company = company
                st.session_state.job = job
                change_page('analysis')
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

def show_analysis_page():
    st.markdown('<div class="spinner-container">', unsafe_allow_html=True)
    messages = [
        f"'{st.session_state.company}'의 최신 기술 블로그를 분석 중입니다...",
        "채용 공고의 핵심 요구 역량을 추출하고 있습니다...",
        f"'{st.session_state.job}' 직무와 회원님의 경험 데이터 매칭 중...",
        "프로젝트 설명을 AI가 재구성하는 중...",
        "맞춤 포트폴리오 생성 완료!"
    ]
    
    with st.spinner("AI가 분석 중입니다... 잠시만 기다려 주세요."):
        for i, message in enumerate(messages):
            st.text(message)
            time.sleep(1.5) # 실제 작업 대신 시간 지연
    
    st.markdown('</div>', unsafe_allow_html=True)
    change_page('result')
    st.rerun()


def show_result_page():
    # 헤더
    st.markdown(f"""
    <header class="result-header">
        <h2><span class="company-name">{st.session_state.company}</span> 맞춤 포트폴리오</h2>
        <p>FitFolio의 AI가 <strong>{st.session_state.job}</strong> 직무에 맞춰 재구성한 결과입니다.</p>
    </header>
    """, unsafe_allow_html=True)

    # AI 분석 요약
    st.markdown("""
    <div id="ai-summary-card" class="card portfolio-section">
        <h3><span class="icon-emoji">💡</span>AI 분석 요약</h3>
        <p>FitFolio AI가 분석한 '{company} {job}' 직무의 핵심은 <strong>'LLM 경량화'</strong>와 <strong>'온디바이스 AI'</strong> 경험입니다. 회원님의 경험을 이 키워드에 맞춰 강조하고 재구성했습니다.</p>
    </div>
    """.format(company=st.session_state.company, job=st.session_state.job), unsafe_allow_html=True)

    # 핵심 역량
    with st.container(border=False):
        st.markdown("""
        <div class="card portfolio-section">
            <h3><span class="icon-emoji">🎯</span>핵심 역량 (Skills)</h3>
            <div class="skills-grid">
        """, unsafe_allow_html=True)
        
        required_skills = ['On-Device AI', 'LLM', 'PyTorch']
        for skill in USER_PROFILE['skills']:
            highlight_class = "highlighted" if skill in required_skills else ""
            st.markdown(f'<div class="skill-tag {highlight_class}">{skill}</div>', unsafe_allow_html=True)
        
        st.markdown("</div></div>", unsafe_allow_html=True)

    # 프로젝트 재구성
    with st.container(border=False):
        st.markdown("""
        <div class="card portfolio-section">
            <h3><span class="icon-emoji">🚀</span>프로젝트 재구성 (Projects)</h3>
        """, unsafe_allow_html=True)
        
        for project in USER_PROFILE['projects']:
            st.markdown(f"""
            <div class="project-card">
                <h4>{project['title']}</h4>
                <p>{project['description']}</p>
                <div class="ai-rewrite">
                    <div class="rewrite-header">✨ AI Rewrite</div>
                    <p>'{st.session_state.company}'가 최근 집중하고 있는 <strong>'온디바이스 AI'</strong> 전략에 맞춰, <strong>TensorFlow Lite 기반 모델 경량화</strong> 경험을 강조했습니다. 이를 통해 제한된 하드웨어 환경에서의 효율적인 AI 모델 배포 및 운영 능력을 어필할 수 있습니다.</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    if st.button("처음으로 돌아가기"):
        # 세션 상태 초기화
        st.session_state.page = 'landing'
        st.session_state.connected_platforms = set()
        st.rerun()

# --- 메인 로직 ---
# 세션 상태에 따라 적절한 페이지를 표시
if st.session_state.page == 'landing':
    show_landing_page()
elif st.session_state.page == 'connect':
    show_connect_page()
elif st.session_state.page == 'input':
    show_input_page()
elif st.session_state.page == 'analysis':
    show_analysis_page()
elif st.session_state.page == 'result':
    show_result_page()
