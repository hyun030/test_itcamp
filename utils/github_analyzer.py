import streamlit as st
import google.generativeai as genai
from github import Github
from github.GithubException import UnknownObjectException

class GitHubAnalyzer:
    def __init__(self):
        self.gemini_api_key = "AIzaSyBN7rug51EVTphC3uSOzNFj66LwAHGmEGQ"
    
    def get_all_repos_readme_content(self, github_token):
        """GitHub 토큰을 사용해서 모든 저장소의 README 내용 가져오기"""
        readme_list = []
        try:
            g = Github(github_token)
            user_repos = g.get_user().get_repos()
            for repo in user_repos:
                try:
                    file_content = repo.get_contents("README.md")
                    readme_text = file_content.decoded_content.decode('utf-8')
                    readme_list.append(readme_text)
                except UnknownObjectException:
                    continue  # README.md가 없으면 건너뛰기
                except Exception as e:
                    continue  # 다른 오류도 건너뛰기
            return readme_list
        except Exception as e:
            st.error(f"GitHub 접근 오류: {str(e)}")
            return []

    def summarize_text_with_gemini(self, text_list):
        """Gemini API를 사용해서 GitHub 프로젝트들 요약"""
        try:
            genai.configure(api_key=self.gemini_api_key)
            model = genai.GenerativeModel('gemini-1.5-pro-latest')
            
            combined_text = "\n\n".join(text_list)
            
            prompt = f"""
            다음은 여러 GitHub 저장소의 README 파일 내용입니다. 이 내용들을 종합하여 한 사람의 포트폴리오 관점에서 어떤 프로젝트들을 수행했는지, 기술 스택은 무엇인지, 그리고 전반적인 특징이 무엇인지 줄글 형식으로 요약해 주세요. 각 프로젝트를 명확하게 구분하여 설명해 주시고, 전체적인 내용을 종합하는 내용도 포함시켜 주세요.
            
            {combined_text}
            """
            
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            st.error(f"Gemini API 오류: {str(e)}")
            return None

    def analyze_github_projects(self, github_token):
        """GitHub 프로젝트 분석 전체 프로세스"""
        with st.spinner("GitHub 저장소를 분석하는 중입니다..."):
            readme_content = self.get_all_repos_readme_content(github_token)
            
            if readme_content:
                with st.spinner("AI로 프로젝트를 요약하는 중입니다..."):
                    summary = self.summarize_text_with_gemini(readme_content)
                    return summary
            else:
                return None
