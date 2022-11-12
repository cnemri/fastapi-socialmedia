# FastAPI Social Media App Example
## Introduction
This is an example of a social media application capturing the following entities
- users
- posts 
- votes

The topics covered in this example include
- FastAPI
- Databases
- Python + Raw SQL
- ORMs
- Pydantic
- User authentication (JWT tokens)
- Relationships
- Database migration with Alembic
- CORS
- Docker
- Testing
- CI/CD
## Run local
### Install dependencies
1. Clone repo
```
git clone https://github.com/cnemri/fastapi-socialmedia
```
2. Create virtual environment
```
python3 -m venv venv
```
3. Activate virtual environment
```
source venv/bin/activate
```
4. Install requirements
```
pip3 install -r requirements.txt
```
### Run server
```
uvicorn app.main:app --reload
```
### Run test
```
pytest -v -s
```
## Run with docker
### Dev environment
```
docker-compose up -f docker-compose-dev.yml
```
### Prod environment
```
docker-compose up -f docker-compose-prod.yml
```
## API Documentation (provided by Swagger UI)
```
http://127.0.0.1:8000/docs
```