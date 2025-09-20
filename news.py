import requests
import json

def fetch_news(company, role):

    url = "https://api.perplexity.ai/chat/completions"

    payload = {
        "model": "sonar",
        "messages": [
            {
                "role": "system",
                "content": """기업의 이름과 직무를 입력할거야. 그럼 너는 그와 관련된 기업 트렌드, 핵심 역량, 기업의 인재상에 대해 조사해줘. 각 항목에 대해 3가지를 다음과 같은 json 형식으로 출력해줘.
                    {
                        "trend": [
                            "trend1",
                            "trend2",
                            "trend3"
                        ],
                        "skills": [
                            "skill1",
                            "skill2",
                            "skill3"
                        ],
                        "company_values": [
                            "value1",
                            "value2",
                            "value3"
                        ]
                    }
                    
                    각 항목은 한국어로 출력하고, 링크 주석이나 강조 효과 없이 텍스트로만 출력해줘."""
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

    response = requests.post(url, json=payload, headers=headers)
    result = response.json()

    # 응답에서 content 부분 추출
    content = result["choices"][0]["message"]["content"]

    # 문자열(JSON 텍스트)을 파이썬 dict로 변환
    data = json.loads(content)

    # 원하는 항목만 반환
    return data["trend"], data["skills"], data["company_values"]

# 테스트용
# fetch_news('카카오', '프론트엔드 개발자')