import streamlit as st
import time
import requests
import json

# --- 뉴스 분석 함수 추가 (기존 코드에 추가만) ---
def fetch_news_analysis(company, role):
    """Perplexity API를 통한 실제 뉴스 분석"""
    url = "https://api.perplexity.ai/chat/completions"
    payload = {
        "model": "sonar",
        "messages": [
            {
                "role": "system",
                "content": "기업의 이름과 직무를 입력할거야. 너는 그 기업에 관련된 최신 동향을 알려줘. 그리고 그 동향을 토대로 해당 직무에 필요한 역량을 핵심 키워드로 정리해줘. 답변은 한국어로, 3~5줄 이내로 작성해줘. 링크 주석, 글자 강조 표시 등은 모두 제거하고 줄글로만 작성해줘."
            },
            {
                "role": "user",
                "content": f"기업: {company}, 직무: {role}"
            }
        ]
    }
    headers = {
        "Authorization": "Bearer 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",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        result = response.json()
        
        if 'choices' in result and len(result['choices']) > 0:
            content = result['choices'][0]['message']['content']
            return parse_analysis(content, company, role)
        else:
            return None
    except:
        return None

def parse_analysis(content, company, role):
    """응답 내용을 기존 데이터 구조에 맞게 파싱"""
    sentences = content.split('.')
    
    # 기본 구조는 기존과 동일하게 유지
    return {
        'company_trends': [s.strip() for s in sentences[:3] if len(s.strip()) > 10],
        'key_skills': ['Python/PyTorch', 'Machine Learning', '대규모 데이터 처리'],  # 기본값 유지
        'company_values': ['혁신', '협업', '고객 중심'],  # 기본값 유지
        'recent_projects': ['AI 모델 최적화', 'MLOps 구축', '개인화 추천 시스템'],  # 기본값 유지
        'raw_content': content
    }

# --- 페이지 설정 ---
st.set_page_config(
    page_title="FitFolio - AI 기반 맞춤형 포트폴리오",
    page_icon="🎯",
    layout="wide"
)

# --- CSS 스타일 ---
st.markdown("""
<style>
/* 전체 레이아웃 */
.main-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 1rem;
}

/* 헤더 스타일 */
.header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem 0;
    border-bottom: 1px solid #e5e7eb;
    margin-bottom: 2rem;
}

.logo-section {
    display: flex;
    align-items: center;
    gap: 0.75rem;
}

.logo {
    width: 3rem;
    height: 3rem;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 0.75rem;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-weight: bold;
    font-size: 1.25rem;
}

.brand-name {
    font-size: 1.5rem;
    font-weight: bold;
    color: #1f2937;
}

.nav-links {
    display: flex;
    gap: 2rem;
    align-items: center;
}

.nav-link {
    color: #6b7280;
    text-decoration: none;
    font-weight: 500;
    transition: color 0.3s;
}

.nav-link:hover {
    color: #667eea;
}

/* Hero 섹션 */
.hero {
    text-align: center;
    padding: 3rem 0;
    background: linear-gradient(135deg, #667eea10 0%, #764ba210 100%);
    border-radius: 1rem;
    margin-bottom: 3rem;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}

.hero-title {
    font-size: 2.5rem;
    font-weight: bold;
    color: #1f2937;
    margin-bottom: 1rem;
    width: 100%;
}

.hero-subtitle {
    font-size: 1.25rem;
    color: #6b7280;
    margin-bottom: 2rem;
    max-width: 700px;
    margin-left: auto;
    margin-right: auto;
    width: 100%;
}

.highlight {
    color: #667eea;
    font-weight: 600;
}

/* 입력 섹션 */
.input-section {
    background: white;
    padding: 2rem;
    border-radius: 1rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    margin-bottom: 2rem;
}

/* 카드 스타일 */
.analysis-card, .profile-card, .skills-card {
    background: white;
    border-radius: 1rem;
    padding: 1.5rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    margin-bottom: 1rem;
}

.card-header {
    margin-bottom: 1rem;
}

.card-title {
    font-size: 1.25rem;
    font-weight: bold;
    color: #1f2937;
    margin-bottom: 0.5rem;
}

.card-description {
    color: #6b7280;
    line-height: 1.6;
}

/* 뱃지 */
.badge {
    display: inline-block;
    padding: 0.25rem 0.75rem;
    border-radius: 9999px;
    font-size: 0.875rem;
    font-weight: 500;
    margin: 0.25rem;
}

.badge-primary { background: #ddd6fe; color: #5b21b6; }
.badge-success { background: #dcfce7; color: #166534; }
.badge-warning { background: #fef3c7; color: #92400e; }
.badge-secondary { background: #f3f4f6; color: #6b7280; }

/* 스킬 그리드 */
.skills-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1rem;
    margin-top: 1rem;
}

.skill-item {
    padding: 1rem;
    background: #f9fafb;
    border-radius: 0.5rem;
    border-left: 3px solid #667eea;
}

.skill-item h4 {
    margin: 0 0 0.5rem 0;
    color: #1f2937;
    font-size: 0.95rem;
}

.skill-item p {
    margin: 0;
    color: #6b7280;
    font-size: 0.85rem;
}

/* 로딩 애니메이션 */
.loading-animation {
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 2rem;
    color: #667eea;
}

.spinner {
    border: 2px solid #f3f3f3;
    border-top: 2px solid #667eea;
    border-radius: 50%;
    width: 20px;
    height: 20px;
    animation: spin 1s linear infinite;
    margin-right: 0.5rem;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

/* 반응형 */
@media (max-width: 768px) {
    .hero-title { font-size: 2rem; }
    .hero-subtitle { font-size: 1rem; }
    .nav-links { display: none; }
}
</style>
""", unsafe_allow_html=True)

# --- 세션 상태 초기화 ---
if 'analysis_completed' not in st.session_state:
    st.session_state.analysis_completed = False
if 'target_company' not in st.session_state:
    st.session_state.target_company = ""
if 'target_position' not in st.session_state:
    st.session_state.target_position = ""
if 'analysis_data' not in st.session_state:
    st.session_state.analysis_data = {}
if 'editing_profile' not in st.session_state:
    st.session_state.editing_profile = False
if 'profile_summary' not in st.session_state:
    st.session_state.profile_summary = ""

# --- 헤더 ---
st.markdown("""
<div class="header">
    <div class="logo-section">
        <div class="logo">F</div>
        <div class="brand-name">FitFolio</div>
    </div>
    <div class="nav-links">
        <a href="#" class="nav-link">서비스 소개</a>
        <a href="#" class="nav-link">사용 가이드</a>
        <a href="#" class="nav-link">요금제</a>
        <a href="#" class="nav-link">로그인</a>
    </div>
</div>
""", unsafe_allow_html=True)

# --- Hero 섹션 ---
st.markdown("""
<div class="hero">
    <h1 class="hero-title">AI 기반 <span class="highlight">맞춤형 포트폴리오</span> 자동 생성</h1>
    <p class="hero-subtitle">
        지원하고 싶은 기업을 입력하면, AI가 실시간으로 기업을 분석하고<br>
        당신의 경험을 최적의 포트폴리오로 재구성합니다
    </p>
</div>
""", unsafe_allow_html=True)

# --- 입력 섹션 ---
if not st.session_state.analysis_completed:
    st.markdown('<div class="input-section">', unsafe_allow_html=True)
    st.markdown("### 🎯 지원 정보 입력")
    
    col1, col2 = st.columns(2)
    
    with col1:
        company = st.text_input(
            "지원 기업명",
            placeholder="예: 네이버, 카카오, 삼성전자, Google...",
            help="분석하고 싶은 기업명을 정확히 입력해주세요"
        )
    
    with col2:
        position = st.text_input(
            "지원 직무/부서",
            placeholder="예: AI 연구팀, 백엔드 개발자, 데이터 사이언티스트...",
            help="구체적인 직무명이나 부서명을 입력하면 더 정확한 분석이 가능합니다"
        )
    
    st.markdown("### 📊 개인 데이터 연결 (선택사항)")
    
    col3, col4, col5 = st.columns(3)
    
    with col3:
        github_token = st.text_input("GitHub TOKEN", placeholder="github_pat_xxx")
    
    with col4:
        linkedin_url = st.text_input("LinkedIn URL", placeholder="https://linkedin.com/in/username")
    
    with col5:
        blog_url = st.text_input("기술 블로그 URL", placeholder="https://blog.example.com")
    
    st.markdown("---")
    
    analyze_button = st.button(
        "🔍 AI 분석 시작하기", 
        type="primary", 
        use_container_width=True,
        disabled=not (company and position)
    )
    
    if analyze_button:
        if company and position:
            st.session_state.target_company = company
            st.session_state.target_position = position
            
            # 실제 뉴스 분석 호출 (기존 더미 데이터 대신)
            with st.spinner(f'{company}의 최신 동향을 분석하고 있습니다...'):
                analysis_result = fetch_news_analysis(company, position)
                
                if analysis_result:
                    # 실제 분석 결과 사용
                    st.session_state.analysis_data = analysis_result
                else:
                    # API 실패시 기존 더미 데이터 사용
                    st.session_state.analysis_data = {
                        'company_trends': ['AI 기술 투자 확대', '클라우드 인프라 강화', '데이터 기반 의사결정'],
                        'key_skills': ['Python/PyTorch', 'Machine Learning', '대규모 데이터 처리'],
                        'company_values': ['혁신', '협업', '고객 중심'],
                        'recent_projects': ['AI 모델 최적화', 'MLOps 구축', '개인화 추천 시스템']
                    }
                
                # 맞춤형 자기소개서 생성 (기존 로직과 동일)
                st.session_state.profile_summary = f"""
{company} {position} 직무에 대한 깊은 이해와 관련 기술 역량을 바탕으로, 혁신적인 AI 솔루션 개발에 기여하고 싶습니다.

특히 Python과 PyTorch를 활용한 머신러닝 모델 개발 경험과 대규모 데이터 처리 능력을 통해, {company}의 AI 기술 투자 확대와 데이터 기반 의사결정 문화에 적극적으로 기여할 수 있습니다.

협업과 혁신을 중시하는 {company}의 기업 문화에 맞춰, 팀과 함께 성장하며 고객 중심의 가치를 실현하는 개발자가 되겠습니다.
                """.strip()
                
                st.session_state.analysis_completed = True
                st.rerun()
        else:
            st.error("기업명과 직무를 모두 입력해주세요.")
    
    st.markdown('</div>', unsafe_allow_html=True)

# --- 분석 결과 표시 (기존과 완전 동일) ---
if st.session_state.analysis_completed:
    st.markdown(f"""
    <div style="background: linear-gradient(90deg, #667eea, #764ba2); color: white; padding: 1rem; border-radius: 0.5rem; margin-bottom: 2rem; text-align: center;">
        <h3 style="margin: 0;">🎉 {st.session_state.target_company} {st.session_state.target_position} 맞춤 포트폴리오 생성 완료!</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # 탭 네비게이션
    tab1, tab2, tab3 = st.tabs([
        "🔍 AI 분석 결과",
        "🎯 핵심 역량 매칭",
        "📁 포트폴리오 자료"
    ])
    
    # --- 탭 1: AI 분석 결과 ---
    with tab1:
        col1, col2 = st.columns(2)
        
        # 기업 분석 결과
        with col1:
            st.markdown(f"""
            <div class="analysis-card">
                <div class="card-header">
                    <span class="badge badge-primary">실시간 분석 완료</span>
                    <h2 class="card-title">{st.session_state.target_company} 기업 분석</h2>
                    <p class="card-description">
                        최신 뉴스, 기술 블로그, 채용 공고를 종합 분석한 결과입니다.
                    </p>
                </div>
                <div class="skills-grid">
            """, unsafe_allow_html=True)
            
            for trend in st.session_state.analysis_data['company_trends']:
                st.markdown(f"""
                <div class="skill-item">
                    <h4>🔥 {trend}</h4>
                    <p>현재 {st.session_state.target_company}의 핵심 전략 방향</p>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("</div></div>", unsafe_allow_html=True)
        
        # 맞춤형 자기소개서
        with col2:
            st.markdown("""
            <div class="profile-card">
                <div class="card-header">
                    <span class="badge badge-success">AI 생성 완료</span>
                    <h2 class="card-title">맞춤형 자기소개서</h2>
                    <p class="card-description">기업 분석 결과를 반영한 개인화된 자기소개서입니다.</p>
                </div>
            """, unsafe_allow_html=True)
            
            if st.session_state.editing_profile:
                edited_text = st.text_area(
                    "자기소개서 수정:",
                    value=st.session_state.profile_summary,
                    height=200,
                    label_visibility="collapsed"
                )
                
                col_save, col_cancel = st.columns(2)
                if col_save.button("저장", type="primary", use_container_width=True):
                    st.session_state.profile_summary = edited_text
                    st.session_state.editing_profile = False
                    st.rerun()
                if col_cancel.button("취소", use_container_width=True):
                    st.session_state.editing_profile = False
                    st.rerun()
            else:
                st.markdown(f"""
                <div style="background: #f9fafb; padding: 1rem; border-radius: 0.5rem; line-height: 1.6; white-space: pre-line;">
                {st.session_state.profile_summary}
                </div>
                """, unsafe_allow_html=True)
                
                col_edit, col_download = st.columns(2)
                if col_edit.button("✏️ 편집", use_container_width=True):
                    st.session_state.editing_profile = True
                    st.rerun()
                
                col_download.download_button(
                    label="📄 다운로드",
                    data=st.session_state.profile_summary,
                    file_name=f"{st.session_state.target_company}_{st.session_state.target_position}_자기소개서.txt",
                    mime="text/plain",
                    use_container_width=True
                )
            
            st.markdown("</div>", unsafe_allow_html=True)
    
    # --- 탭 2: 핵심 역량 매칭 ---
    with tab2:
        st.markdown(f"""
        <div class="skills-card">
            <div class="card-header">
                <h2 class="card-title">🎯 {st.session_state.target_position} 핵심 역량 분석</h2>
                <p class="card-description">현재 역량과 요구 역량 간의 매칭도를 확인하세요.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # 스킬 매칭 결과
        skills_data = {
            'Python/PyTorch': 85,
            'Machine Learning': 78,
            '대규모 데이터 처리': 72,
            '클라우드 인프라': 65,
            '팀워크 & 협업': 90
        }
        
        for skill, score in skills_data.items():
            color = "🟢" if score >= 80 else "🟡" if score >= 70 else "🟠"
            st.write(f"{color} **{skill}**")
            st.progress(score/100, text=f"{score}% 매칭")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # 추천 개선 사항
        st.markdown("""
        <div class="analysis-card">
            <div class="card-header">
                <h3 class="card-title">💡 개선 추천사항</h3>
            </div>
            <div style="padding: 1rem; background: #fef3c7; border-radius: 0.5rem; border-left: 4px solid #f59e0b;">
                <strong>클라우드 인프라</strong> 역량 강화가 필요합니다. AWS나 GCP 관련 프로젝트를 추가하면 더욱 경쟁력 있는 포트폴리오가 될 것입니다.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # --- 탭 3: 포트폴리오 자료 ---
    with tab3:
        st.markdown("""
        <div class="analysis-card">
            <div class="card-header">
                <h2 class="card-title">📁 포트폴리오 현황</h2>
                <p class="card-description">현재 포트폴리오 자료의 완성도를 확인하세요.</p>
            </div>
        """, unsafe_allow_html=True)
        
        # 포트폴리오 항목들
        portfolio_items = [
            {"title": "AI 모델 최적화 프로젝트", "status": "완료", "relevance": "높음"},
            {"title": "데이터 파이프라인 구축", "status": "완료", "relevance": "높음"}, 
            {"title": "GitHub 오픈소스 기여", "status": "업데이트 필요", "relevance": "보통"},
            {"title": "기술 블로그 포스팅", "status": "진행중", "relevance": "보통"}
        ]
        
        for item in portfolio_items:
            status_color = "success" if item["status"] == "완료" else "warning"
            relevance_color = "primary" if item["relevance"] == "높음" else "secondary"
            
            st.markdown(f"""
            <div style="display: flex; justify-content: space-between; align-items: center; padding: 0.75rem; background: #f9fafb; border-radius: 0.5rem; margin-bottom: 0.5rem;">
                <div>
                    <strong>{item["title"]}</strong>
                </div>
                <div>
                    <span class="badge badge-{status_color}">{item["status"]}</span>
                    <span class="badge badge-{relevance_color}">관련성 {item["relevance"]}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # 파일 업로드 섹션
        st.markdown("### 📤 추가 자료 업로드")
        uploaded_files = st.file_uploader(
            "포트폴리오에 추가할 파일을 업로드하세요",
            type=['pdf', 'docx', 'pptx', 'png', 'jpg', 'jpeg'],
            accept_multiple_files=True
        )
        
        if uploaded_files:
            st.success(f"✅ {len(uploaded_files)}개의 파일이 업로드되었습니다!")
            for file in uploaded_files:
                st.write(f"• {file.name}")
    
    # 새로운 분석 시작 버튼
    st.markdown("<br><hr>", unsafe_allow_html=True)
    if st.button("🔄 새로운 기업 분석하기", type="secondary"):
        st.session_state.analysis_completed = False
        st.session_state.target_company = ""
        st.session_state.target_position = ""
        st.session_state.analysis_data = {}
        st.session_state.profile_summary = ""
        st.session_state.editing_profile = False
        st.rerun()

# --- 푸터 ---
st.markdown("""
<div style="text-align: center; padding: 2rem; color: #6b7280; border-top: 1px solid #e5e7eb; margin-top: 3rem;">
    <p>&copy; 2024 FitFolio. AI 기반 맞춤형 포트폴리오 생성 서비스</p>
    <p style="font-size: 0.875rem;">개인의 경험을 기업의 미래와 연결합니다</p>
</div>
""", unsafe_allow_html=True)
