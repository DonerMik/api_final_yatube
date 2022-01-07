# **_Как запустить проект:_**

Клонировать репозиторий и перейти в него в командной строке:

git clone https://github.com/DonerMik/api_final_yatube/

cd api_final_yatube

**_Cоздать и активировать виртуальное окружение:_**

python3 -m venv env

source env/bin/activate

**_Установить зависимости из файла requirements.txt:_**

python3 -m pip install --upgrade pip

pip install -r requirements.txt

**_Выполнить миграции:_**

python3 manage.py migrate

**_Запустить проект:_**

python3 manage.py runserver

