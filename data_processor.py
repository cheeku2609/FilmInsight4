import pandas as pd
import numpy as np
import json
import ast
from datetime import datetime

class DataProcessor:
    """Class to handle data loading and preprocessing"""
    
    def __init__(self):
        pass
    
    def process_data(self, movies_df, credits_df):
        """Process and clean the movie dataset"""
        
        # Merge datasets
        df = movies_df.merge(credits_df, left_on='id', right_on='movie_id', how='inner')
        
        # Rename columns for clarity
        df = df.rename(columns={'id': 'movie_id', 'title_x': 'title'})
        
        # Select relevant columns
        analysis_columns = [
            'movie_id', 'title', 'release_date', 'runtime', 'vote_average', 
            'vote_count', 'revenue', 'budget', 'popularity', 'genres', 
            'cast', 'crew', 'overview', 'tagline', 'keywords'
        ]
        
        # Keep only existing columns
        existing_columns = [col for col in analysis_columns if col in df.columns]
        df = df[existing_columns]
        
        # Convert release_date and extract year
        df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')
        df['release_year'] = df['release_date'].dt.year
        
        # Clean numeric columns
        numeric_columns = ['runtime', 'vote_average', 'vote_count', 'revenue', 'budget', 'popularity']
        for col in numeric_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Handle missing values
        df = self._handle_missing_values(df)
        
        # Process genres
        df = self._process_genres(df)
        
        # Process cast and crew if available
        if 'cast' in df.columns:
            df = self._process_cast(df)
        
        if 'crew' in df.columns:
            df = self._process_crew(df)
        
        # Calculate additional metrics
        df = self._calculate_metrics(df)
        
        # Filter out invalid data
        df = self._filter_invalid_data(df)
        
        return df
    
    def _handle_missing_values(self, df):
        """Handle missing values in the dataset"""
        
        # Fill missing numeric values
        numeric_columns = ['runtime', 'vote_average', 'vote_count', 'revenue', 'budget', 'popularity']
        for col in numeric_columns:
            if col in df.columns:
                df[col] = df[col].fillna(0)
        
        # Fill missing text values
        text_columns = ['overview', 'tagline']
        for col in text_columns:
            if col in df.columns:
                df[col] = df[col].fillna('')
        
        # Drop rows with missing essential data
        essential_columns = ['title', 'release_year']
        df = df.dropna(subset=essential_columns)
        
        return df
    
    def _process_genres(self, df):
        """Process genres column"""
        if 'genres' not in df.columns:
            return df
        
        def extract_genres(genre_str):
            try:
                if pd.isna(genre_str) or genre_str == '':
                    return []
                
                # Parse JSON string
                genres = ast.literal_eval(genre_str)
                return [genre['name'] for genre in genres]
            except:
                return []
        
        df['genre_list'] = df['genres'].apply(extract_genres)
        df['primary_genre'] = df['genre_list'].apply(lambda x: x[0] if x else 'Unknown')
        df['genre_count'] = df['genre_list'].apply(len)
        
        return df
    
    def _process_cast(self, df):
        """Process cast column"""
        def extract_main_cast(cast_str, num_actors=5):
            try:
                if pd.isna(cast_str) or cast_str == '':
                    return []
                
                cast = ast.literal_eval(cast_str)
                return [actor['name'] for actor in cast[:num_actors]]
            except:
                return []
        
        df['main_cast'] = df['cast'].apply(extract_main_cast)
        df['cast_size'] = df['main_cast'].apply(len)
        
        return df
    
    def _process_crew(self, df):
        """Process crew column to extract director"""
        def extract_director(crew_str):
            try:
                if pd.isna(crew_str) or crew_str == '':
                    return 'Unknown'
                
                crew = ast.literal_eval(crew_str)
                for person in crew:
                    if person.get('job') == 'Director':
                        return person['name']
                return 'Unknown'
            except:
                return 'Unknown'
        
        df['director'] = df['crew'].apply(extract_director)
        
        return df
    
    def _calculate_metrics(self, df):
        """Calculate additional metrics"""
        
        # Profit calculation
        df['profit'] = df['revenue'] - df['budget']
        
        # ROI calculation (avoid division by zero)
        df['roi'] = np.where(df['budget'] > 0, (df['profit'] / df['budget']) * 100, 0)
        
        # Success score (combination of rating and popularity)
        df['success_score'] = (df['vote_average'] * 0.7) + (np.log1p(df['popularity']) * 0.3)
        
        # Rating category
        df['rating_category'] = pd.cut(
            df['vote_average'], 
            bins=[0, 4, 6, 8, 10], 
            labels=['Poor', 'Average', 'Good', 'Excellent']
        )
        
        # Runtime category
        df['runtime_category'] = pd.cut(
            df['runtime'], 
            bins=[0, 90, 120, 180, float('inf')], 
            labels=['Short', 'Medium', 'Long', 'Epic']
        )
        
        # Budget category
        df['budget_category'] = pd.cut(
            df['budget'], 
            bins=[0, 1e6, 10e6, 50e6, float('inf')], 
            labels=['Low', 'Medium', 'High', 'Blockbuster']
        )
        
        return df
    
    def _filter_invalid_data(self, df):
        """Filter out invalid or unrealistic data"""
        
        # Remove movies with invalid years
        current_year = datetime.now().year
        df = df[(df['release_year'] >= 1900) & (df['release_year'] <= current_year)]
        
        # Remove movies with unrealistic runtime
        df = df[(df['runtime'] >= 10) & (df['runtime'] <= 500)]
        
        # Remove movies with invalid ratings
        df = df[(df['vote_average'] >= 0) & (df['vote_average'] <= 10)]
        
        # Reset index
        df = df.reset_index(drop=True)
        
        return df
