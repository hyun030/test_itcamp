from github import Github
from github.GithubException import UnknownObjectException

# 환경 변수에서 API 키를 가져오는 것을 권장합니다.
# 직접 코드에 넣을 경우 아래 두 변수에 발급받은 실제 키를 입력하세요.
# GITHUB_TOKEN = "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"

def get_readme_list(github_token):
    readme_list = []
    try:
        g = Github(github_token)
        print("모든 저장소 목록을 불러오는 중...")
        user_repos = g.get_user().get_repos()
        for repo in user_repos:
            print(f"\n--- 저장소: {repo.full_name} ---")
            try:
                file_content = repo.get_contents("README.md")
                readme_text = file_content.decoded_content.decode('utf-8')
                print(readme_text)
                readme_list.append(readme_text)

            except UnknownObjectException:
                print("README.md 파일이 존재하지 않습니다.")
            except Exception as e:
                print(f"README.md 파일을 가져오는 중 오류 발생: {e}")
        return readme_list

    except Exception as e:
        print(f"오류 발생: {e}")
