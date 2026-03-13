import streamlit as st
from data_handle import new_df, similarity
from filter import recommend_movies, all_genres

st.header("🎬 Movie Recommender System")

# Session state to control UI
if "show_results" not in st.session_state:
    st.session_state.show_results = False

if "selected_genres" not in st.session_state:
    st.session_state.selected_genres = []

if "selected_movie" not in st.session_state:
    st.session_state.selected_movie = ""


# Movie dropdown
movies_list = [""] + list(new_df['title'].values)

select_movie = st.selectbox(
    "Type or select a Movie (optional)",
    movies_list
)


def recommend(movie):
    index = new_df[new_df['title'] == movie].index[0]

    distance = sorted(
        list(enumerate(similarity[index])),
        reverse=True,
        key=lambda x: x[1]
    )

    recommend_list = []

    for i in distance[1:6]:
        recommend_list.append(new_df.iloc[i[0]].title)

    return recommend_list


# BEFORE clicking recommendation
if not st.session_state.show_results:

    st.subheader("Select Genres")

    selected_genres = []

    cols = st.columns(4)

    for i, genre in enumerate(all_genres):
        if cols[i % 4].toggle(genre):
            selected_genres.append(genre)

    if st.button("Show Recommendation"):

        st.session_state.selected_genres = selected_genres
        st.session_state.selected_movie = select_movie
        st.session_state.show_results = True

        st.rerun()


# AFTER clicking recommendation
else:

    st.subheader("Recommended Movies")

    selected_genres = st.session_state.selected_genres
    select_movie = st.session_state.selected_movie

    if selected_genres:
        recommended_movies = recommend_movies(selected_genres)

    elif select_movie != "":
        recommended_movies = recommend(select_movie)

    else:
        st.warning("Please select a movie or genres.")
        recommended_movies = []

    for movie in recommended_movies:
        st.write(movie)

    # Back button
    if st.button("🔄 Back"):
        st.session_state.show_results = False
        st.rerun()
    