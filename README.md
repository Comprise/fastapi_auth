- Python 3.8.10
- MySQL >= 4.1


Create a Migration Script: `alembic revision --autogenerate -m 'name'`  
Running Migration: `alembic upgrade head`

Running: `uvicorn main:app --reload --host 127.0.0.1 --port 8000`