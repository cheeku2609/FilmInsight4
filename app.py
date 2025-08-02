import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import json
from datetime import datetime
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

from data_processor import DataProcessor
from visualizations import MovieVisualizations
from utils import MovieUtils

# Page configuration
st.set_page_config(
    page_title="🎬 Movie Rating Analysis Dashboard",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for dark theme and styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(90deg, #ff6b6b, #4ecdc4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2rem;
    }
    
    .metric-card {
        background-color: #1e2327;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #ff6b6b;
        margin: 0.5rem 0;
    }
    
    .section-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #4ecdc4;
        margin: 1rem 0;
        border-bottom: 2px solid #4ecdc4;
        padding-bottom: 0.5rem;
    }
    
    .filter-container {
        background-color: #1e2327;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load and process movie data"""
    try:
        # Try to load from uploaded files or local files
        movies_df = pd.read_csv('attached_assets/tmdb_5000_movies_1754127464330.csv')
        credits_df = pd.read_csv('attached_assets/tmdb_5000_credits_1754127464329.csv')
        
        processor = DataProcessor()
        return processor.process_data(movies_df, credits_df)
    except FileNotFoundError:
        st.error("Dataset files not found. Please ensure the TMDB dataset files are available.")
        return None

def main():
    # Header
    st.markdown('<h1 class="main-header">🎬 Movie Rating Analysis Dashboard</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #888;">A Data-Driven Exploration of the TMDB Movie Dataset</p>', unsafe_allow_html=True)
    
    # Load data
    df = load_data()
    if df is None:
        st.stop()
    
    # Initialize visualization class
    viz = MovieVisualizations(df)
    utils = MovieUtils(df)
    
    # Sidebar filters
    st.sidebar.markdown('<div class="section-header">🔍 Data Filters</div>', unsafe_allow_html=True)
    
    # Year range filter
    min_year = int(df['release_year'].min())
    max_year = int(df['release_year'].max())
    year_range = st.sidebar.slider(
        "Select Year Range",
        min_value=min_year,
        max_value=max_year,
        value=(min_year, max_year),
        step=1
    )
    
    # Rating filter
    rating_range = st.sidebar.slider(
        "Vote Average Range",
        min_value=0.0,
        max_value=10.0,
        value=(0.0, 10.0),
        step=0.1
    )
    
    # Runtime filter
    runtime_range = st.sidebar.slider(
        "Runtime (minutes)",
        min_value=0,
        max_value=int(df['runtime'].max()),
        value=(0, int(df['runtime'].max())),
        step=5
    )
    
    # Genre filter
    all_genres = utils.get_all_genres()
    selected_genres = st.sidebar.multiselect(
        "Select Genres",
        options=all_genres,
        default=all_genres[:5] if len(all_genres) > 5 else all_genres
    )
    
    # Apply filters
    filtered_df = utils.filter_data(df, year_range, rating_range, runtime_range, selected_genres)
    
    # Display filter summary
    st.sidebar.markdown("---")
    st.sidebar.metric("Total Movies", len(filtered_df))
    st.sidebar.metric("Average Rating", f"{filtered_df['vote_average'].mean():.2f}")
    st.sidebar.metric("Total Revenue", f"${filtered_df['revenue'].sum():,.0f}")
    
    # Main dashboard content
    if len(filtered_df) == 0:
        st.warning("No movies match the selected filters. Please adjust your criteria.")
        return
    
    # Overview metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Movies Analyzed",
            f"{len(filtered_df):,}",
            delta=f"{len(filtered_df) - len(df)} from total"
        )
    
    with col2:
        avg_rating = filtered_df['vote_average'].mean()
        st.metric(
            "Average Rating",
            f"{avg_rating:.2f}",
            delta=f"{avg_rating - df['vote_average'].mean():.2f}"
        )
    
    with col3:
        total_revenue = filtered_df['revenue'].sum()
        st.metric(
            "Total Revenue",
            f"${total_revenue/1e9:.1f}B",
            delta=f"${(total_revenue - df['revenue'].sum())/1e9:.1f}B"
        )
    
    with col4:
        avg_runtime = filtered_df['runtime'].mean()
        st.metric(
            "Avg Runtime",
            f"{avg_runtime:.0f} min",
            delta=f"{avg_runtime - df['runtime'].mean():.0f} min"
        )
    
    st.markdown("---")
    
    # Analysis sections
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Overview Analysis", 
        "🎭 Genre Analysis", 
        "📈 Trends & Correlations", 
        "🏆 Top Movies", 
        "💰 Financial Analysis"
    ])
    
    with tab1:
        st.markdown('<div class="section-header">📊 Movie Dataset Overview</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Rating distribution
            fig_rating = viz.plot_rating_distribution(filtered_df)
            st.plotly_chart(fig_rating, use_container_width=True)
        
        with col2:
            # Runtime distribution
            fig_runtime = viz.plot_runtime_distribution(filtered_df)
            st.plotly_chart(fig_runtime, use_container_width=True)
        
        # Year-wise analysis
        st.markdown('<div class="section-header">🗓️ Year-wise Analysis</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Movies per year
            fig_year_count = viz.plot_movies_per_year(filtered_df)
            st.plotly_chart(fig_year_count, use_container_width=True)
        
        with col2:
            # Average rating by year
            fig_year_rating = viz.plot_rating_by_year(filtered_df)
            st.plotly_chart(fig_year_rating, use_container_width=True)
    
    with tab2:
        st.markdown('<div class="section-header">🎭 Genre Analysis</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Genre distribution
            fig_genre_dist = viz.plot_genre_distribution(filtered_df)
            st.plotly_chart(fig_genre_dist, use_container_width=True)
        
        with col2:
            # Average rating by genre
            fig_genre_rating = viz.plot_genre_ratings(filtered_df)
            st.plotly_chart(fig_genre_rating, use_container_width=True)
        
        # Genre popularity over time
        fig_genre_time = viz.plot_genre_trends(filtered_df)
        st.plotly_chart(fig_genre_time, use_container_width=True)
    
    with tab3:
        st.markdown('<div class="section-header">📈 Correlations & Trends</div>', unsafe_allow_html=True)
        
        # Correlation heatmap
        fig_corr = viz.plot_correlation_heatmap(filtered_df)
        st.plotly_chart(fig_corr, use_container_width=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Runtime vs Rating scatter
            fig_runtime_rating = viz.plot_runtime_vs_rating(filtered_df)
            st.plotly_chart(fig_runtime_rating, use_container_width=True)
        
        with col2:
            # Vote count vs Rating
            fig_votes_rating = viz.plot_votes_vs_rating(filtered_df)
            st.plotly_chart(fig_votes_rating, use_container_width=True)
    
    with tab4:
        st.markdown('<div class="section-header">🏆 Top Movies Analysis</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Top rated movies
            st.subheader("⭐ Highest Rated Movies")
            top_rated = utils.get_top_rated_movies(filtered_df, 10)
            fig_top_rated = viz.plot_top_movies_bar(top_rated, 'vote_average', 'Top Rated Movies')
            st.plotly_chart(fig_top_rated, use_container_width=True)
            
            # Display table
            st.dataframe(
                top_rated[['title', 'vote_average', 'vote_count', 'release_year']].head(),
                use_container_width=True
            )
        
        with col2:
            # Longest movies
            st.subheader("⏱️ Longest Movies")
            longest_movies = utils.get_longest_movies(filtered_df, 10)
            fig_longest = viz.plot_top_movies_bar(longest_movies, 'runtime', 'Longest Movies (Runtime)')
            st.plotly_chart(fig_longest, use_container_width=True)
            
            # Display table
            st.dataframe(
                longest_movies[['title', 'runtime', 'vote_average', 'release_year']].head(),
                use_container_width=True
            )
        
        # Movies with runtime >= 180 minutes
        st.subheader("🎬 Epic Movies (Runtime ≥ 180 minutes)")
        long_movies = utils.get_movies_by_runtime(filtered_df, min_runtime=180)
        
        if len(long_movies) > 0:
            fig_long_movies = viz.plot_long_movies(long_movies)
            st.plotly_chart(fig_long_movies, use_container_width=True)
            
            st.dataframe(
                long_movies[['title', 'runtime', 'vote_average', 'release_year']].head(10),
                use_container_width=True
            )
        else:
            st.info("No movies found with runtime ≥ 180 minutes in the selected filters.")
    
    with tab5:
        st.markdown('<div class="section-header">💰 Financial Analysis</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Budget vs Revenue scatter
            fig_budget_revenue = viz.plot_budget_vs_revenue(filtered_df)
            st.plotly_chart(fig_budget_revenue, use_container_width=True)
        
        with col2:
            # Profitability analysis
            fig_profit = viz.plot_profit_analysis(filtered_df)
            st.plotly_chart(fig_profit, use_container_width=True)
        
        # Top grossing movies
        st.subheader("💰 Top Grossing Movies")
        top_grossing = utils.get_top_grossing_movies(filtered_df, 10)
        
        if len(top_grossing) > 0:
            fig_grossing = viz.plot_top_movies_bar(top_grossing, 'revenue', 'Top Grossing Movies')
            st.plotly_chart(fig_grossing, use_container_width=True)
            
            st.dataframe(
                top_grossing[['title', 'revenue', 'budget', 'vote_average', 'release_year']].head(),
                use_container_width=True
            )
        else:
            st.info("No revenue data available for the selected filters.")
    
    # Footer
    st.markdown("---")
    st.markdown(
        '<p style="text-align: center; color: #888;">Data source: TMDB 5000 Movie Dataset | '
        'Built with Streamlit & Plotly</p>',
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
