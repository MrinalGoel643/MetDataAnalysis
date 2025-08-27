# MetDataAnalysis
Bootcamp Final Project

## How to run
### Create your virtual environment
`python3 -m venv venv`
### Activate your virtual environment
`source venv/bin/activate`
### Install dependencies
`pip install -r requirements.txt`
### Run streamlit app
`streamlit run main.py`
### Run CLI
`python met_api.py`
The CLI will search for images that matches the keyword across selected departments (or all departments).
The CLI will display a list of departments to choose from (or press enter for all)
Then it will ask for a search query. It will then display a table of items that matches the query with some details.

