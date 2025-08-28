---
title: Met Data Analysis
emoji: 📊
colorFrom: green
colorTo: blue
sdk: streamlit
sdk_version: 1.48.1
app_file: main.py
pinned: false
---

# MetDataAnalysis
Bootcamp Final Project

Browse and analyze Met art collection API
![The Met Logo](https://cdn.sanity.io/images/cctd4ker/production/1357b570f8ec477e8bc69bf74f56b43877e72e58-720x466.gif?w=360&q=75&fit=clip&auto=format)

API document: https://huggingface.co/spaces/mg643/MetDataAnalysis

## How to run locally
### Create your virtual environment
`python3 -m venv venv`
### Activate your virtual environment
`source venv/bin/activate`
### Install dependencies
`pip install -r requirements.txt`
### Run streamlit app
`streamlit run main.py`

The application has 3 tabs:
1. Random - Display 3 random images from the Met collection
2. Search & Browse - searches the image collection based on query, 
display a table of select results from across the departments, and select one for more details
3. Dept Analytics - a chart of matching images by department 

### Run CLI
`python met_api.py`

The CLI will search for images that matches the keyword across selected departments (or all departments).
The CLI will display a list of departments to choose from (or press enter for all)
Then it will ask for a search query. It will then display a table of items that matches the query with some details.

### Specifics 
- **Python**: 3.9.6
- Deployed as a [Hugging Face Space](https://huggingface.co/spaces/mg643/MetDataAnalysis) and automatically synced with GitHub Actions.

  ![GIF](end.jpg)