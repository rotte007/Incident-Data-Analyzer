# cis6930fa24-project3
Data Engineering

**Name:** Rachana Rotte

## Project Description

This project involves building a web application using Flask that allows users to upload incident PDF files or provide URLs for Norman PD incident PDFs. The application extracts and processes the incident data to generate visualizations, including bar charts for the nature of incidents, time series graphs for incidents over time, and clustering visualizations based on incident locations and nature.

## How to Install
```
git clone https://github.com/rotte007/cis6930fa24-project3.git
cd cis6930fa24-project3
pip install pipenv (if not already installed)
pipenv install -e .
```

## How to Run
```
pipenv run python src/main.py

pipenv run python -m pytest -v
```
Open your web browser and navigate to:

```
http://127.0.0.1:5000/
```

![video](https://github.com/rotte007/cis6930fa24-project0/blob/main/resources/Video.gif)

## Example of Output

Example console output -> 
``` 
 * Serving Flask app 'main'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 264-523-139
127.0.0.1 - - [07/Dec/2024 18:08:29] "GET / HTTP/1.1" 200 -
127.0.0.1 - - [07/Dec/2024 18:08:29] "GET /static/style.css HTTP/1.1" 304 -
```

## Functions

### `main.py`

