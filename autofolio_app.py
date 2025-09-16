import streamlit as st
import pandas as pd
from typing import Literal
import base64
from io import BytesIO

# 페이지 설정
st.set_page_config(
    page_title="삼성전자 맞춤 포트폴리오",
    page_icon="🔵",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS 스타일 정의
def load_css():
    st.markdown("""
    <style>
    /* 기본 스타일 */
    .main-header {
        background: linear-gradient(135deg, #f0f8ff 0%, #ffffff 50%, #f0f4ff 100%);
        padding: 2rem 0;
        margin-bottom: 2rem;
        border-radius: 0 0 20px 20px;
        text-align: center;
    }
    
    .hero-title {
        background: linear-gradient(45deg, #2563eb, #4f46e5);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3.5rem;
        font-weight: bold;
        margin: 1rem 0;
    }
    
    .hero-subtitle {
        color: #64748b;
        font-size: 1.2rem;
        margin-bottom: 2rem;
        line-height: 1.6;
    }
    
    .card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        border: 1px solid #e2e8f0;
        margin-bottom: 2rem;
    }
    
    .analysis-card {
        background: linear-gradient(135deg, #eff6ff 0%, #e0e7ff 100%);
        border: 1px solid #bfdbfe;
    }
    
    .profile-card {
        background: linear-gradient(135deg, #fefbeb 0%, #fef3c7 100%);
        border: 1px solid #fcd34d;
    }
    
    .skill-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.75rem 1rem;
        background: #f8fafc;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 4px solid #3b82f6;
    }
    
    .progress-bar {
        background: #e5e7eb;
        border-radius: 10px;
        height: 8px;
        margin: 0.5rem 0;
    }
    
    .progress-fill {
        background: linear-gradient(90deg, #3b82f6, #1d4ed8);
        height: 100%;
        border-radius: 10px;
        transition: width 0.3s ease;
    }
    
    .badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 500;
        margin: 0.25rem;
    }
    
    .badge-primary {
        background: #dbeafe;
        color: #1e40af;
    }
    
    .badge-success {
        background: #dcfce7;
        color: #166534;
    }
    
    .badge-warning {
        background: #fef3c7;
        color: #92400e;
    }
    
    .badge-danger {
        background: #fee2e2;
        color: #991b1b;
    }
    
    .portfolio-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1rem;
        border: 1px solid #e5e7eb;
        border-radius: 10px;
        margin: 0.5rem 0;
        transition: background-color 0.2s;
    }
    
    .portfolio-item:hover {
        background-color: #f9fafb;
    }
    
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        border: 1px solid #e5e7eb;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: #1f2937;
    }
    
    .metric-label {
        color: #6b7280;
        font-size: 0.9rem;
        margin-top: 0.5rem;
    }
    
    /* 탭 스타일 */
    .tab-container {
        border-bottom: 2px solid #e5e7eb;
        margin-bottom: 2rem;
    }
    
    /* 반응형 */
    @media (max-width: 768px) {
        .hero-title {
            font-size: 2.5rem;
        }
        .card {
            padding: 1rem;
        }
    }
    </style>
    """, unsafe_allow_html=True)

# 헤더 컴포넌트
def render_header():
    st.markdown("""
    <div style="background: white; padding: 1rem 0; border-bottom: 1px solid #e5e7eb; margin-bottom: 0;">
        <div style="max-width: 1200px; margin: 0 auto; display: flex; justify-content: space-between; align-items: center;">
            <div style="display: flex; align-items: center;">
                <div style="width: 40px; height: 40px; background: #2563eb; border-radius: 8px; display: flex; align-items: center; justify-content: center; margin-right: 1rem;">
                    <span style="color: white; font-weight: bold; font-size: 1.2rem;">S</span>
                </div>
                <span style="font-size: 1.5rem; font-weight: 600; color: #1f2937;">삼성전자</span>
                <span class="badge badge-primary" style="margin-left: 1rem;">AI 채용 플랫폼</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# 히어로 섹션
def render_hero_section():
    st.markdown("""
    <div class="main-header">
        <div style="display: flex; align-items: center; justify-content: center; margin-bottom: 1rem;">
            <span style="color: #2563eb; margin-right: 0.5rem;">✨</span>
            <span class="badge badge-primary">AI 기반 맞춤형 분석</span>
        </div>
        <h1 class="hero-title">삼성전자 맞춤 포트폴리오</h1>
        <p class="hero-subtitle">
            시각 <strong style="color: #2563eb;">'AI 연구팀'</strong> 직무에 맞춘 제7성할 질문입니다.<br>
            AI가 분석한 맞춤형 포트폴리오로 성공적인 지원을 준비하세요.
        </p>
        <div style="display: flex; justify-content: center; gap: 2rem; color: #6b7280; font-size: 0.9rem;">
            <div>🎯 맞춤형 분석</div>
            <div>🧠 AI 전략 제안</div>
            <div>✨ 자동 생성</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# AI 분석 카드
def render_analysis_card():
    st.markdown("""
    <div class="card analysis-card">
        <div style="display: flex; align-items: center; margin-bottom: 1rem;">
            <span style="font-size: 1.5rem; margin-right: 0.5rem;">🧠</span>
            <span class="badge badge-primary">AI 분석 완료</span>
        </div>
        <h2 style="color: #1e3a8a; margin-bottom: 1rem;">AI 기반 분석 및 전략 제안</h2>
        <p style="color: #3730a3; margin-bottom: 2rem; line-height: 1.6;">
            AI가 분석한 '삼성전자'의 최고 역량 기준에 '초기 AI', 'LLM 전문성', 'HBM 반도체'입니다. 
            따라서 'AI 연구팀' 직무에서는 관련 기술 경험과 반도체 산업에 대한 이해도를 함께 어필하는 것이 중요합니다.
        </p>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin-bottom: 2rem;">
            <div style="background: rgba(255,255,255,0.7); padding: 1rem; border-radius: 10px; border: 1px solid #bfdbfe;">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">📈</div>
                <h4 style="color: #1e3a8a; margin-bottom: 0.5rem;">LLM 전문성</h4>
                <p style="color: #3730a3; font-size: 0.9rem;">대규모 언어모델 연구 경험</p>
            </div>
            <div style="background: rgba(255,255,255,0.7); padding: 1rem; border-radius: 10px; border: 1px solid #bfdbfe;">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">👥</div>
                <h4 style="color: #1e3a8a; margin-bottom: 0.5rem;">HBM 반도체</h4>
                <p style="color: #3730a3; font-size: 0.9rem;">고대역폭 메모리 기술 이해</p>
            </div>
            <div style="background: rgba(255,255,255,0.7); padding: 1rem; border-radius: 10px; border: 1px solid #bfdbfe;">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">💡</div>
                <h4 style="color: #1e3a8a; margin-bottom: 0.5rem;">초기 AI</h4>
                <p style="color: #3730a3; font-size: 0.9rem;">AI 기술 연구개발 역량</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# 프로필 요약 카드
def render_profile_summary_card():
    st.markdown("""
    <div class="card profile-card">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
            <div style="display: flex; align-items: center;">
                <span style="font-size: 1.5rem; margin-right: 0.5rem;">📝</span>
                <span class="badge badge-warning">자동 생성됨</span>
            </div>
        </div>
        <h2 style="color: #92400e; margin-bottom: 1rem;">AI 자기소개서 초안 (Profile Summary)</h2>
        <p style="color: #b45309; margin-bottom: 2rem;">
            AI가 생성한 맞춤형 자기소개서 초안입니다. 필요에 따라 수정하여 사용하세요.
        </p>
    """, unsafe_allow_html=True)
    
    # 편집 가능한 텍스트 영역
    if 'profile_text' not in st.session_state:
        st.session_state.profile_text = "'AI 연구팀' 직무에 대한 깊은 이해와 LLM, PyTorch 역량을 바탕으로..."
    
    profile_text = st.text_area(
        "자기소개서 내용",
        value=st.session_state.profile_text,
        height=150,
        help="자기소개서 내용을 수정할 수 있습니다."
    )
    st.session_state.profile_text = profile_text
    
    # 키워드 태그
    st.markdown("""
        <div style="margin-top: 1rem;">
            <span class="badge badge-warning">AI 연구</span>
            <span class="badge badge-warning">LLM</span>
            <span class="badge badge-warning">PyTorch</span>
            <span class="badge badge-warning">반도체</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# 스킬 분석 콘텐츠
def render_skills_content():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("## ⭐ 핵심 역량 분석")
    st.markdown("AI 연구팀 직무에 필요한 핵심 기술과 현재 수준을 평가했습니다.")
    
    # 스킬 데이터
    skills_data = [
        {"skill": "Python/PyTorch", "level": 90, "required": True, "priority": "높음"},
        {"skill": "Large Language Models", "level": 85, "required": True, "priority": "높음"},
        {"skill": "반도체 기술 이해", "level": 70, "required": True, "priority": "보통"},
        {"skill": "머신러닝 알고리즘", "level": 80, "required": True, "priority": "높음"},
        {"skill": "데이터 분석", "level": 75, "required": False, "priority": "보통"},
        {"skill": "논문 작성", "level": 65, "required": False, "priority": "낮음"},
    ]
    
    for skill in skills_data:
        priority_color = {
            "높음": "danger",
            "보통": "warning", 
            "낮음": "primary"
        }[skill["priority"]]
        
        st.markdown(f"""
        <div class="skill-item">
            <div style="display: flex; align-items: center; gap: 0.5rem;">
                <strong>{skill["skill"]}</strong>
                {'<span class="badge badge-success">필수</span>' if skill["required"] else ''}
                <span class="badge badge-{priority_color}">{skill["priority"]}</span>
            </div>
            <span>{skill["level"]}%</span>
        </div>
        <div class="progress-bar">
            <div class="progress-fill" style="width: {skill["level"]}%;"></div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 관련 경험 및 프로젝트
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("## 관련 경험 및 프로젝트")
    st.markdown("직무와 연관된 경험들의 완성도와 관련성을 확인하세요.")
    
    experiences = [
        {"title": "AI 모델 최적화 프로젝트", "status": "완료", "relevance": "높음"},
        {"title": "LLM 파인튜닝 경험", "status": "완료", "relevance": "높음"},
        {"title": "반도체 관련 연구", "status": "진행중", "relevance": "보통"},
        {"title": "논문 게재 경험", "status": "계획", "relevance": "낮음"},
    ]
    
    for exp in experiences:
        status_icon = {"완료": "✅", "진행중": "🔄", "계획": "📋"}[exp["status"]]
        relevance_color = {
            "높음": "success",
            "보통": "warning",
            "낮음": "primary"
        }[exp["relevance"]]
        
        st.markdown(f"""
        <div class="portfolio-item">
            <div style="display: flex; align-items: center; gap: 1rem;">
                <span style="font-size: 1.2rem;">{status_icon}</span>
                <strong>{exp["title"]}</strong>
            </div>
            <div style="display: flex; gap: 0.5rem;">
                <span class="badge badge-{relevance_color}">관련성 {exp["relevance"]}</span>
                <span class="badge badge-primary">{exp["status"]}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# 포트폴리오 콘텐츠
def render_portfolio_content():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("## 📁 포트폴리오 현황")
    st.markdown("현재 포트폴리오 자료의 완성도를 확인하고 부족한 부분을 보완하세요.")
    
    portfolio_items = [
        {"type": "문서", "title": "AI 모델 성능 최적화 보고서", "desc": "PyTorch를 활용한 LLM 최적화 프로젝트 결과", "status": "완료"},
        {"type": "코드", "title": "GitHub 리포지토리", "desc": "오픈소스 기여 및 개인 프로젝트", "status": "업데이트 필요"},
        {"type": "발표", "title": "연구 발표 자료", "desc": "AI 연구팀 관련 발표 슬라이드", "status": "누락"},
    ]
    
    for item in portfolio_items:
        status_colors = {
            "완료": "success",
            "업데이트 필요": "warning",
            "누락": "danger"
        }
        
        st.markdown(f"""
        <div class="portfolio-item">
            <div style="display: flex; align-items: center; gap: 1rem;">
                <span style="font-size: 1.5rem;">{'📄' if item['type'] == '문서' else '💻' if item['type'] == '코드' else '🎯'}</span>
                <div>
                    <strong>{item["title"]}</strong>
                    <div style="color: #6b7280; font-size: 0.9rem;">{item["desc"]}</div>
                </div>
            </div>
            <span class="badge badge-{status_colors[item["status"]]}">{item["status"]}</span>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 추천 자료
    st.markdown('<div class="card" style="background: linear-gradient(135deg, #eff6ff 0%, #e0e7ff 100%); border: 1px solid #bfdbfe;">', unsafe_allow_html=True)
    st.markdown("## 💡 추천 자료")
    st.markdown("AI 연구팀 지원을 위해 추가로 준비하면 좋은 자료들입니다.")
    
    recommendations = [
        {"title": "기술 블로그 작성", "desc": "AI 연구 과정과 인사이트를 공유하는 블로그 포스트", "priority": "높음"},
        {"title": "오픈소스 기여", "desc": "PyTorch 또는 관련 라이브러리에 기여한 내역", "priority": "보통"},
        {"title": "논문 요약 자료", "desc": "최신 AI 논문을 분석하고 요약한 자료", "priority": "보통"},
    ]
    
    for rec in recommendations:
        priority_color = "danger" if rec["priority"] == "높음" else "warning"
        st.markdown(f"""
        <div style="background: rgba(255,255,255,0.7); padding: 1rem; border-radius: 10px; margin: 0.5rem 0; border: 1px solid #bfdbfe;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <strong style="color: #1e3a8a;">{rec["title"]}</strong>
                    <div style="color: #3730a3; font-size: 0.9rem;">{rec["desc"]}</div>
                </div>
                <span class="badge badge-{priority_color}">우선순위 {rec["priority"]}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 파일 업로드
    st.markdown('<div class="card" style="background: linear-gradient(135deg, #faf5ff 0%, #f3e8ff 100%); border: 1px solid #c084fc;">', unsafe_allow_html=True)
    st.markdown("## 📤 자료 업로드")
    st.markdown("기존 자료를 업로드하여 AI 분석을 받아보세요.")
    
    uploaded_files = st.file_uploader(
        "파일을 선택하세요",
        type=['pdf', 'docx', 'pptx', 'png', 'jpg', 'jpeg'],
        accept_multiple_files=True,
        help="PDF, DOCX, PPT, 이미지 파일을 지원합니다."
    )
    
    if uploaded_files:
        st.success(f"{len(uploaded_files)}개의 파일이 업로드되었습니다!")
        for file in uploaded_files:
            st.write(f"📄 {file.name} ({file.size} bytes)")
    
    st.markdown('</div>', unsafe_allow_html=True)

# 메인 앱
def main():
    # CSS 로드
    load_css()
    
    # 세션 상태 초기화
    if 'active_tab' not in st.session_state:
        st.session_state.active_tab = 'AI 분석 학습'
    
    # 헤더
    render_header()
    
    # 히어로 섹션
    render_hero_section()
    
    # 탭 네비게이션
    tab1, tab2, tab3 = st.tabs(['🔍 AI 분석 학습', '🎯 핵심 역량', '📁 포트폴리오 준비'])
    
    with tab1:
        col1, col2 = st.columns([1, 1], gap="large")
        with col1:
            render_analysis_card()
        with col2:
            render_profile_summary_card()
    
    with tab2:
        render_skills_content()
    
    with tab3:
        render_portfolio_content()
    
    # 푸터
    st.markdown("""
    <div style="margin-top: 4rem; padding: 2rem; background: white; border-top: 1px solid #e5e7eb; text-align: center; color: #6b7280;">
        <p>&copy; 2024 삼성전자. AI 기반 채용 플랫폼</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
