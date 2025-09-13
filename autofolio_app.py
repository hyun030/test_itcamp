import streamlit as st
import time
import pandas as pd

# --- 페이지 설정 ---
st.set_page_config(
    page_title="AutoFolio | AI 맞춤 포트폴리오 생성",
    page_icon="✨",
    layout="centered",
)

# --- 더미 데이터 ---
# 1. 사용자 프로필 데이터 (실제로는 DB나 연동 플랫폼에서 가져옴)
DUMMY_USER_PROFILE = {
    "name": "홍길동",
    "skills": ['Python', 'PyTorch', 'TensorFlow', 'LLM', 'Data Analysis', 'React', 'Node.js', 'Figma', 'SQL'],
    "projects": [
        {
            "title": '소셜 미디어 감성 분석 모델',
            "description": 'LSTM 기반의 딥러닝 모델을 사용하여 소셜 미디어 텍스트의 긍정/부정을 분류하는 프로젝트를 진행했습니다. 데이터 전처리부터 모델 학습, 평가까지 전 과정을 담당했습니다.',
        },
        {
            "title": '개인 기술 블로그 개발',
            "description": 'Django 프레임워크를 이용해 개인 기술 블로그를 개발했습니다. CRUD 기능과 태그 기반 검색 기능을 구현했습니다.',
        },
        {
            "title": '사내 데이터 분석 대시보드 구축',
            "description": 'Tableau와 SQL을 활용하여 마케팅 팀의 KPI를 추적하는 인터랙티브 대시보드를 구축하여 데이터 기반 의사결정을 지원했습니다.',
        }
    ]
}

# 2. Perplexity API 호출 결과 시뮬레이션 데이터
DUMMY_ANALYSIS_RESULTS = {
    "삼성전자": {
        "summary": "AI가 분석한 '삼성전자'의 최근 핵심 키워드는 **'초거대 AI', 'LLM 경량화', 'HBM 반도체'** 입니다. 특히 AI 반도체 부문에서의 리더십 확보를 위해 공격적인 R&D 투자를 진행하고 있습니다. 따라서 '{job}' 직무에서는 관련 기술 경험과 반도체 산업에 대한 이해도를 함께 어필하는 것이 중요합니다."
    },
    "네이버": {
        "summary": "AI가 분석한 '네이버'의 최근 핵심 키워드는 **'하이퍼클로바X', '생성형 AI', 'B2B 솔루션'** 입니다. 자체 개발한 초거대 AI 모델을 기반으로 다양한 서비스에 생성형 AI를 접목하고 있으며, 클라우드 플랫폼을 통한 B2B 사업 확장에 주력하고 있습니다. '{job}' 직무에서는 서비스 중심의 AI 모델 적용 능력을 강조하는 것이 효과적입니다."
    },
    "카카오": {
        "summary": "AI가 분석한 '카카오'의 최근 핵심 키워드는 **'KoGPT', 'AI 에이전트', '카카오톡 연계'** 입니다. 국민 메신저 카카오톡을 기반으로 한 AI 서비스 통합에 집중하고 있으며, 사용자 친화적인 AI 경험 제공을 목표로 합니다. '{job}' 직무에서는 플랫폼 생태계에 대한 이해와 창의적인 AI 서비스 기획 역량을 어필하는 것이 좋습니다."
    }
}


# --- 세션 상태 초기화 ---
if 'page' not in st.session_state:
    st.session_state.page = 'main'
if 'company' not in st.session_state:
    st.session_state.company = ''
if 'job' not in st.session_state:
    st.session_state.job = ''

# --- 함수 정의 ---

def fetch_company_analysis(company, job):
    """Perplexity API 호출을 시뮬레이션하는 함수"""
    st.toast(f"'{company}' 정보 분석을 시작합니다...")
    time.sleep(1.5) # 실제 API 호출 시간처럼 보이게 딜레이
    
    # 사용자가 입력한 회사 이름과 시뮬레이션 데이터의 키를 비교
    # (띄어쓰기, 대소문자 등 차이를 무시하기 위해 정규화)
    normalized_company = company.strip().lower().replace(" ", "")
    
    for key, value in DUMMY_ANALYSIS_RESULTS.items():
        normalized_key = key.strip().lower().replace(" ", "")
        if normalized_company == normalized_key:
            # {job} 부분을 실제 직무명으로 교체하여 반환
            return value["summary"].format(job=job)
    
    # 시뮬레이션 데이터에 없는 회사일 경우, 일반적인 응답 반환
    return f"AI가 분석한 '{company}'의 최근 핵심 키워드는 **'디지털 전환', '데이터 기반 의사결정', '고객 경험 향상'** 입니다. 따라서 '{job}' 직무에서는 관련 기술 경험과 비즈니스 이해도를 함께 어필하는 것이 중요합니다."


def render_main_page():
    """메인 페이지 UI를 렌더링하는 함수"""
    st.markdown("<h1 style='text-align: center;'>AutoFolio</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #5A67D8;'>AI가 당신의 경험을 기업에 맞춰 재구성합니다</h3>", unsafe_allow_html=True)
    
    st.write("")
    st.write("")

    with st.form("input_form"):
        company = st.text_input("**지원 회사명**", placeholder="예: 삼성전자, 네이버, 카카오")
        job = st.text_input("**지원 직무**", placeholder="예: AI 연구원")
        
        submitted = st.form_submit_button("✨ AI 맞춤 포트폴리오 생성하기")

        if submitted:
            if not company or not job:
                st.error("회사명과 직무를 모두 입력해주세요.")
            else:
                st.session_state.company = company
                st.session_state.job = job
                st.session_state.page = 'loading'
                st.rerun()

def render_loading_page():
    """로딩 페이지 UI를 렌더링하고 결과 페이지로 전환하는 함수"""
    company = st.session_state.company
    
    st.markdown("---")
    messages = [
        f"**1/4 단계:** '{company}'의 최신 뉴스 및 채용 공고를 분석 중입니다... (Perplexity API)",
        f"**2/4 단계:** 직무의 핵심 요구 역량을 추출하고 있습니다... (GPT-4)",
        f"**3/4 단계:** 내 경험 데이터와 기업의 요구 역량을 매칭하고 있습니다...",
        f"**4/4 단계:** AI가 맞춤 포트폴리오 초안을 생성하는 중입니다... (Gemini)",
        "**분석 완료!** 결과를 생성합니다."
    ]

    progress_bar = st.progress(0)
    status_text = st.empty()

    for i, message in enumerate(messages):
        progress_bar.progress((i + 1) * (100 // len(messages)))
        status_text.info(message)
        time.sleep(1.5)

    st.session_state.page = 'result'
    st.rerun()

def render_result_page():
    """결과 페이지 UI를 렌더링하는 함수"""
    company = st.session_state.company
    job = st.session_state.job
    
    st.markdown(f"## ✨ **{company}** 맞춤 포트폴리오")
    st.markdown(f"AI가 **'{job}'** 직무에 맞춰 재구성한 결과입니다.")
    st.markdown("---")

    # 1. AI 기업 분석 요약 (Perplexity API 시뮬레이션)
    st.subheader("1. AI 기업 분석 및 전략 제안")
    with st.spinner("Perplexity API로 최신 기업 동향을 분석 중..."):
        analysis_result = fetch_company_analysis(company, job)
    st.info(analysis_result)
    st.write("")
    
    # 2. 맞춤 자기소개 요약
    st.subheader("2. AI 자기소개서 초안 (Profile Summary)")
    st.success(f"""
    '{job}' 직무에 대한 깊은 이해와 **LLM, PyTorch** 역량을 바탕으로, '{company}'가 추구하는 차세대 AI 기술 개발에 기여할 준비가 된 인재입니다. 
    특히 **대규모 데이터 처리 및 모델 경량화** 경험은 귀사의 경쟁력 강화에 실질적인 도움이 될 것입니다.
    """)
    st.write("")

    # 3. 역량 분석 (Skill Match)
    st.subheader("3. 핵심 역량 분석 (Skill Match)")
    required_skills = ['LLM', 'PyTorch', 'TensorFlow', 'SQL']
    match_count = len(set(DUMMY_USER_PROFILE['skills']) & set(required_skills))
    
    col1, col2 = st.columns(2)
    col1.metric(label="나의 보유 역량", value=f"{len(DUMMY_USER_PROFILE['skills'])} 개")
    col2.metric(label=f"'{job}' 핵심 요구 역량", value=f"{len(required_skills)} 개", delta=f"{match_count} 개 일치")

    skill_data = {"skill": [], "match": []}
    for skill in DUMMY_USER_PROFILE['skills']:
        skill_data["skill"].append(skill)
        skill_data["match"].append(1 if skill in required_skills else 0.5)
        
    df = pd.DataFrame(skill_data)
    st.write("**역량 일치도 시각화 (Gemini)**")
    st.bar_chart(df.set_index('skill')['match'])
    st.caption("AI가 분석한 핵심 요구 역량과 일치하는 스킬이 더 높게 표시됩니다.")
    st.write("")

    # 4. 프로젝트 재배치 및 설명 수정
    st.subheader("4. AI 추천 프로젝트 및 설명 재구성")
    st.warning("AI가 직무 연관성이 가장 높다고 판단한 프로젝트를 **상단에 재배치**했습니다.")
    
    first_project = DUMMY_USER_PROFILE['projects'][0]
    with st.expander(f"**🏆 {first_project['title']} (AI 추천)**", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**기존 설명**")
            st.markdown(f"<div style='background-color:#f0f2f6; padding:10px; border-radius:5px;'>{first_project['description']}</div>", unsafe_allow_html=True)
        with col2:
            st.markdown("**AI 재구성 설명 (GPT-4)**")
            rewritten_desc = f"'{company}'의 사용자 중심 AI 경험 전략에 발맞춰, **LSTM 기반 감성 분석 모델**을 개발했습니다. 이 프로젝트는 **대규모 텍스트 데이터 처리** 능력과 **PyTorch를 활용한 딥러닝 모델 최적화** 역량을 보여줍니다."
            st.markdown(f"<div style='background-color:#d4edda; padding:10px; border-radius:5px;'>{rewritten_desc}</div>", unsafe_allow_html=True)
            
    for project in DUMMY_USER_PROFILE['projects'][1:]:
        with st.expander(f"**📄 {project['title']}**"):
            st.write(project['description'])
            
    st.markdown("---")
    
    # 5. 다운로드 및 재시작
    st.subheader("포트폴리오 활용하기")
    report_text = f"# {company} 맞춤 포트폴리오 ({job})\n\n(생성된 내용 요약...)"
    st.download_button(
        label="📄 포트폴리오 텍스트로 다운로드",
        data=report_text,
        file_name=f"{company}_{job}_portfolio.txt",
    )

    if st.button("🏠 처음으로 돌아가기"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

# --- 메인 로직 ---
if st.session_state.page == 'main':
    render_main_page()
elif st.session_state.page == 'loading':
    render_loading_page()
elif st.session_state.page == 'result':
    render_result_page()

