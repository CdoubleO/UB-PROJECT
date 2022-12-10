# UB-PROJECT

## Requirements to run the project in a Python virtual enviroment can be found in the requirements.txt file

1. Clone Project

```sh
git clone https://github.com/CdoubleO/UB-PROJECT.git
```
2. Create virtual Enviroment

```sh 
python3 -m venv venv
```

3. Activate venv

```sh
source {path to project folder}/venv/bin/activate
```

4. Install packages

```sh
pip install -r requirements.txt
```
5. Create .env file in project folder

    * DATABASE_HOSTNAME=
    * DATABASE_PORT=
    * DATABASE_PASSWORD=
    * DATABASE_NAME=
    * DATABASE_USERNAME=
    * SECRET_KEY=
    * ALGORITHM=
    * ACCESS_TOKEN_EXPIRE_MINUTES=

6. Run server to test api\n

```sh
uvicorn app.main:app --reload
```