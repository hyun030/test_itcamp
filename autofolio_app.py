import streamlit as st
import time

# --- 페이지 설정 ---
st.set_page_config(
    page_title="FitFolio - AI 포트폴리오",
    page_icon="✨",
    layout="wide"
)

# --- CSS 파일 로드 함수 ---
def local_css(file_name):
    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        st.error(f"'{file_name}' 파일을 찾을 수 없습니다. app.py와 동일한 폴더에 있는지 확인해주세요.")

local_css("styles.css")


# --- 세션 상태 초기화 ---
if 'page' not in st.session_state:
    st.session_state.page = 'landing'
if 'connected_platforms' not in st.session_state:
    st.session_state.connected_platforms = set()
if 'company' not in st.session_state:
    st.session_state.company = ''
if 'job' not in st.session_state:
    st.session_state.job = ''

# --- 더미 데이터 ---
USER_PROFILE = {
    'skills': ['Python', 'PyTorch', 'TensorFlow', 'LLM', 'On-Device AI', 'React', 'Data Analysis'],
    'projects': [
        {'title': '모바일 기기용 이미지 분류 모델 경량화', 'description': 'TensorFlow Lite를 사용하여 CNN 모델의 크기를 줄이고, 모바일 환경에서의 추론 속도를 30% 개선한 프로젝트입니다.'},
        {'title': '소셜 미디어 감성 분석 모델', 'description': 'LSTM 기반의 딥러닝 모델을 사용하여 소셜 미디어 텍스트의 긍정/부정을 분류하는 프로젝트를 진행했습니다.'},
    ]
}

# --- 페이지 전환 함수 ---
def change_page(page_name):
    st.session_state.page = page_name

# --- 공통 레이아웃 컴포넌트 ---
def show_header():
    st.markdown("""
    <header class="header">
        <div class="container">
            <div class="header-content">
                <div class="header-left">
                    <div class="logo-section">
                        <div class="logo"><span>F</span></div>
                        <span class="company-name">FitFolio</span>
                    </div>
                    <span class="badge badge-secondary">AI Portfolio</span>
                </div>
                <div class="custom-nav">
                    <a href="#" class="nav-link">포트폴리오</a>
                    <a href="#" class="nav-link">채용정보</a>
                    <button class="btn btn-outline" style="margin-left: 1rem;">로그인</button>
                </div>
            </div>
        </div>
    </header>
    """, unsafe_allow_html=True)

def show_footer():
    st.markdown("""
    <footer class="footer">
        <div class="container">
            <div class="footer-content">
                <p>&copy; 2025 FitFolio. All rights reserved.</p>
            </div>
        </div>
    </footer>
    """, unsafe_allow_html=True)

# --- 각 페이지 함수 ---

def show_landing_page():
    st.markdown("""
    <section class="hero">
        <div class="container">
            <div class="hero-content">
                <h1 class="hero-title">당신의 커리어, AI가 맞춤 설계합니다.</h1>
                <p class="hero-description">
                    FitFolio는 흩어진 당신의 경험을 모아 지원하는 기업에 맞춰 포트폴리오를 자동으로 재구성해주는 가장 스마트한 방법입니다.
                </p>
                <div id="landing-button-container"></div>
            </div>
        </div>
    </section>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        if st.button("내 포트폴리오 만들기", key="start_button", use_container_width=True):
            change_page('connect')
            st.rerun()

def show_connect_page():
    st.markdown("""
    <div class="container" style="text-align: center; padding-top: 3rem; padding-bottom: 3rem;">
        <h2 style="font-size: 2rem; font-weight: bold; margin-bottom: 2rem;">1. 데이터 연동하기</h2>
    </div>
    """, unsafe_allow_html=True)

    platforms = {
        "github": {"name": "GitHub", "desc": "프로젝트와 코드를 가져옵니다.", "icon": "https://simpleicons.org/icons/github.svg"},
        "linkedin": {"name": "LinkedIn", "desc": "경력과 학력을 가져옵니다.", "icon": "https://simpleicons.org/icons/linkedin.svg"},
        "tistory": {"name": "블로그 (Tistory)", "desc": "작성한 글과 전문성을 가져옵니다.", "icon": "https://simpleicons.org/icons/tistory.svg"},
        "behance": {"name": "Behance", "desc": "디자인 작업물을 가져옵니다.", "icon": "https://simpleicons.org/icons/behance.svg"},
    }
    
    cols = st.columns(4) 
    for col, (key, val) in zip(cols, platforms.items()):
        with col:
            is_connected = key in st.session_state.connected_platforms
            button_text = "연동 완료 ✔" if is_connected else "연동하기"
            
            st.markdown(f"""
            <div class="card" style="text-align: center; height: 100%;">
                <img src="{val['icon']}" style="width: 40px; height: 40px; margin: 0 auto 1rem auto;">
                <div style="flex-grow: 1;">
                    <h3 style="font-size: 1.2rem; margin-bottom: 0.2rem; margin-top: 0;">{val['name']}</h3>
                    <p style="color: #6b7280; font-size: 0.9rem; margin-bottom: 1.5rem;">{val['desc']}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(button_text, key=key, disabled=is_connected, use_container_width=True):
                st.session_state.connected_platforms.add(key)
                st.rerun()

    st.markdown("<br><br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        is_ready = len(st.session_state.connected_platforms) > 0
        if st.button("다음 단계로", disabled=not is_ready, use_container_width=True):
            change_page('input')
            st.rerun()

def show_input_page():
    st.markdown("""
    <div class="container" style="text-align: center; padding-top: 3rem; padding-bottom: 3rem;">
        <h2 style="font-size: 2rem; font-weight: bold; margin-bottom: 2rem;">2. 포트폴리오 맞춤화</h2>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.container(border=True):
            st.session_state.company = st.text_input("지원 회사명", value=st.session_state.company, placeholder="예: SK 하이닉스")
            st.session_state.job = st.text_input("지원 직무", value=st.session_state.job, placeholder="예: 설비/설계")
            
            st.markdown('<div style="margin-top: 1rem;"></div>', unsafe_allow_html=True)
            
            btn_col1, btn_col2, btn_col3 = st.columns([1, 2, 1])
            with btn_col2:
                if st.button("AI 맞춤 포트폴리오 생성", use_container_width=True):
                    if not st.session_state.company or not st.session_state.job:
                        st.warning("회사명과 직무를 모두 입력해주세요.")
                    else:
                        change_page('analysis')
                        st.rerun()

def show_analysis_page():
    st.markdown("""
    <div class="container" style="text-align: center; padding-top: 3rem; padding-bottom: 3rem;">
        <h2 style="font-size: 2rem; font-weight: bold; margin-bottom: 2rem;">AI가 회원님의 데이터를 분석하고 있습니다.</h2>
    </div>
    """, unsafe_allow_html=True)
    
    messages = [
        f"'{st.session_state.company}'의 최신 기술 동향을 분석 중입니다...",
        "채용 공고의 핵심 요구 역량을 추출하고 있습니다...",
        f"'{st.session_state.job}' 직무와 회원님의 경험 데이터 매칭 중...",
        "프로젝트 설명을 AI가 재구성하는 중...",
        "맞춤 포트폴리오 생성 완료!"
    ]
    
    progress_bar = st.progress(0, text=messages[0])
    for i, message in enumerate(messages):
        progress_value = (i + 1) / len(messages)
        progress_bar.progress(progress_value, text=message)
        time.sleep(1)
    
    change_page('result')
    st.rerun()

def show_result_page():
    # 헤더
    st.markdown(f"""
    <div style="text-align: center; margin-bottom: 3rem;">
        <h1 class="hero-title" style="font-size: 3rem; margin-bottom: 1rem;">
            {st.session_state.company} 맞춤 포트폴리오
        </h1>
        <p class="hero-description" style="font-size: 1.1rem; color: #6b7280; max-width: 100%;">
            FitFolio의 AI가 '{st.session_state.job}' 직무에 맞춰 재구성한 결과입니다.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # AI 분석 요약 카드
    st.markdown(f"""
    <div class="card analysis-card">
        <div class="card-title">
            <span style="font-size: 1.5rem;">💡</span> AI 분석 요약
        </div>
        <div class="card-content">
            <p class="card-description">
                FitFolio AI가 분석한 '{st.session_state.company} {st.session_state.job}' 직무의 핵심은 
                <span class="highlight">'LLM 경량화'</span>와 
                <span class="highlight">'온디바이스 AI'</span> 경험입니다. 
                회원님의 경험을 이 키워드에 맞춰 강조하고 재구성했습니다.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 핵심 역량 카드
    st.markdown("""
    <div class="card">
        <div class="card-title">
             <span style="font-size: 1.5rem;">🎯</span> 핵심 역량 (Skills)
        </div>
    """, unsafe_allow_html=True)
    
    required_skills = ['On-Device AI', 'LLM', 'PyTorch']
    for skill in USER_PROFILE['skills']:
        is_highlighted = skill in required_skills
        st.markdown(f"""
        <div class="skill-item-new {'highlighted-skill' if is_highlighted else ''}">
            {skill}
        </div>
        """, unsafe_allow_html=True)

    # 프로젝트 재구성 카드
    st.markdown("""
    <div class="card" style="margin-top: 2rem;">
         <div class="card-title">
             <span style="font-size: 1.5rem;">🚀</span> 프로젝트 재구성 (Projects)
        </div>
    """, unsafe_allow_html=True)

    for project in USER_PROFILE['projects']:
        st.markdown(f"""
        <div class="experience-item">
            <div class="experience-info">
                <span class="experience-status">✅</span>
                <span class="experience-title">{project['title']}</span>
            </div>
        </div>
        <div class="profile-content" style="border-radius: 0.5rem; margin-bottom: 1rem;">
            <p><b>[기존 설명]</b> {project['description']}</p>
            <p style="margin-top: 0.5rem;"><b>[✨ AI Rewrite]</b> '{st.session_state.company}'가 최근 집중하고 있는 <strong>'온디바이스 AI'</strong> 전략에 맞춰, <strong>TensorFlow Lite 기반 모델 경량화</strong> 경험을 강조했습니다. 이를 통해 제한된 하드웨어 환경에서의 효율적인 AI 모델 배포 및 운영 능력을 어필할 수 있습니다.</p>
        </div>
        """, unsafe_allow_html=True)

    # <<<--- [추가된 부분] 추천 자료 섹션 --- #
    st.markdown("""
    <div class="card" style="margin-top: 2rem;">
        <div class="card-title">
            <span style="font-size: 1.5rem;">💡</span> 추천 자료
        </div>
        <p class="card-description" style="margin-bottom: 1.5rem;">
            AI 연구팀 지원을 위해 추가로 준비하면 좋은 자료들입니다.
        </p>
        
        <div class="experience-item" style="margin-top: 1rem;">
            <div class="experience-info">
                <span class="experience-status">📝</span>
                <span class="experience-title">기술블로그 작성</span>
            </div>
        </div>
        <div class="experience-item" style="border-top: none; border-radius: 0 0 0.5rem 0.5rem; background: #f9fafb; padding-left: 3.5rem;">
            AI 연구 과정과 인사이트를 공유하는 블로그 포스트
        </div>

        <div class="experience-item" style="margin-top: 1rem;">
            <div class="experience-info">
                <span class="experience-status">🌐</span>
                <span class="experience-title">오픈소스 기여</span>
            </div>
        </div>
        <div class="experience-item" style="border-top: none; border-radius: 0 0 0.5rem 0.5rem; background: #f9fafb; padding-left: 3.5rem;">
            PyTorch 등 관련 라이브러리에 기여한 내역
        </div>

        <div class="experience-item" style="margin-top: 1rem;">
            <div class="experience-info">
                <span class="experience-status">📄</span>
                <span class="experience-title">논문 요약 자료</span>
            </div>
        </div>
        <div class="experience-item" style="border-top: none; border-radius: 0 0 0.5rem 0.5rem; background: #f9fafb; padding-left: 3.5rem;">
            최신 AI 논문을 분석하고 요약한 자료
        </div>
    </div>
    """, unsafe_allow_html=True)
    # --- [추가된 부분] 끝 --- #

    # 처음으로 돌아가기 버튼
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        if st.button("처음으로 돌아가기", use_container_width=True):
            change_page('landing')
            st.rerun()

# --- 메인 로직 ---
show_header()

st.markdown('<main class="main"><div class="container">', unsafe_allow_html=True)

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

st.markdown('</div></main>', unsafe_allow_html=True)

show_footer()
