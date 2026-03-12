import streamlit as st
from data_handle import new_df, similarity

st.header("🎬 Movie Recommender System")

movies_list = new_df['title'].values

select_movie = st.selectbox(
    "Type or select a Movie",
    movies_list
)

def recommend(movie):
    index = new_df[new_df['title'] == movie].index[0]
    distance = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])

    recommend_list = []

    for i in distance[1:6]:
        recommend_list.append(new_df.iloc[i[0]].title)

    return recommend_list


if st.button('Show Recommendation'):
    recommended_movies = recommend(select_movie)

    st.subheader("Recommended Movies")

    for movie in recommended_movies:
        st.write(movie)
    