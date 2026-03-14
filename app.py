
import streamlit as st
from data_handle import new_df, similarity
from filter import recommend_movies, all_genres
from details import about

st.header("🎬 Movie Recommender System")

# ---------------- SESSION STATE ----------------

if "page" not in st.session_state:
    st.session_state.page = "home"

if "selected_movie" not in st.session_state:
    st.session_state.selected_movie = ""

if "selected_genres" not in st.session_state:
    st.session_state.selected_genres = []

if "recommended_movies" not in st.session_state:
    st.session_state.recommended_movies = []


# ---------------- RECOMMENDATION FUNCTION ----------------

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


# ---------------- SHOW MOVIE DETAILS PAGE ----------------

def movie_details_page(movie):

    movie_data = about[about['title'] == movie]

    if movie_data.empty:
        st.warning("Details not available for this movie.")
        return

    movie_data = movie_data.iloc[0]

    st.title(movie)

    st.write("🎬 **Overview**")
    st.write(movie_data['overview'])

    st.write("🎭 **Cast**")

    cast = movie_data['cast']

    if isinstance(cast, list):
        for actor in cast[:5]:
            st.markdown(f"• {actor}")
    else:
        st.write(cast)

    st.write("🎥 **Director**")

    director = movie_data['Director']

    if isinstance(director, list):
        st.write(", ".join(director))
    else:
        st.write(director)

    if st.button("⬅ Back to Recommendations"):
        st.session_state.page = "recommendations"
        st.rerun()


# ---------------- HOME PAGE ----------------

if st.session_state.page == "home":

    movies_list = [""] + list(new_df['title'].values)

    select_movie = st.selectbox(
        "Type or select a Movie (optional)",
        movies_list
    )

    st.subheader("Select Genres")

    selected_genres = []

    cols = st.columns(4)

    for i, genre in enumerate(all_genres):
        if cols[i % 4].toggle(genre):
            selected_genres.append(genre)

    if st.button("Show Recommendation"):

        if selected_genres:
            st.session_state.recommended_movies = recommend_movies(selected_genres)

        elif select_movie != "":
            st.session_state.recommended_movies = recommend(select_movie)

        else:
            st.warning("Please select a movie or genres.")
            st.stop()

        st.session_state.page = "recommendations"
        st.rerun()


# ---------------- RECOMMENDATION PAGE ----------------

elif st.session_state.page == "recommendations":

    st.subheader("Recommended Movies")

    movies = st.session_state.recommended_movies

    cols = st.columns(5)

    for i, movie in enumerate(movies):

        if cols[i].button(movie):
            st.session_state.selected_movie = movie
            st.session_state.page = "details"
            st.rerun()

    if st.button("🔄 Start Over"):
        st.session_state.page = "home"
        st.rerun()


# ---------------- DETAILS PAGE ----------------

elif st.session_state.page == "details":

    movie_details_page(st.session_state.selected_movie)






    