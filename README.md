# Movie Rating Analysis Dashboard

An interactive Streamlit dashboard for analyzing movie ratings, genres, and trends using the TMDB dataset.

## Features

- **Overview Analysis**: Movie rating distributions and year-wise statistics
- **Genre Analysis**: Genre popularity and rating trends
- **Timeline Trends**: Movie production and rating patterns over time
- **Top Movies**: Highest-rated movies with clean text displays
- **Financial Analysis**: Budget vs revenue insights

## Files Required for Deployment

Make sure these files are in your repository root:
- `app.py` - Main Streamlit application
- `data_processor.py` - Data processing module
- `visualizations.py` - Chart generation module
- `utils.py` - Utility functions
- `tmdb_5000_movies.csv` - Movie dataset
- `tmdb_5000_credits.csv` - Credits dataset
- `requirements.txt` - Python dependencies

## Local Setup

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deployment on Streamlit Cloud

1. Push your project to GitHub
2. Connect to Streamlit Cloud
3. Deploy from your repository

Created by Kritarth Karambelkar