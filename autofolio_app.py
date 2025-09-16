import streamlit as st

# --- 페이지 설정 ---
st.set_page_config(
    page_title="삼성전자 맞춤 포트폴리오",
    page_icon="🔷",
    layout="wide"
)

# --- CSS 파일 로드 ---
def local_css(file_name):
    # 'styles.css' 파일이 app.py와 같은 경로에 있는지 확인하세요.
    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        st.error(f"'{file_name}' 파일을 찾을 수 없습니다. app.py와 동일한 폴더에 있는지 확인해주세요.")


local_css("styles.css")

# --- 세션 상태 초기화 (자기소개서 편집 기능용) ---
if 'editing_profile' not in st.session_state:
    st.session_state.editing_profile = False
if 'profile_summary' not in st.session_state:
    st.session_state.profile_summary = "'AI 연구팀' 직무에 대한 깊은 이해와 LLM, PyTorch 역량을 바탕으로..."

# --- 헤더 ---
# st.columns와 st.markdown을 사용하여 원본과 유사하게 구성
col1, col2 = st.columns([2, 3])
with col1:
    st.markdown("""
    <div class="header-left">
        <div class="logo-section">
            <div class="logo"><span>S</span></div>
            <span class="company-name">삼성전자</span>
        </div>
        <span class="badge badge-secondary">AI 채용 플랫폼</span>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="custom-nav">
        <a href="#" class="nav-link">포트폴리오</a>
        <a href="#" class="nav-link">채용정보</a>
        <a href="#" class="nav-link">지원하기</a>
        <button class="btn btn-outline" style="margin-left: 1rem;">로그인</button>
    </div>
    <style>
    .custom-nav { display: flex; justify-content: flex-end; align-items: center; height: 4rem; }
    .custom-nav .nav-link { margin: 0 0.75rem; color: #6b7280; text-decoration: none; }
    .custom-nav .nav-link:hover { color: #1f2937; }
    /* 모바일 화면 대응 */
    @media (max-width: 768px) {
        .custom-nav { display: none; }
    }
    </style>
    """, unsafe_allow_html=True)


# --- Hero 섹션 ---
st.markdown("""
<section class="hero" style="padding: 2rem 0;">
    <div class="hero-background">
        <img src="https://images.unsplash.com/photo-1623715537851-8bc15aa8c145?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxtb2Rlcm4lMjB0ZWNobm9sb2d5JTIwb2ZmaWNlJTIwd29ya3NwYWNlfGVufDF8fHx8MTc1NzkxNDMxMXww&ixlib=rb-4.0&q=80&w=1080&utm_source=figma&utm_medium=referral" alt="Modern workspace">
    </div>
    <div class="container">
        <div class="hero-content">
            <div class="hero-badge-section">
                <svg class="sparkles-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="m9 12 2 2 4-4"/><path d="M21 12c.552 0 1.447-.167 2-1 0-.552-.167-1.447-1-2-.552 0-1.447.167-2 1 0 .552.167 1.447 1 2z"/><path d="M9 12c.552 0 1.447-.167 2-1 0-.552-.167-1.447-1-2-.552 0-1.447.167-2 1 0 .552.167 1.447 1 2z"/></svg>
                <span class="badge badge-ai">AI 기반 맞춤형 분석</span>
            </div>
            <h1 class="hero-title">삼성전자 맞춤 포트폴리오</h1>
            <p class="hero-description">
                시각 <span class="highlight">'AI 연구팀'</span> 직무에 맞춘 제7성할 질문입니다.<br>
                AI가 분석한 맞춤형 포트폴리오로 성공적인 지원을 준비하세요.
            </p>
        </div>
    </div>
</section>
""", unsafe_allow_html=True)


# --- 탭 네비게이션 (Streamlit 기능으로 대체) ---
tab1, tab2, tab3 = st.tabs([
    "📊 AI 분석 학습",
    "🎯 핵심 역량",
    "📁 포트폴리오 준비"
])

# --- 탭 1: AI 분석 학습 ---
with tab1:
    col1, col2 = st.columns(2)

    # 분석 카드 (왼쪽)
    with col1:
        st.markdown("""
        <div class="card analysis-card">
            <div class="card-header">
                <div class="card-header-top">
                    <svg class="brain-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M9.5 2A2.5 2.5 0 0 1 12 4.5v15a2.5 2.5 0 0 1-4.96.44 2.5 2.5 0 0 1-2.96-3.08 3 3 0 0 1-.34-5.58 2.5 2.5 0 0 1 1.32-4.24 2.5 2.5 0 0 1 1.98-3A2.5 2.5 0 0 1 9.5 2Z"/></svg>
                    <span class="badge badge-completed">AI 분석 완료</span>
                </div>
                <h2 class="card-title">AI 기반 분석 및 전략 제안</h2>
                <p class="card-description">
                    AI가 분석한 '삼성전자'의 최고 역량 기준에 '초기 AI', 'LLM 전문성', 'HBM 반도체'입니다.
                    따라서 'AI 연구팀' 직무에서는 관련 기술 경험과 반도체 산업에 대한 이해도를 함께 어필하는 것이 중요합니다.
                </p>
            </div>
            <div class="card-content">
                <div class="skills-grid">
                    <div class="skill-item"><h4>LLM 전문성</h4><p>대규모 언어모델 연구 경험</p></div>
                    <div class="skill-item"><h4>HBM 반도체</h4><p>고대역폭 메모리 기술 이해</p></div>
                    <div class="skill-item"><h4>초기 AI</h4><p>AI 기술 연구개발 역량</p></div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("상세 분석 보기", use_container_width=True, type="primary"):
            st.toast("상세 분석 페이지로 이동합니다.")

    # 프로필 요약 카드 (오른쪽)
    with col2:
        with st.container(border=False):
             st.markdown("""
             <div class="card profile-card" style="margin-bottom: 0;">
                <div class="card-header">
                    <div class="card-header-actions">
                        <div class="card-header-top">
                            <span class="badge badge-auto">자동 생성됨</span>
                        </div>
                    </div>
                    <h2 class="card-title">AI 자기소개서 초안</h2>
                    <p class="card-description">AI가 생성한 맞춤형 자기소개서 초안입니다. 필요에 따라 수정하여 사용하세요.</p>
                </div>
             """, unsafe_allow_html=True)

             # 편집 로직
             if st.session_state.editing_profile:
                 edited_text = st.text_area(
                     "자기소개서 수정:",
                     value=st.session_state.profile_summary,
                     height=150,
                     label_visibility="collapsed"
                 )

                 save_col, cancel_col = st.columns(2)
                 if save_col.button("저장", use_container_width=True, type="primary"):
                     st.session_state.profile_summary = edited_text
                     st.session_state.editing_profile = False
                     st.rerun()
                 if cancel_col.button("취소", use_container_width=True):
                     st.session_state.editing_profile = False
                     st.rerun()

             else:
                 st.markdown(f"""
                 <div class="profile-content"><p>{st.session_state.profile_summary}</p></div>
                 """, unsafe_allow_html=True)

                 edit_col, download_col = st.columns(2)
                 if edit_col.button("✏️ 편집", use_container_width=True):
                     st.session_state.editing_profile = True
                     st.rerun()

                 download_col.download_button(
                     label="📄 다운로드",
                     data=st.session_state.profile_summary,
                     file_name="profile_summary.txt",
                     mime="text/plain",
                     use_container_width=True
                 )

             st.markdown("""
                <div class="tags" style="margin-top: 1rem;">
                    <span class="tag">AI 연구</span><span class="tag">LLM</span>
                    <span class="tag">PyTorch</span><span class="tag">반도체</span>
                </div>
            </div>
             """, unsafe_allow_html=True)

# --- 탭 2: 핵심 역량 ---
with tab2:
    st.markdown("""
    <div class="card">
        <div class="card-header">
            <h2 class="card-title">⭐ 핵심 역량 분석</h2>
            <p class="card-description">AI 연구팀 직무에 필요한 핵심 기술과 현재 수준을 평가했습니다.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    skills = {
        "Python/PyTorch": 90, "Large Language Models": 85, "반도체 기술 이해": 70,
        "머신러닝 알고리즘": 80, "데이터 분석": 75, "논문 작성": 65
    }

    for skill, level in skills.items():
        st.write(f"**{skill}**")
        st.progress(level, text=f"{level}%")

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
        <div class="card-header">
            <h2 class="card-title">관련 경험 및 프로젝트</h2>
            <p class="card-description">직무와 연관된 경험들의 완성도와 관련성을 확인하세요.</p>
        </div>
        <div class="card-content">
            <div class="experience-list">
                <div class="experience-item">
                    <div class="experience-info"><span class="experience-status">✅</span><span class="experience-title">AI 모델 최적화 프로젝트</span></div>
                    <div class="experience-badges"><span class="badge badge-success">관련성 높음</span><span class="badge badge-secondary">완료</span></div>
                </div>
                <div class="experience-item">
                    <div class="experience-info"><span class="experience-status">✅</span><span class="experience-title">LLM 파인튜닝 경험</span></div>
                    <div class="experience-badges"><span class="badge badge-success">관련성 높음</span><span class="badge badge-secondary">완료</span></div>
                </div>
                <div class="experience-item">
                    <div class="experience-info"><span class="experience-status">🔄</span><span class="experience-title">반도체 관련 연구</span></div>
                    <div class="experience-badges"><span class="badge badge-warning">관련성 보통</span><span class="badge badge-secondary">진행중</span></div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# --- 탭 3: 포트폴리오 준비 ---
with tab3:
    st.markdown("""
    <div class="card">
        <div class="card-header">
            <h2 class="card-title">📁 포트폴리오 현황</h2>
            <p class="card-description">현재 포트폴리오 자료의 완성도를 확인하고 부족한 부분을 보완하세요.</p>
        </div>
        <div class="card-content">
            <div class="portfolio-list">
                 <div class="portfolio-item">
                    <div class="portfolio-info"><span class="portfolio-icon">📄</span><div class="portfolio-details"><h4>AI 모델 성능 최적화 보고서</h4><p>PyTorch를 활용한 LLM 최적화 프로젝트 결과</p></div></div>
                    <div class="portfolio-actions"><span class="badge badge-success">완료</span></div>
                </div>
                <div class="portfolio-item">
                    <div class="portfolio-info"><span class="portfolio-icon">💻</span><div class="portfolio-details"><h4>GitHub 리포지토리</h4><p>오픈소스 기여 및 개인 프로젝트</p></div></div>
                    <div class="portfolio-actions"><span class="badge badge-warning">업데이트 필요</span></div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Streamlit 파일 업로더로 기능 대체
    with st.container(border=False):
        st.markdown("""
        <div class="card upload-card">
            <div class="card-header">
                <h2 class="card-title">📤 자료 업로드</h2>
                <p class="card-description">기존 자료를 업로드하여 AI 분석을 받아보세요.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        uploaded_files = st.file_uploader(
            "파일을 드래그하거나 클릭하여 업로드 (PDF, DOCX, PPTX, PNG, JPG)",
            type=['pdf', 'docx', 'pptx', 'png', 'jpg', 'jpeg'],
            accept_multiple_files=True,
            label_visibility="collapsed"
        )
        if uploaded_files:
            st.success(f"{len(uploaded_files)}개의 파일이 성공적으로 업로드되었습니다!")
            for file in uploaded_files:
                st.write(f"- {file.name} ({round(file.size / 1024, 2)} KB)")

# --- 푸터 ---
st.markdown("""
<footer class="footer">
    <div class="container">
        <div class="footer-content">
            <p>&copy; 2024 삼성전자. AI 기반 채용 플랫폼</p>
        </div>
    </div>
</footer>
""", unsafe_allow_html=True)
