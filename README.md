# greystone-labs-challenge

## Prerequisites
1. Install [python3](https://www.python.org/downloads/). As of 02/02/2024, this repo is using ***Python 3.12.1***

## Installation
1. Clone the repository
    ```
    git clone https://github.com/MiSTERSPOONS/greystone-labs-challenge.git
    ```

2. Install dependencies
    ```
    pip3 -r requirements.txt
    ```

## Start the server
This server using the [FastAPI](https://fastapi.tiangolo.com/) python framework for creating REST APIs
1. The following command will run the Uvicorn server on http://127.0.0.1:8000
    ```
    uvicorn main:app --reload
    ```
    - `main`: the file main.py (the Python "module").
    - `app`: the object created inside of main.py with the line app = FastAPI().
    - `--reload`: make the server restart after code changes. Only do this for development.