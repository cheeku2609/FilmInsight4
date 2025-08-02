import pandas as pd
import numpy as np
from collections import Counter

class MovieUtils:
    """Utility functions for movie data analysis"""
    
    def __init__(self, df):
        self.df = df
    
    def get_all_genres(self):
        """Get all unique genres from the dataset"""
        if 'genre_list' not in self.df.columns:
            return []
        
        all_genres = []
        for genres in self.df['genre_list']:
            if isinstance(genres, list):
                all_genres.extend(genres)
        
        return sorted(list(set(all_genres)))
    
    def filter_data(self, df, year_range, rating_range, runtime_range, selected_genres):
        """Filter dataframe based on user selections"""
        filtered_df = df.copy()
        
        # Year filter
        filtered_df = filtered_df[
            (filtered_df['release_year'] >= year_range[0]) & 
            (filtered_df['release_year'] <= year_range[1])
        ]
        
        # Rating filter
        filtered_df = filtered_df[
            (filtered_df['vote_average'] >= rating_range[0]) & 
            (filtered_df['vote_average'] <= rating_range[1])
        ]
        
        # Runtime filter
        filtered_df = filtered_df[
            (filtered_df['runtime'] >= runtime_range[0]) & 
            (filtered_df['runtime'] <= runtime_range[1])
        ]
        
        # Genre filter
        if selected_genres and 'genre_list' in filtered_df.columns:
            def has_selected_genre(genres):
                if not isinstance(genres, list):
                    return False
                return any(genre in selected_genres for genre in genres)
            
            filtered_df = filtered_df[filtered_df['genre_list'].apply(has_selected_genre)]
        
        return filtered_df
    
    def get_top_rated_movies(self, df, n=10):
        """Get top rated movies with minimum vote count"""
        # Filter movies with at least 100 votes for reliability
        qualified_movies = df[df['vote_count'] >= 100]
        return qualified_movies.nlargest(n, 'vote_average')
    
    def get_longest_movies(self, df, n=10):
        """Get longest movies by runtime"""
        return df.nlargest(n, 'runtime')
    
    def get_movies_by_runtime(self, df, min_runtime=180):
        """Get movies with runtime >= specified minutes"""
        long_movies = df[df['runtime'] >= min_runtime]
        return long_movies.sort_values('runtime', ascending=False)
    
    def get_top_grossing_movies(self, df, n=10):
        """Get top grossing movies"""
        # Filter movies with revenue data
        revenue_movies = df[df['revenue'] > 0]
        return revenue_movies.nlargest(n, 'revenue')
    
    def get_movies_by_year(self, df, year):
        """Get all movies from a specific year"""
        return df[df['release_year'] == year]
    
    def get_movies_by_genre(self, df, genre):
        """Get movies of a specific genre"""
        if 'genre_list' not in df.columns:
            return pd.DataFrame()
        
        return df[df['genre_list'].apply(lambda x: genre in x if isinstance(x, list) else False)]
    
    def get_movie_statistics(self, df):
        """Get comprehensive statistics about the dataset"""
        stats = {
            'total_movies': len(df),
            'avg_rating': df['vote_average'].mean(),
            'avg_runtime': df['runtime'].mean(),
            'total_revenue': df['revenue'].sum(),
            'total_budget': df['budget'].sum(),
            'year_range': (df['release_year'].min(), df['release_year'].max()),
            'top_genre': self._get_most_common_genre(df),
            'avg_votes': df['vote_count'].mean()
        }
        
        return stats
    
    def _get_most_common_genre(self, df):
        """Get the most common genre in the dataset"""
        if 'genre_list' not in df.columns:
            return 'Unknown'
        
        all_genres = []
        for genres in df['genre_list']:
            if isinstance(genres, list):
                all_genres.extend(genres)
        
        if not all_genres:
            return 'Unknown'
        
        return Counter(all_genres).most_common(1)[0][0]
    
    def search_movies(self, df, query):
        """Search movies by title"""
        return df[df['title'].str.contains(query, case=False, na=False)]
    
    def get_director_movies(self, df, director):
        """Get movies by a specific director"""
        if 'director' not in df.columns:
            return pd.DataFrame()
        
        return df[df['director'].str.contains(director, case=False, na=False)]
    
    def get_decade_analysis(self, df):
        """Analyze movies by decade"""
        df = df.copy()
        df['decade'] = (df['release_year'] // 10) * 10
        
        decade_stats = df.groupby('decade').agg({
            'movie_id': 'count',
            'vote_average': 'mean',
            'runtime': 'mean',
            'revenue': 'sum',
            'budget': 'sum'
        }).round(2)
        
        decade_stats.columns = ['Movie Count', 'Avg Rating', 'Avg Runtime', 'Total Revenue', 'Total Budget']
        
        return decade_stats
    
    def get_rating_distribution(self, df):
        """Get distribution of movies by rating categories"""
        if 'rating_category' not in df.columns:
            return pd.Series()
        
        return df['rating_category'].value_counts()
    
    def calculate_success_metrics(self, df):
        """Calculate various success metrics"""
        metrics = {}
        
        if 'profit' in df.columns:
            profitable_movies = df[df['profit'] > 0]
            metrics['profitability_rate'] = len(profitable_movies) / len(df) * 100
            metrics['avg_profit'] = df['profit'].mean()
        
        if 'roi' in df.columns:
            metrics['avg_roi'] = df['roi'].mean()
        
        metrics['high_rated_percentage'] = len(df[df['vote_average'] >= 7]) / len(df) * 100
        metrics['blockbuster_percentage'] = len(df[df['budget'] >= 100000000]) / len(df) * 100
        
        return metrics
