import streamlit as st
import time
import pandas as pd

# --- 페이지 설정 ---
st.set_page_config(
    page_title="AutoFolio | AI 맞춤 포트폴리오 생성",
    page_icon="✨",
    layout="wide",
)

# --- 더미 데이터 ---
DUMMY_USER_PROFILE = {
    "name": "홍길동",
    "skills": ['Python', 'PyTorch', 'TensorFlow', 'LLM', 'Data Analysis', 'React', 'Node.js', 'Figma', 'SQL'],
    "projects": [
        {"title": '소셜 미디어 감성 분석 모델', "description": 'LSTM 기반의 딥러닝 모델을 사용하여 소셜 미디어 텍스트의 긍정/부정을 분류하는 프로젝트를 진행했습니다.'},
        {"title": '개인 기술 블로그 개발', "description": 'Django 프레임워크를 이용해 개인 기술 블로그를 개발했습니다. CRUD 기능과 태그 기반 검색 기능을 구현했습니다.'},
        {"title": '사내 데이터 분석 대시보드 구축', "description": 'Tableau와 SQL을 활용하여 마케팅 팀의 KPI를 추적하는 인터랙티브 대시보드를 구축하여 데이터 기반 의사결정을 지원했습니다.'}
    ]
}

DUMMY_ANALYSIS_RESULTS = {
    "삼성전자": {"summary": "AI가 분석한 '삼성전자'의 최근 핵심 키워드는 **'초거대 AI', 'LLM 경량화', 'HBM 반도체'** 입니다. 따라서 '{job}' 직무에서는 관련 기술 경험과 반도체 산업에 대한 이해도를 함께 어필하는 것이 중요합니다."},
    "네이버": {"summary": "AI가 분석한 '네이버'의 최근 핵심 키워드는 **'하이퍼클로바X', '생성형 AI', 'B2B 솔루션'** 입니다. '{job}' 직무에서는 서비스 중심의 AI 모델 적용 능력을 강조하는 것이 효과적입니다."},
    "카카오": {"summary": "AI가 분석한 '카카오'의 최근 핵심 키워드는 **'KoGPT', 'AI 에이전트', '카카오톡 연계'** 입니다. '{job}' 직무에서는 플랫폼 생태계에 대한 이해와 창의적인 AI 서비스 기획 역량을 어필하는 것이 좋습니다."}
}

# --- 세션 상태 초기화 ---
if 'page' not in st.session_state:
    st.session_state.page = 'landing'
if 'company' not in st.session_state:
    st.session_state.company = ''
if 'job' not in st.session_state:
    st.session_state.job = ''
if 'connected_platforms' not in st.session_state:
    st.session_state.connected_platforms = set()
# 직접 입력을 위한 세션 상태 추가
if 'manual_text' not in st.session_state:
    st.session_state.manual_text = ""
if 'uploaded_file' not in st.session_state:
    st.session_state.uploaded_file = None

# --- 공통 스타일 ---
st.markdown("""
<style>
    .main .block-container { padding-top: 2rem; padding-bottom: 2rem; }
    .card {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 0.5rem;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
    }
    h5 {
        font-weight: 700;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# --- 함수 정의 ---
def go_to_page(page_name):
    st.session_state.page = page_name
    st.rerun()

def fetch_company_analysis(company, job):
    time.sleep(1.5)
    normalized_company = company.strip().lower().replace(" ", "")
    for key, value in DUMMY_ANALYSIS_RESULTS.items():
        if normalized_company == key.strip().lower().replace(" ", ""):
            return value["summary"].format(job=job)
    return f"AI가 분석한 '{company}'의 최근 핵심 키워드는 **'디지털 전환', '데이터 기반 의사결정', '고객 경험 향상'** 입니다. 따라서 '{job}' 직무에서는 관련 기술 경험과 비즈니스 이해도를 함께 어필하는 것이 중요합니다."

def render_landing_page():
    st.markdown("<h1 style='text-align: center;'>AutoFolio</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #5A67D8;'>AI가 당신의 경험을 기업에 맞춰 재구성합니다</h3>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("<p style='text-align: center; font-size: 1.1em;'>흩어진 당신의 경험(GitHub, 블로그 등)을 자동으로 취합하고, 지원하는 기업의 최신 동향에 맞춰 포트폴리오를 AI가 재구성해주는 가장 스마트한 방법입니다.</p>", unsafe_allow_html=True)
    st.write("")
    col1, col2, col3 = st.columns([1,1,1])
    with col2:
        if st.button("내 포트폴리오 만들기 →", use_container_width=True, type="primary"):
            go_to_page('dashboard')

def render_dashboard_page():
    """[2단계] 데이터 불러오기 (연동 + 직접 입력)"""
    st.header("1. 데이터 불러오기")
    st.info("AI가 분석할 데이터를 연동하거나 직접 입력해주세요. (1개 이상)")

    st.subheader("🔗 플랫폼 데이터 연동")
    platforms = {"GitHub": "💻", "LinkedIn": "📄", "블로그": "✍️", "Behance": "🎨"}
    cols = st.columns(4)
    for i, (platform, icon) in enumerate(platforms.items()):
        with cols[i]:
            with st.container():
                is_connected = platform in st.session_state.connected_platforms
                button_text = f"{icon} {platform} 연동 완료" if is_connected else f"{icon} {platform} 연동하기"
                if st.button(button_text, key=f"connect_{platform}", use_container_width=True, disabled=is_connected):
                    st.session_state.connected_platforms.add(platform)
                    st.toast(f"{platform} 연동이 완료되었습니다!", icon="🎉")
                    st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)

    st.subheader("📝 추가 정보 직접 입력")
    with st.container():
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        # 경력/역량 입력
        st.markdown("<h5>📝 나의 경력 및 핵심 역량</h5>", unsafe_allow_html=True)
        manual_text = st.text_area(
            "manual_text_input",
            placeholder="- A회사 (2022.03 ~ 현재): 추천 시스템 개발 및 성능 개선 담당...\n- 주요 기술 스택: Python, PyTorch, AWS S3...",
            height=150,
            label_visibility="collapsed"
        )
        st.session_state.manual_text = manual_text

        st.markdown("<br>", unsafe_allow_html=True)
        
        # 파일 업로드
        st.markdown("<h5>📂 자기소개서/이력서 파일 업로드</h5>", unsafe_allow_html=True)
        uploaded_file = st.file_uploader(
            "resume_uploader",
            type=['pdf', 'docx', 'txt'],
            label_visibility="collapsed"
        )
        st.session_state.uploaded_file = uploaded_file
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # 다음 단계 버튼 활성화 로직
    is_ready = (
        len(st.session_state.connected_platforms) > 0 or
        (st.session_state.manual_text and st.session_state.manual_text.strip() != "") or
        st.session_state.uploaded_file is not None
    )

    if st.button("다음 단계로 →", use_container_width=True, type="primary", disabled=not is_ready):
        go_to_page('input')


def render_input_page():
    st.header("2. 포트폴리오 맞춤화")
    st.info("AI가 분석할 지원 회사와 직무를 정확하게 입력해주세요.")
    with st.form("input_form"):
        company = st.text_input("**지원 회사명**", placeholder="예: 삼성전자, 네이버, 카카오")
        job = st.text_input("**지원 직무**", placeholder="예: AI 연구원")
        submitted = st.form_submit_button("✨ AI 맞춤 포트폴리오 생성하기", use_container_width=True, type="primary")
        if submitted:
            if not company or not job: st.error("회사명과 직무를 모두 입력해주세요.")
            else:
                st.session_state.company, st.session_state.job = company, job
                go_to_page('loading')

def render_loading_page():
    st.header("AI가 포트폴리오를 재구성하고 있습니다...")
    messages = [
        f"**1/4 단계:** '{st.session_state.company}'의 최신 뉴스 및 채용 공고를 분석 중입니다... (Perplexity API)",
        "**2/4 단계:** 직무의 핵심 요구 역량을 추출하고 있습니다... (GPT-4)",
        "**3/4 단계:** 내 경험 데이터와 기업의 요구 역량을 매칭하고 있습니다...",
        "**4/4 단계:** AI가 맞춤 포트폴리오 초안을 생성하는 중입니다... (Gemini)",
    ]
    progress_bar = st.progress(0, text="분석 시작...")
    for i, message in enumerate(messages):
        progress_bar.progress((i + 1) * 25, text=message)
        time.sleep(1.5)
    go_to_page('result')

def render_result_page():
    company, job = st.session_state.company, st.session_state.job
    st.markdown(f"## ✨ **{company}** 맞춤 포트폴리오")
    st.markdown(f"AI가 **'{job}'** 직무에 맞춰 재구성한 결과입니다.")
    st.markdown("---")

    tab1, tab2, tab3 = st.tabs(["**📊 AI 분석 요약**", "**💪 핵심 역량**", "**🚀 프로젝트 추천**"])

    with tab1:
        st.subheader("🤖 AI 기업 분석 및 전략 제안")
        analysis_result = fetch_company_analysis(company, job)
        st.info(analysis_result)
        st.subheader("✍️ AI 자기소개서 초안 (Profile Summary)")
        st.success("'{job}' 직무에 대한 깊은 이해와 **LLM, PyTorch** 역량을 바탕으로...".format(job=job, company=company))

    with tab2:
        st.subheader("🎯 핵심 역량 분석 (Skill Match)")
        required_skills = ['LLM', 'PyTorch', 'TensorFlow', 'SQL']
        match_count = len(set(DUMMY_USER_PROFILE['skills']) & set(required_skills))
        col1, col2 = st.columns(2)
        col1.metric("나의 보유 역량", f"{len(DUMMY_USER_PROFILE['skills'])} 개")
        col2.metric(f"'{job}' 핵심 요구 역량", f"{len(required_skills)} 개", f"{match_count} 개 일치")
        df = pd.DataFrame({"skill": DUMMY_USER_PROFILE['skills'], "match": [1 if s in required_skills else 0.5 for s in DUMMY_USER_PROFILE['skills']]})
        st.bar_chart(df.set_index('skill')['match'])

    with tab3:
        st.subheader("💡 AI 추천 프로젝트 및 설명 재구성")
        st.warning("AI가 직무 연관성이 가장 높다고 판단한 프로젝트를 **상단에 재배치**했습니다.")
        for i, project in enumerate(DUMMY_USER_PROFILE['projects']):
            with st.expander(f"**{ '🏆' if i==0 else '📄'} {project['title']} {'(AI 추천)' if i==0 else ''}**", expanded=(i==0)):
                st.markdown(f"**기존 설명:** {project['description']}")
                if i == 0:
                    st.markdown("---")
                    rewritten_desc = f"'{company}'의 사용자 중심 AI 경험 전략에 발맞춰, **LSTM 기반 감성 분석 모델**을 개발했습니다..."
                    st.success(f"**AI 재구성 설명 (GPT-4):** {rewritten_desc}")

    st.markdown("---")
    col1, col2 = st.columns([1, 4])
    if col1.button("🏠 처음으로", use_container_width=True):
        st.session_state.clear(); st.rerun()
    col2.download_button("📄 포트폴리오 다운로드", data=f"# {company} 맞춤 포트폴리오...", file_name=f"{company}_{job}_portfolio.txt", use_container_width=True)

# --- 메인 로직: 페이지 라우터 ---
if 'page' in st.session_state:
    page_map = {
        'landing': render_landing_page,
        'dashboard': render_dashboard_page,
        'input': render_input_page,
        'loading': render_loading_page,
        'result': render_result_page
    }
    page_map.get(st.session_state.page, render_landing_page)()
else:
    render_landing_page()

