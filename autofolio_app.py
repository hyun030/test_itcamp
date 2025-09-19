<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FitFolio - AI 포트폴리오 프로토타입</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700;900&display=swap" rel="stylesheet">
    <style>
        /* --- 기본 및 레이아웃 스타일 (기존과 유사) --- */
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
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: 'Noto Sans KR', sans-serif;
            background-color: var(--secondary-color);
            color: var(--text-color);
            line-height: 1.6;
        }
        .container { max-width: 1200px; margin: 0 auto; padding: 2rem; }
        .page { display: none; animation: fadeIn 0.5s ease-in-out; }
        .page.active { display: block; }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        /* --- 공용 컴포넌트 (기존과 유사) --- */
        .btn {
            display: inline-block; background-color: var(--primary-color); color: white;
            padding: 0.8rem 1.8rem; border: none; border-radius: 8px; font-size: 1rem;
            font-weight: 700; cursor: pointer; text-decoration: none; transition: all 0.2s ease;
        }
        .btn:hover { background-color: var(--primary-hover); transform: translateY(-2px); box-shadow: 0 4px 10px rgba(0,0,0,0.1); }
        .btn:disabled { background-color: #A0AEC0; cursor: not-allowed; transform: none; box-shadow: none; }
        .card {
            background: white; border-radius: 12px; padding: 2rem;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
            margin-bottom: 1.5rem;
        }
        h1, h2, h3, h4 { font-weight: 900; letter-spacing: -0.5px; }
        .page-description { text-align: center; color: var(--subtext-color); margin-bottom: 2.5rem; }
        .text-center { text-align: center; }

        /* --- 1. 랜딩 페이지 --- */
        #landing-page { text-align: center; padding: 4rem 1rem; }
        #landing-page h1 { font-size: 3rem; margin-bottom: 1rem; }
        #landing-page .highlight { color: var(--primary-color); }
        #landing-page p { font-size: 1.2rem; color: var(--subtext-color); max-width: 600px; margin: 0 auto 2rem; }

        /* --- 2. 데이터 연동 페이지 (수정됨) --- */
        #connect-page h2 { font-size: 2rem; text-align: center; margin-bottom: 2.5rem; }
        .connect-grid {
            display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1.5rem;
        }
        .connect-card {
            display: flex; align-items: center; padding: 1.5rem; border: 1px solid var(--border-color);
            border-radius: 10px; transition: all 0.2s ease; background-color: white;
        }
        .connect-card:hover { transform: translateY(-4px); box-shadow: 0 4px 12px rgba(0,0,0,0.08); }
        .connect-card .icon { width: 40px; height: 40px; margin-right: 1.5rem; }
        .connect-card .info h3 { font-size: 1.2rem; margin-bottom: 0.2rem; }
        .connect-card .info p { color: var(--subtext-color); font-size: 0.9rem; }
        .connect-btn {
            margin-left: auto; padding: 0.5rem 1rem; font-size: 0.9rem; background-color: #F0F4F8;
            color: var(--text-color); border: 1px solid var(--border-color); white-space: nowrap;
        }
        .connect-btn.connected {
            background-color: var(--green-light); color: var(--green-dark);
            border-color: var(--green-dark); cursor: default;
        }

        /* --- 3. 맞춤화 입력 페이지 --- */
        #input-page h2 { text-align: center; font-size: 2rem; margin-bottom: 2rem; }
        .input-form { max-width: 500px; margin: 0 auto; }
        .form-group { margin-bottom: 1.5rem; }
        .form-group label { display: block; font-weight: 700; margin-bottom: 0.5rem; }
        .form-group input {
            width: 100%; padding: 0.8rem; border: 1px solid var(--border-color);
            border-radius: 8px; font-size: 1rem;
        }
        .input-form .btn { width: 100%; }

        /* --- 4. AI 분석 페이지 (수정됨) --- */
        #analysis-page {
            display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 60vh;
        }
        .spinner {
            width: 60px; height: 60px; border: 6px solid var(--border-color);
            border-top-color: var(--primary-color); border-radius: 50%;
            animation: spin 1s linear infinite; margin-bottom: 2rem;
        }
        @keyframes spin { to { transform: rotate(360deg); } }
        #analysis-text { font-size: 1.1rem; font-weight: 500; color: var(--subtext-color); transition: opacity 0.3s; }

        /* --- 5. 결과 페이지 (수정됨) --- */
        #result-page header { text-align: center; margin-bottom: 3rem; }
        #result-page header h2 { font-size: 2.5rem; }
        #result-page header .company-name { color: var(--primary-color); }
        .portfolio-section h3 {
            font-size: 1.5rem; margin-bottom: 1rem; padding-bottom: 0.5rem;
            border-bottom: 2px solid var(--border-color); display: flex; align-items: center;
        }
        .portfolio-section h3 .icon-emoji { margin-right: 0.75rem; }
        
        #ai-summary-card { background-color: #F0F4FF; border-left: 4px solid var(--primary-color); }
        #ai-summary-card h3 { border: none; }
        #ai-summary-card p { font-size: 1.1rem; }

        .skills-grid { display: flex; flex-wrap: wrap; gap: 0.8rem; }
        .skill-tag {
            padding: 0.5rem 1rem; border-radius: 20px;
            background-color: var(--secondary-color); font-weight: 500;
        }
        .skill-tag.highlighted {
            background-color: var(--highlight-bg); color: var(--highlight-text); font-weight: 700;
        }

        .project-card { border: 1px solid var(--border-color); padding: 1.5rem; border-radius: 10px; margin-bottom: 1.5rem; }
        .project-card h4 { font-size: 1.3rem; margin-bottom: 0.5rem; }
        .project-card .description { color: var(--subtext-color); }
        .project-card .ai-rewrite {
            margin-top: 1.5rem; padding: 1rem; background-color: #F0FFF4;
            border-left: 4px solid var(--green-dark); border-radius: 4px;
        }
        .ai-rewrite .rewrite-header { display: flex; align-items: center; font-weight: 700; color: var(--green-dark); margin-bottom: 0.5rem; }
        .ai-rewrite .rewrite-header span { margin-left: 0.5rem; }

    </style>
</head>
<body>

    <div class="container">

        <div id="landing-page" class="page active">
            <h1>당신의 커리어, <span class="highlight">AI가 맞춤 설계</span>합니다.</h1>
            <p>FitFolio는 흩어진 당신의 경험을 모아 지원하는 기업에 맞춰 포트폴리오를 자동으로 재구성해주는 가장 스마트한 방법입니다.</p>
            <button id="start-btn" class="btn">내 포트폴리오 만들기</button>
        </div>

        <div id="connect-page" class="page">
            <h2>1. 데이터 연동하기</h2>
            <div class="connect-grid">
                <div class="connect-card">
                    <img src="https://simpleicons.org/icons/github.svg" class="icon" alt="GitHub Icon">
                    <div class="info">
                        <h3>GitHub</h3>
                        <p>프로젝트와 코드를 가져옵니다.</p>
                    </div>
                    <button class="btn connect-btn" data-platform="github">연동하기</button>
                </div>
                 <div class="connect-card">
                    <img src="https://simpleicons.org/icons/linkedin.svg" class="icon" alt="LinkedIn Icon">
                    <div class="info">
                        <h3>LinkedIn</h3>
                        <p>경력과 학력을 가져옵니다.</p>
                    </div>
                    <button class="btn connect-btn" data-platform="linkedin">연동하기</button>
                </div>
                 <div class="connect-card">
                    <img src="https://simpleicons.org/icons/tistory.svg" class="icon" alt="Blog Icon">
                    <div class="info">
                        <h3>블로그 (Tistory)</h3>
                        <p>작성한 글과 전문성을 가져옵니다.</p>
                    </div>
                    <button class="btn connect-btn" data-platform="blog">연동하기</button>
                </div>
                 <div class="connect-card">
                    <img src="https://simpleicons.org/icons/behance.svg" class="icon" alt="Behance Icon">
                    <div class="info">
                        <h3>Behance</h3>
                        <p>디자인 작업물을 가져옵니다.</p>
                    </div>
                    <button class="btn connect-btn" data-platform="behance">연동하기</button>
                </div>
            </div>
            <div class="text-center" style="margin-top: 3rem;">
                <button id="next-to-input-btn" class="btn" disabled>다음 단계로</button>
            </div>
        </div>

        <div id="input-page" class="page">
            <h2>2. 포트폴리오 맞춤화</h2>
            <div class="input-form card">
                <div class="form-group">
                    <label for="company-name">지원 회사명</label>
                    <input type="text" id="company-name" placeholder="예: 삼성전자">
                </div>
                 <div class="form-group">
                    <label for="job-title">지원 직무</label>
                    <input type="text" id="job-title" placeholder="예: AI 연구원">
                </div>
                <button id="generate-btn" class="btn">AI 맞춤 포트폴리오 생성</button>
            </div>
        </div>

        <div id="analysis-page" class="page">
            <div class="spinner"></div>
            <h2 id="analysis-text">AI가 포트폴리오를 분석하고 있습니다...</h2>
        </div>

        <div id="result-page" class="page">
            <header>
                <h2><span id="result-company-name" class="company-name"></span> 맞춤 포트폴리오</h2>
                <p>FitFolio의 AI가 <strong id="result-job-title"></strong> 직무에 맞춰 재구성한 결과입니다.</p>
            </header>
            
            <section id="ai-summary-card" class="portfolio-section card">
                <h3><span class="icon-emoji">💡</span>AI 분석 요약</h3>
                <p id="ai-summary"></p>
            </section>

             <section class="portfolio-section card">
                <h3><span class="icon-emoji">🎯</span>핵심 역량 (Skills)</h3>
                <div class="skills-grid" id="skills-container">
                    </div>
            </section>

            <section class="portfolio-section card">
                <h3><span class="icon-emoji">🚀</span>프로젝트 재구성 (Projects)</h3>
                <div id="projects-container">
                    </div>
            </section>
            
            <div class="text-center" style="margin-top: 2rem;">
                <button class="btn">PDF로 다운로드</button>
            </div>
        </div>

    </div>


    <script>
        document.addEventListener('DOMContentLoaded', () => {
            // --- DOM 요소 ---
            const pages = document.querySelectorAll('.page');
            const startBtn = document.getElementById('start-btn');
            const connectBtns = document.querySelectorAll('.connect-btn');
            const nextToInputBtn = document.getElementById('next-to-input-btn');
            const generateBtn = document.getElementById('generate-btn');
            const companyInput = document.getElementById('company-name');
            const jobInput = document.getElementById('job-title');
            const analysisText = document.getElementById('analysis-text');

            // --- 상태 변수 ---
            let connectedPlatforms = new Set();

            // --- 더미 데이터 (시뮬레이션용) ---
            const userProfile = {
                skills: ['Python', 'PyTorch', 'TensorFlow', 'LLM', 'On-Device AI', 'React', 'Data Analysis'],
                projects: [
                    {
                        title: '모바일 기기용 이미지 분류 모델 경량화',
                        description: 'TensorFlow Lite를 사용하여 CNN 모델의 크기를 줄이고, 모바일 환경에서의 추론 속도를 30% 개선한 프로젝트입니다.',
                        relatedSkills: ['Python', 'TensorFlow', 'On-Device AI']
                    },
                    {
                        title: '소셜 미디어 감성 분석 모델',
                        description: 'LSTM 기반의 딥러닝 모델을 사용하여 소셜 미디어 텍스트의 긍정/부정을 분류하는 프로젝트를 진행했습니다. 데이터 전처리부터 모델 학습, 평가까지 전 과정을 담당했습니다.',
                        relatedSkills: ['Python', 'PyTorch', 'LLM']
                    },
                ]
            };

            // --- 함수 ---

            // 페이지 전환 함수
            function showPage(pageId) {
                pages.forEach(page => page.classList.remove('active'));
                document.getElementById(pageId).classList.add('active');
            }

            // '다음 단계' 버튼 상태 업데이트
            function updateConnectState() {
                if (connectedPlatforms.size > 0) {
                    nextToInputBtn.disabled = false;
                } else {
                    nextToInputBtn.disabled = true;
                }
            }
            
            // AI 분석 시뮬레이션 함수
            function startAnalysisSimulation(company, job) {
                showPage('analysis-page');
                const messages = [
                    `'${company}'의 최신 기술 블로그를 분석 중입니다...`,
                    "채용 공고의 핵심 요구 역량을 추출하고 있습니다...",
                    `'${job}' 직무와 회원님의 경험 데이터 매칭 중...`,
                    "프로젝트 설명을 AI가 재구성하는 중...",
                    "맞춤 포트폴리오 생성 완료!"
                ];
                let messageIndex = 0;
                analysisText.textContent = messages[messageIndex];
                
                const interval = setInterval(() => {
                    messageIndex++;
                    if (messageIndex < messages.length) {
                        analysisText.style.opacity = '0';
                        setTimeout(() => {
                            analysisText.textContent = messages[messageIndex];
                            analysisText.style.opacity = '1';
                        }, 300);
                    } else {
                        clearInterval(interval);
                        renderResultPage(company, job);
                    }
                }, 2000); // 2초마다 메시지 변경
            }

            // 결과 페이지 렌더링 함수
            function renderResultPage(company, job) {
                document.getElementById('result-company-name').textContent = company;
                document.getElementById('result-job-title').textContent = job;
                
                // AI 분석 요약 (시뮬레이션)
                const aiSummary = document.getElementById('ai-summary');
                aiSummary.innerHTML = `FitFolio AI가 분석한 '${company} ${job}' 직무의 핵심은 <strong>'LLM 경량화'</strong>와 <strong>'온디바이스 AI'</strong> 경험입니다. 회원님의 경험을 이 키워드에 맞춰 강조하고 재구성했습니다.`;
                
                // 스킬 렌더링 (시뮬레이션)
                const skillsContainer = document.getElementById('skills-container');
                skillsContainer.innerHTML = '';
                const requiredSkills = ['On-Device AI', 'LLM', 'PyTorch']; // AI가 추출한 필수 스킬로 가정
                userProfile.skills.forEach(skill => {
                    const skillTag = document.createElement('div');
                    skillTag.className = 'skill-tag';
                    skillTag.textContent = skill;
                    if (requiredSkills.includes(skill)) {
                        skillTag.classList.add('highlighted');
                    }
                    skillsContainer.appendChild(skillTag);
                });

                // 프로젝트 렌더링 (시뮬레이션)
                const projectsContainer = document.getElementById('projects-container');
                projectsContainer.innerHTML = '';
                // AI가 관련성 높은 순으로 정렬했다고 가정
                userProfile.projects.forEach((project) => {
                    const projectCard = document.createElement('div');
                    projectCard.className = 'project-card';
                    
                    let aiRewriteHTML = '';
                    // AI가 모든 관련 프로젝트를 재구성했다고 가정
                    if (project.relatedSkills.some(skill => requiredSkills.includes(skill))) {
                        aiRewriteHTML = `
                            <div class="ai-rewrite">
                                <div class="rewrite-header">✨<span>AI Rewrite</span></div>
                                <p>'${company}'가 최근 집중하고 있는 <strong>'온디바이스 AI'</strong> 전략에 맞춰, <strong>TensorFlow Lite 기반 모델 경량화</strong> 경험을 강조했습니다. 이를 통해 제한된 하드웨어 환경에서의 효율적인 AI 모델 배포 및 운영 능력을 어필할 수 있습니다.</p>
                            </div>
                        `;
                    }

                    projectCard.innerHTML = `
                        <h4>${project.title}</h4>
                        <p class="description">${project.description}</p>
                        ${aiRewriteHTML}
                    `;
                    projectsContainer.appendChild(projectCard);
                });

                showPage('result-page');
            }

            // --- 이벤트 리스너 ---

            // 시작하기 버튼
            startBtn.addEventListener('click', () => showPage('connect-page'));

            // 플랫폼 연동 버튼
            connectBtns.forEach(btn => {
                btn.addEventListener('click', () => {
                    const platform = btn.dataset.platform;
                    btn.textContent = '연동 완료 ✔';
                    btn.classList.add('connected');
                    btn.disabled = true;
                    connectedPlatforms.add(platform);
                    updateConnectState();
                });
            });

            // 다음 단계로 버튼
            nextToInputBtn.addEventListener('click', () => showPage('input-page'));

            // 포트폴리오 생성 버튼
            generateBtn.addEventListener('click', () => {
                const company = companyInput.value.trim();
                const job = jobInput.value.trim();

                if (!company || !job) {
                    alert('회사명과 직무를 모두 입력해주세요.');
                    return;
                }
                
                startAnalysisSimulation(company, job);
            });
        });
    </script>
</body>
</html>
