# 간단한 커머스 api 연습해보기

## 환경 설정 및 프로젝트 설치
```cmd
python3.12 -m venv venv
./venv/Script/activate # 가상환경 활성화

# 장고 LTS 기준으로 설치
pip install Django==4.2.* djangorestframework
pip install django-silk drf-spectacular django-filter # 라이브러리 추가 설치

pip freeze > requirements.txt

# 장고 프로젝트 런치
python -m django startproject config .

# 장고 앱 추가
python manage.py startapp common

```
## 참고 강의 및 깃헙
- https://www.youtube.com/watch?v=5W2Yff00H8s&list=PL-2EBeDYMIbTLulc9FSoAXhbmXpLq2l5t&index=26
- https://github.com/bugbytes-io/drf-course-api
