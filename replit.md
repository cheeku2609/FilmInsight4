# Movie Rating Analysis Dashboard

## Overview

This is a Streamlit-based movie data analytics dashboard that provides comprehensive insights into movie ratings, runtime distributions, and genre analysis. The application processes movie datasets (including cast and crew information) to create interactive visualizations and statistical summaries. Users can filter data by release year, rating range, runtime, and genres to explore different aspects of movie data through dynamic charts and metrics.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Framework**: Streamlit web application framework
- **Styling**: Custom CSS with dark theme implementation using linear gradients and styled metric cards
- **Layout**: Wide layout with expandable sidebar for filters and controls
- **Page Configuration**: Centralized configuration with movie-themed icons and branding

### Data Processing Architecture
- **Modular Design**: Separated into three main components:
  - `DataProcessor`: Handles data loading, cleaning, and preprocessing
  - `MovieVisualizations`: Manages all chart generation and visual components
  - `MovieUtils`: Provides utility functions for data filtering and genre management
- **Data Pipeline**: Merges movie and credits datasets, processes JSON-like fields (genres, cast, crew), handles missing values, and extracts temporal features
- **Data Validation**: Robust error handling for date parsing and numeric conversions with fallback mechanisms

### Visualization Architecture
- **Charting Library**: Plotly with both Express and Graph Objects for different visualization needs
- **Theme Consistency**: Dark template with custom color palette across all visualizations
- **Chart Types**: Histograms, subplots, and interactive filtering capabilities
- **Performance**: Efficient data processing with pandas and numpy for large datasets

### Data Model
- **Core Entities**: Movies with attributes including ratings, runtime, release dates, budget, revenue, and popularity metrics
- **Relationships**: Movie-to-cast and movie-to-crew relationships through merged datasets
- **Derived Fields**: Calculated fields like release year and processed genre lists from JSON data
- **Filtering Schema**: Multi-dimensional filtering by year range, rating range, runtime, and genre selections

## External Dependencies

### Core Libraries
- **streamlit**: Web application framework for the dashboard interface
- **pandas**: Primary data manipulation and analysis library
- **plotly**: Interactive visualization library (both express and graph_objects modules)
- **numpy**: Numerical computing support for data processing
- **seaborn**: Statistical visualization enhancements

### Data Processing
- **json**: JSON parsing for nested movie metadata fields
- **ast**: Safe evaluation of string representations of Python literals
- **datetime**: Date and time processing for release date handling
- **collections.Counter**: Efficient counting operations for genre analysis

### Visualization Support
- **plotly.subplots**: Advanced subplot creation for complex visualizations
- **warnings**: Suppression of non-critical warnings for cleaner output

### Data Sources
- Movie datasets with fields: id, title, release_date, runtime, vote_average, vote_count, revenue, budget, popularity, genres, overview, tagline, keywords
- Credits dataset with cast and crew information linked via movie_id
- Expected JSON-formatted fields for genres, cast, crew, and keywords that require parsing