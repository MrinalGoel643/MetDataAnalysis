# Design document for MetDataAnalysis

## Application Requirement Summary:
1) an API "layer" and a CLI for the API
2) StreamLit app (that can run locally and in HuggingFace)
3) Visual element
4) Data analysis

## Application Components
- [ ] METrics StreamLit App (that runs locally and in HuggingFace)
    - [ ] Display a dataframe table of items with image and metadata
    - [ ] Search and display matching items in table
    - [ ] data analysis visual (# by department, period, etc...)
    - [ ] Nice visual layout and design
- [ ] API wrapper function
    - [ ] CLI runner for api search function
    - [ ] (optional) Local cache of recent items (serialized json)

## Additional Tasks
- [ ] HuggingFace Space/Repo setup
- [x] GitHub Repo setup
- [ ] Everyone make a branch and commit
- [ ] Everyone do a PR