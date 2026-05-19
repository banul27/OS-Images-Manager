# Cum sa rulezi:

python -m venv venv
venv\Scripts\python.exe -m pip install -r requirements.txt
venv\Scripts\python.exe manage.py migrate
venv\Scripts\python.exe manage.py runserver

(pe PowerShell `activate` da uneori eroare de permisiuni — folosesti direct python din venv)

!!! Docker Desktop trebuie sa fie pornit
