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

1. **Push to GitHub:**
   ```bash
   git add .
   git commit -m "Deploy movie dashboard"
   git push origin main
   ```

2. **Deploy on Streamlit Cloud:**
   - Go to https://share.streamlit.io/
   - Connect your GitHub repository
   - Set main file as: `app.py`
   - The app will automatically detect dependencies from `requirements.txt`

3. **Required Files (make sure these are in your repo root):**
   - `app.py`, `data_processor.py`, `visualizations.py`, `utils.py`
   - `tmdb_5000_movies.csv`, `tmdb_5000_credits.csv`
   - `requirements.txt`, `.streamlit/config.toml`

**Troubleshooting:**
- If deployment fails, check that CSV files are properly uploaded to GitHub
- Ensure all Python files are in the repository root
- Verify requirements.txt contains all dependencies

Created by Kritarth Karambelkar