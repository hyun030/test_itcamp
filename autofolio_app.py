import streamlit as st
import time
import pandas as pd

# --- 페이지 설정 ---
st.set_page_config(
    page_title="AutoFolio | AI 맞춤 포트폴리오 생성",
    page_icon="✨",
    layout="centered", # 중앙 정렬 레이아웃
)

# --- 더미 데이터 ---
DUMMY_USER_PROFILE = {
    "skills": ['Python', 'PyTorch', 'TensorFlow', 'LLM', 'Data Analysis', 'React', 'Node.js'],
    "projects": [
        {"title": '소셜 미디어 감성 분석 모델', "description": 'LSTM 기반의 딥러닝 모델을 사용하여 소셜 미디어 텍스트의 긍정/부정을 분류하는 프로젝트를 진행했습니다. 데이터 전처리부터 모델 학습, 평가까지 전 과정을 담당했습니다.'},
        {"title": '개인 기술 블로그 개발', "description": 'Django 프레임워크를 이용해 개인 기술 블로그를 개발했습니다. CRUD 기능과 태그 기반 검색 기능을 구현했습니다.'}
    ]
}

# --- 세션 상태 초기화 ---
if 'page' not in st.session_state:
    st.session_state.page = 'landing'
# 각 페이지에서 사용할 데이터 초기화
for key in ['company', 'job', 'manual_text']:
    if key not in st.session_state:
        st.session_state[key] = ''
if 'connected_platforms' not in st.session_state:
    st.session_state.connected_platforms = set()
if 'uploaded_file' not in st.session_state:
    st.session_state.uploaded_file = None


# --- HTML 프로토타입 CSS 주입 ---
st.markdown("""
<style>
/* --- 폰트 임포트 --- */
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700;900&display=swap');

/* --- 기본 및 레이아웃 스타일 --- */
:root {
    --primary-color: #5A67D8; /* 차분한 보라/파랑 계열 */
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

/* Streamlit 기본 요소 오버라이드 */
body {
    font-family: 'Noto Sans KR', sans-serif;
    background-color: var(--secondary-color);
    color: var(--text-color);
}
h1, h2, h3, h4 {
    font-weight: 900 !important;
    letter-spacing: -0.5px !important;
    color: var(--text-color) !important;
}
.stButton>button {
    border-radius: 8px !important;
    font-weight: 700 !important;
    padding: 0.5rem 1rem !important;
    transition: all 0.2s ease !important;
}
.stButton>button:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 10px rgba(0,0,0,0.1);
}

/* 커스텀 클래스 */
.card {
    background: white;
    border-radius: 12px;
    padding: 2rem;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    margin-bottom: 1.5rem;
    width: 100%;
}
.highlight { color: var(--primary-color); }
.page-description { text-align: center; color: var(--subtext-color); margin-bottom: 2.5rem; }

.connect-card {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: space-between;
    text-align: center;
    border: 1px solid var(--border-color);
    border-radius: 10px;
    padding: 1.5rem;
    height: 100%;
}
.connect-card h3 { font-size: 1.2rem; margin-bottom: 0.2rem; }
.connect-card p { color: var(--subtext-color); font-size: 0.9rem; flex-grow: 1; }
.connect-card img { width: 48px; height: 48px; margin-bottom: 1rem; }

.input-section h4 {
    font-size: 1.2rem;
    font-weight: 700;
    margin-bottom: 0.8rem;
    display: flex;
    align-items: center;
}
.input-section h4 .icon-emoji { margin-right: 0.75rem; font-size: 1.5rem; }
.spinner-container {
    display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 50vh;
}
.spinner {
    width: 60px; height: 60px; border: 6px solid var(--border-color);
    border-top-color: var(--primary-color); border-radius: 50%;
    animation: spin 1s linear infinite; margin-bottom: 2rem;
}
@keyframes spin { to { transform: rotate(360deg); } }
</style>
""", unsafe_allow_html=True)


# --- 페이지 렌더링 함수 ---

def go_to_page(page_name):
    st.session_state.page = page_name
    st.rerun()

def render_landing_page():
    st.markdown("""
        <div style="text-align: center; padding: 4rem 1rem;">
            <h1>당신의 커리어, <span class="highlight">AI가 맞춤 설계</span>합니다.</h1>
            <p style="font-size: 1.2rem; color: var(--subtext-color); max-width: 600px; margin: 0 auto 2rem;">
                AutoFolio는 흩어진 당신의 경험을 모아 지원하는 기업에 맞춰 포트폴리오를 자동으로 재구성해주는 가장 스마트한 방법입니다.
            </p>
        </div>
    """, unsafe_allow_html=True)
    if st.button("내 포트폴리오 만들기", type="primary"):
        go_to_page('dashboard')

def render_dashboard_page():
    st.header("1. 데이터 불러오기")
    st.markdown('<p class="page-description">AI가 분석할 데이터를 연동하거나 직접 입력해주세요.</p>', unsafe_allow_html=True)

    # --- 플랫폼 연동 ---
    platforms = {
        "GitHub": "https://via.placeholder.com/48x48/2D3748/FFFFFF?text=G",
        "LinkedIn": "https://via.placeholder.com/48x48/0A66C2/FFFFFF?text=in",
        "블로그": "https://via.placeholder.com/48x48/000000/FFFFFF?text=M",
        "Behance": "https://via.placeholder.com/48x48/0057FF/FFFFFF?text=Be"
    }
    cols = st.columns(4)
    for i, (name, icon) in enumerate(platforms.items()):
        with cols[i]:
            is_connected = name in st.session_state.connected_platforms
            st.markdown(f"""
                <div class="connect-card">
                    <img src="{icon}" alt="{name} Icon">
                    <h3>{name}</h3>
                    <p>{'프로젝트와 코드를' if name == 'GitHub' else '경력과 학력을' if name == 'LinkedIn' else '작성한 글을' if name == '블로그' else '디자인 작업물을'} 가져옵니다.</p>
                </div>
            """, unsafe_allow_html=True)
            if st.button("연동 완료 ✔" if is_connected else "연동하기", key=f"connect_{name}", use_container_width=True, disabled=is_connected):
                st.session_state.connected_platforms.add(name)
                st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # --- 직접 입력 ---
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<h3 style="text-align:center;">추가 정보 직접 입력</h3>', unsafe_allow_html=True)
        st.markdown('<p class="description" style="text-align:center; margin-bottom: 1.5rem;">플랫폼 연동 외에 추가하고 싶은 정보를 직접 입력하거나 파일을 업로드하세요.</p>', unsafe_allow_html=True)
        
        st.markdown('<div class="input-section"><h4><span class="icon-emoji">📝</span> 나의 경력 및 핵심 역량</h4></div>', unsafe_allow_html=True)
        st.session_state.manual_text = st.text_area("manual_skills", placeholder="- A회사 (2022.03 ~ 현재): 추천 시스템 개발...\n- 주요 기술 스택: Python, PyTorch, AWS...", height=150, label_visibility="collapsed")
        
        st.markdown('<div class="input-section" style="margin-top: 2rem;"><h4><span class="icon-emoji">📂</span> 자기소개서/이력서 파일 업로드</h4></div>', unsafe_allow_html=True)
        st.session_state.uploaded_file = st.file_uploader("resume_upload", type=['pdf', 'docx', 'txt'], label_visibility="collapsed")
        
        st.markdown('</div>', unsafe_allow_html=True)

    # --- 다음 단계 버튼 ---
    is_ready = bool(st.session_state.connected_platforms or st.session_state.manual_text.strip() or st.session_state.uploaded_file)
    if st.button("다음 단계로", type="primary", disabled=not is_ready):
        go_to_page('input')

def render_input_page():
    st.header("2. 포트폴리오 맞춤화")
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        with st.form("input_form"):
            st.text_input("지원 회사명", placeholder="예: 삼성전자", key="company")
            st.text_input("지원 직무", placeholder="예: AI 연구원", key="job")
            if st.form_submit_button("AI 맞춤 포트폴리오 생성", use_container_width=True, type="primary"):
                if not st.session_state.company or not st.session_state.job:
                    st.error("회사명과 직무를 모두 입력해주세요.")
                else:
                    go_to_page('loading')
        st.markdown('</div>', unsafe_allow_html=True)

def render_loading_page():
    st.markdown(f"""
        <div class="spinner-container">
            <div class="spinner"></div>
            <h2 id="loading-text">AI가 포트폴리오를 분석하고 있습니다...</h2>
        </div>
    """, unsafe_allow_html=True)
    
    # 실제 로딩 시뮬레이션
    time.sleep(2) # UI가 먼저 렌더링될 시간을 줌
    go_to_page('result')

def render_result_page():
    company, job = st.session_state.company, st.session_state.job
    st.markdown(f'<header style="text-align:center; margin-bottom:3rem;"><h2><span class="company-name">{company}</span> 맞춤 포트폴리오</h2><p>AI가 <strong>{job}</strong> 직무에 맞춰 재구성한 결과입니다.</p></header>', unsafe_allow_html=True)

    st.markdown('<div class="card portfolio-section">', unsafe_allow_html=True)
    st.subheader("AI Profile Summary")
    st.success(f"'{job}' 직무에 대한 깊은 이해와 **LLM, PyTorch** 역량을 바탕으로, '{company}'가 추구하는 차세대 AI 기술 개발에 기여할 준비가 된 인재입니다. 특히 **대규모 데이터 처리 및 모델 경량화** 경험은 귀사의 경쟁력 강화에 도움이 될 것입니다.")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card portfolio-section">', unsafe_allow_html=True)
    st.subheader("핵심 역량 (Skills)")
    required_skills = ['LLM', 'PyTorch', 'TensorFlow']
    skills_html = "".join([
        f'<span class="skill-tag {"highlighted" if skill in required_skills else ""}">{skill}</span>'
        for skill in DUMMY_USER_PROFILE['skills']
    ])
    st.markdown(f'<div class="skills-grid">{skills_html}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card portfolio-section">', unsafe_allow_html=True)
    st.subheader("주요 프로젝트 (Projects)")
    for i, project in enumerate(DUMMY_USER_PROFILE['projects']):
        ai_rewrite_html = ""
        if i == 0:
            ai_rewrite_html = f"""
                <div class="ai-rewrite">
                    <strong>[AI 재구성 설명]</strong><br>
                    '{company}'의 사용자 중심 AI 경험 전략에 발맞춰, <strong>LSTM 기반 감성 분석 모델</strong>을 개발했습니다. 이 프로젝트는 <strong>대규모 텍스트 데이터 처리</strong> 능력과 <strong>PyTorch를 활용한 딥러닝 모델 최적화</strong> 역량을 보여줍니다.
                </div>
            """
        st.markdown(f"""
            <div class="project-card">
                <h4>{project['title']}</h4>
                <p class="description">{project['description']}</p>
                {ai_rewrite_html}
            </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div style="text-align:center; margin-top:3rem;">', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.download_button("PDF로 다운로드", data="PDF content", file_name="portfolio.pdf", use_container_width=True)
    with col2:
        if st.button("처음으로 돌아가기", use_container_width=True):
            st.session_state.clear()
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)


# --- 메인 로직: 페이지 라우터 ---
page_map = {
    'landing': render_landing_page,
    'dashboard': render_dashboard_page,
    'input': render_input_page,
    'loading': render_loading_page,
    'result': render_result_page
}
page_function = page_map.get(st.session_state.page, render_landing_page)
page_function()

