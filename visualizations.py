import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
import seaborn as sns
from collections import Counter

class MovieVisualizations:
    """Class to handle all movie data visualizations"""
    
    def __init__(self, df):
        self.df = df
        self.color_palette = [
            '#ff6b6b', '#4ecdc4', '#45b7d1', '#f9ca24', 
            '#f0932b', '#eb4d4b', '#6ab04c', '#be2edd'
        ]
        self.template = 'plotly_dark'
    
    def plot_rating_distribution(self, df):
        """Plot distribution of movie ratings"""
        fig = px.histogram(
            df, 
            x='vote_average', 
            nbins=30,
            title='Distribution of Movie Ratings',
            labels={'vote_average': 'Vote Average', 'count': 'Number of Movies'},
            color_discrete_sequence=['#ff6b6b']
        )
        
        fig.update_layout(
            template=self.template,
            title_x=0.5,
            showlegend=False
        )
        
        return fig
    
    def plot_runtime_distribution(self, df):
        """Plot distribution of movie runtimes"""
        fig = px.histogram(
            df, 
            x='runtime', 
            nbins=30,
            title='Distribution of Movie Runtimes',
            labels={'runtime': 'Runtime (minutes)', 'count': 'Number of Movies'},
            color_discrete_sequence=['#4ecdc4']
        )
        
        fig.update_layout(
            template=self.template,
            title_x=0.5,
            showlegend=False
        )
        
        return fig
    
    def plot_movies_per_year(self, df):
        """Plot number of movies released per year"""
        yearly_counts = df.groupby('release_year').size().reset_index(name='count')
        
        fig = px.line(
            yearly_counts,
            x='release_year',
            y='count',
            title='Number of Movies Released Per Year',
            labels={'release_year': 'Year', 'count': 'Number of Movies'},
            line_shape='spline'
        )
        
        fig.update_traces(line_color='#45b7d1', line_width=3)
        fig.update_layout(
            template=self.template,
            title_x=0.5
        )
        
        return fig
    
    def plot_rating_by_year(self, df):
        """Plot average rating by year"""
        yearly_ratings = df.groupby('release_year')['vote_average'].mean().reset_index()
        
        fig = px.line(
            yearly_ratings,
            x='release_year',
            y='vote_average',
            title='Average Movie Rating by Year',
            labels={'release_year': 'Year', 'vote_average': 'Average Rating'},
            line_shape='spline'
        )
        
        fig.update_traces(line_color='#f9ca24', line_width=3)
        fig.update_layout(
            template=self.template,
            title_x=0.5
        )
        
        return fig
    
    def plot_genre_distribution(self, df):
        """Plot distribution of genres"""
        if 'genre_list' not in df.columns:
            return self._empty_plot("Genre data not available")
        
        # Count all genres
        all_genres = []
        for genres in df['genre_list']:
            all_genres.extend(genres)
        
        genre_counts = Counter(all_genres)
        top_genres = dict(genre_counts.most_common(15))
        
        genre_df = pd.DataFrame(list(top_genres.items()), columns=['Genre', 'Count'])
        
        fig = px.bar(
            genre_df,
            x='Count',
            y='Genre',
            orientation='h',
            title='Distribution of Movie Genres',
            labels={'Count': 'Number of Movies', 'Genre': 'Genre'},
            color='Count',
            color_continuous_scale='Viridis'
        )
        
        fig.update_layout(
            template=self.template,
            title_x=0.5,
            yaxis={'categoryorder': 'total ascending'}
        )
        
        return fig
    
    def plot_genre_ratings(self, df):
        """Plot average ratings by genre"""
        if 'genre_list' not in df.columns:
            return self._empty_plot("Genre data not available")
        
        # Expand genres for analysis
        genre_data = []
        for _, row in df.iterrows():
            for genre in row['genre_list']:
                genre_data.append({
                    'genre': genre,
                    'vote_average': row['vote_average'],
                    'vote_count': row['vote_count']
                })
        
        genre_df = pd.DataFrame(genre_data)
        
        # Calculate weighted average ratings
        genre_ratings = genre_df.groupby('genre').agg({
            'vote_average': 'mean',
            'vote_count': 'sum'
        }).reset_index()
        
        # Filter genres with at least 10 movies
        genre_ratings = genre_ratings[genre_ratings['vote_count'] >= 10]
        genre_ratings = genre_ratings.sort_values('vote_average', ascending=True)
        
        fig = px.bar(
            genre_ratings,
            x='vote_average',
            y='genre',
            orientation='h',
            title='Average Rating by Genre',
            labels={'vote_average': 'Average Rating', 'genre': 'Genre'},
            color='vote_average',
            color_continuous_scale='RdYlGn'
        )
        
        fig.update_layout(
            template=self.template,
            title_x=0.5,
            yaxis={'categoryorder': 'total ascending'}
        )
        
        return fig
    
    def plot_genre_trends(self, df):
        """Plot genre popularity trends over time"""
        if 'genre_list' not in df.columns:
            return self._empty_plot("Genre data not available")
        
        # Get top 6 genres
        all_genres = []
        for genres in df['genre_list']:
            all_genres.extend(genres)
        
        top_genres = [genre for genre, _ in Counter(all_genres).most_common(6)]
        
        # Prepare data for time series
        trend_data = []
        for year in sorted(df['release_year'].unique()):
            year_movies = df[df['release_year'] == year]
            for genre in top_genres:
                count = sum(1 for genres in year_movies['genre_list'] if genre in genres)
                trend_data.append({
                    'year': year,
                    'genre': genre,
                    'count': count
                })
        
        trend_df = pd.DataFrame(trend_data)
        
        fig = px.line(
            trend_df,
            x='year',
            y='count',
            color='genre',
            title='Genre Popularity Trends Over Time',
            labels={'year': 'Year', 'count': 'Number of Movies', 'genre': 'Genre'}
        )
        
        fig.update_layout(
            template=self.template,
            title_x=0.5
        )
        
        return fig
    
    def plot_correlation_heatmap(self, df):
        """Plot correlation heatmap of numeric variables"""
        numeric_cols = ['vote_average', 'vote_count', 'runtime', 'budget', 'revenue', 'popularity']
        available_cols = [col for col in numeric_cols if col in df.columns]
        
        if len(available_cols) < 2:
            return self._empty_plot("Insufficient numeric data for correlation")
        
        corr_matrix = df[available_cols].corr()
        
        fig = go.Figure(data=go.Heatmap(
            z=corr_matrix.values,
            x=corr_matrix.columns,
            y=corr_matrix.columns,
            colorscale='RdBu',
            zmid=0,
            text=np.around(corr_matrix.values, decimals=2),
            texttemplate='%{text}',
            textfont={"size": 10},
            hoverongaps=False
        ))
        
        fig.update_layout(
            template=self.template,
            title='Correlation Matrix of Movie Features',
            title_x=0.5,
            width=600,
            height=500
        )
        
        return fig
    
    def plot_runtime_vs_rating(self, df):
        """Plot runtime vs rating scatter plot"""
        fig = px.scatter(
            df,
            x='runtime',
            y='vote_average',
            title='Runtime vs Rating',
            labels={'runtime': 'Runtime (minutes)', 'vote_average': 'Vote Average'},
            opacity=0.6,
            color='vote_count',
            size='popularity',
            hover_data=['title'],
            color_continuous_scale='Viridis'
        )
        
        fig.update_layout(
            template=self.template,
            title_x=0.5
        )
        
        return fig
    
    def plot_votes_vs_rating(self, df):
        """Plot vote count vs rating scatter plot"""
        fig = px.scatter(
            df,
            x='vote_count',
            y='vote_average',
            title='Vote Count vs Rating',
            labels={'vote_count': 'Vote Count', 'vote_average': 'Vote Average'},
            opacity=0.6,
            color='popularity',
            size='revenue',
            hover_data=['title'],
            color_continuous_scale='Plasma'
        )
        
        fig.update_layout(
            template=self.template,
            title_x=0.5
        )
        
        return fig
    
    def plot_top_movies_bar(self, df, metric_col, title):
        """Generic function to plot top movies bar chart"""
        df_sorted = df.head(10)
        
        fig = px.bar(
            df_sorted,
            x=metric_col,
            y='title',
            orientation='h',
            title=title,
            labels={metric_col: metric_col.replace('_', ' ').title(), 'title': 'Movie'},
            color=metric_col,
            color_continuous_scale='Viridis'
        )
        
        fig.update_layout(
            template=self.template,
            title_x=0.5,
            yaxis={'categoryorder': 'total ascending'}
        )
        
        return fig
    
    def plot_long_movies(self, df):
        """Plot movies with runtime >= 180 minutes"""
        fig = px.bar(
            df.head(15),
            x='runtime',
            y='title',
            orientation='h',
            title='Movies with Runtime ≥ 180 Minutes',
            labels={'runtime': 'Runtime (minutes)', 'title': 'Movie'},
            color='vote_average',
            color_continuous_scale='RdYlGn'
        )
        
        fig.update_layout(
            template=self.template,
            title_x=0.5,
            yaxis={'categoryorder': 'total ascending'}
        )
        
        return fig
    
    def plot_budget_vs_revenue(self, df):
        """Plot budget vs revenue scatter plot"""
        # Filter out zero values for better visualization
        plot_df = df[(df['budget'] > 0) & (df['revenue'] > 0)]
        
        fig = px.scatter(
            plot_df,
            x='budget',
            y='revenue',
            title='Budget vs Revenue',
            labels={'budget': 'Budget ($)', 'revenue': 'Revenue ($)'},
            opacity=0.6,
            color='vote_average',
            size='popularity',
            hover_data=['title'],
            color_continuous_scale='RdYlGn'
        )
        
        # Add diagonal line for break-even
        max_val = max(plot_df['budget'].max(), plot_df['revenue'].max())
        fig.add_trace(go.Scatter(
            x=[0, max_val],
            y=[0, max_val],
            mode='lines',
            name='Break-even line',
            line=dict(color='red', dash='dash')
        ))
        
        fig.update_layout(
            template=self.template,
            title_x=0.5
        )
        
        return fig
    
    def plot_profit_analysis(self, df):
        """Plot profit analysis"""
        if 'profit' not in df.columns:
            return self._empty_plot("Profit data not available")
        
        # Filter movies with budget and revenue data
        profit_df = df[(df['budget'] > 0) & (df['revenue'] > 0)].copy()
        profit_df = profit_df.sort_values('profit', ascending=False).head(15)
        
        fig = px.bar(
            profit_df,
            x='profit',
            y='title',
            orientation='h',
            title='Most Profitable Movies',
            labels={'profit': 'Profit ($)', 'title': 'Movie'},
            color='profit',
            color_continuous_scale='RdYlGn'
        )
        
        fig.update_layout(
            template=self.template,
            title_x=0.5,
            yaxis={'categoryorder': 'total ascending'}
        )
        
        return fig
    
    def _empty_plot(self, message):
        """Create an empty plot with a message"""
        fig = go.Figure()
        fig.add_annotation(
            text=message,
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            showarrow=False,
            font=dict(size=16, color="gray")
        )
        fig.update_layout(
            template=self.template,
            xaxis=dict(visible=False),
            yaxis=dict(visible=False)
        )
        return fig
