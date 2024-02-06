# greystone-labs-challenge

## Prerequisites
1. Install [Visual Studio Code](https://code.visualstudio.com/)
2. Install [python3](https://www.python.org/downloads/). As of 02/02/2024, this repo is using ***Python 3.12.1***
3. Install [SQLite](https://marketplace.visualstudio.com/items?itemName=alexcvzz.vscode-sqlite) extension in the vscode marketplace

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

## Running tests
All tests are under the `/tests/` directory. Simply navigate to the root directory and run `pytests`

## Loan Amortization App
REST API for a Loan Amortization app using the python miniframework [FastAPI](https://fastapi.tiangolo.com/).


### The API should allow a client to,

- [x] Create a user
- [x] Create loan
- [x] Fetch loan schedule
- [x] Fetch loan summary for a specific month
- [x] Fetch all loans for a user
- [x] Share loan with another user

### A loan record should at least contain the following fields: 

- [x] Amount
- [x] Annual Interest Rate
- [x] Loan Term in months

### The loan schedule endpoint should return an array of length loan_term, consisting of:
```code
{
  Month: n
  Remaining balance: $xxxx,
  Monthly payment: $xxx
}
```

### The loan summary endpoint should accept a month number as a parameter and return:

- [x] Current principal balance at given month
- [x] The aggregate amount of principal already paid
- [x] The aggregate amount of interest already paid