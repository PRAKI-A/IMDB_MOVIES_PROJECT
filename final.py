

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("🎬 Movie Dataset Explorer")

# Load dataset
df = pd.read_csv("imdb_miniproject.csv")
df.columns = df.columns.str.strip().str.lower()
df.rename(columns={'title': 'Title', 'rating': 'Rating', 'voting': 'Votes', 'duration': 'Duration', 'genre': 'Genre'}, inplace=True)

# Genre multiselect
unique_genres = df['Genre'].unique()
selected_genres = st.sidebar.multiselect(
    "Select Genre(s)",
    options=unique_genres,
    default=unique_genres,
    key="genre_selector"  # 👈 Optional but safe to add
)

st.sidebar.header("Filters")
min_votes = st.sidebar.slider(
    "Minimum Votes",
    min_value=int(df['Votes'].min()),
    max_value=int(df['Votes'].max()),
    value=1000,
    key="min_votes_slider"  # 👈 Add this line
)


min_duration = st.sidebar.slider(
    "Minimum Duration",
    min_value=0,
    max_value=int(df['Duration'].max()),
    value=120,
    key="min_duration_slider"
)

min_rating = st.sidebar.slider(
    "Minimum Rating",
    min_value=float(df['Rating'].min()),
    max_value=float(df['Rating'].max()),
    value=float(df['Rating'].min()),
    step=0.5,
    key="min_rating_slider"
)


# Apply filters
filtered_df = df[(df['Genre'].isin(selected_genres))& (df['Votes'] >= min_votes)  & (df['Duration']>= min_duration)& (df['Rating']>= min_rating)]


# 1. Top 10 Movies
st.subheader("🎖 Top 10 Movies by Rating and Votes")
top_movies = filtered_df.sort_values(by=['Rating', 'Votes'], ascending=False).head(10)
st.dataframe(top_movies[['Title', 'Genre', 'Rating', 'Votes']])

# 2. Genre Distribution
st.subheader("📊 Genre Distribution")
fig1, ax1 = plt.subplots()
df['Genre'].value_counts().plot(kind='bar', ax=ax1)
ax1.set_xlabel("Genre")
ax1.set_ylabel("Count")
st.pyplot(fig1)

# 3. Average Duration by Genre
st.subheader("⏱ Average Duration by Genre")
fig2, ax2 = plt.subplots()
df.groupby('Genre')['Duration'].mean().sort_values().plot(kind='barh', ax=ax2)
ax2.set_xlabel("Avg Duration (min)")
st.pyplot(fig2)

# 4. Voting Trends by Genre
st.subheader("📈 Average Voting Counts by Genre")
fig3, ax3 = plt.subplots()
df.groupby('Genre')['Votes'].mean().sort_values(ascending=False).plot(kind='bar', ax=ax3)
ax3.set_ylabel("Avg Votes")
st.pyplot(fig3)

# 5. Rating Distribution
st.subheader("⭐ Rating Distribution")
col1, col2 = st.columns(2)

with col1:
    fig4, ax4 = plt.subplots()
    sns.histplot(df['Rating'], bins=10, kde=True, ax=ax4)
    ax4.set_title("Histogram")
    st.pyplot(fig4)

with col2:
    fig5, ax5 = plt.subplots()
    sns.boxplot(x='Rating', data=df, ax=ax5)
    ax5.set_title("Boxplot")
    st.pyplot(fig5)

# 6. Genre-Based Rating Leaders
st.subheader("🏆 Top-Rated Movie by Genre")
leaders = df.sort_values('Rating', ascending=False).groupby('Genre').first().reset_index()
st.dataframe(leaders[['Genre', 'Title', 'Rating', 'Votes']])

# 7. Most Popular Genres by Voting
st.subheader("🔥 Most Popular Genres by Total Votes (Top 10)")
fig6, ax6 = plt.subplots()
df.groupby('Genre')['Votes'].sum().plot.pie(autopct='%1.1f%%', ax=ax6)
ax6.set_ylabel("")
st.pyplot(fig6)

# 8. Duration Extremes
st.subheader("📏 Duration Extremes")
shortest = df.loc[df['Duration'].idxmin()]
longest = df.loc[df['Duration'].idxmax()]
st.metric("Shortest Movie", f"{shortest['Title']} - {shortest['Duration']} min")
st.metric("Longest Movie", f"{longest['Title']} - {longest['Duration']} min")

# 9. Ratings by Genre Heatmap
st.subheader("🌡 Average Ratings by Genre (Heatmap)")
fig7, ax7 = plt.subplots()
sns.heatmap(df.groupby('Genre')['Rating'].mean().to_frame().T, annot=True, cmap='coolwarm', ax=ax7)
st.pyplot(fig7)

# 10. Ratings vs Votes Correlation
st.subheader("🔗 Correlation: Ratings vs Votes")
fig8, ax8 = plt.subplots()
sns.scatterplot(data=df, x='Votes', y='Rating', ax=ax8)
ax8.set_xlabel("Votes")
ax8.set_ylabel("Rating")
st.pyplot(fig8)