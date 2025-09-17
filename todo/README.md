# Django practice

## install 및 start Project
```cmd
py --list # 윈도우 내 파이선 버전 확인해보기

py -3.12 -m venv venv
./venv/Scripts/activate # 가상환경 실행

# 장고 LTS 기준으로 설치
pip install Django==4.2.* djangorestframework

# pip install django-silk drf-spectacular django-filter
pip freeze > requirements.txt

# 장고 프로젝트 런치
python -m django startproject config .

# 장고 api 앱 추가
python manage.py startapp common
python manage.py startapp users
python manage.py startapp todos

# 모델 변경 감지해서 마이그레이션 파일 생성
python manage.py makemigrations

# 마이그레이션 실제 DB에 반영
python manage.py migrate

# 슈퍼 유저 만들기
python manage.py createsuperuser

# 개발 서버 실행
python manage.py runserver
```