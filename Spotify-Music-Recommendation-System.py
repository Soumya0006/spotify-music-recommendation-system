
import streamlit as st
import os
import pickle
import pandas as pd

# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Spotify Music Recommender",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==========================================
# 2. CUSTOM CSS
# ==========================================

st.markdown("""
<style>

/* =====================================
   MAIN APPLICATION
===================================== */

.stApp {
    background: linear-gradient(135deg, #101820, #17232d);
    color: #ffffff;
}

header[data-testid="stHeader"] {
    background: transparent;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
}


/* =====================================
   MAIN HEADINGS
===================================== */

.main-title {
    font-size: 38px;
    font-weight: 800;
    color: #1DB954 !important;
    margin-bottom: 5px;
}

.subtitle {
    color: #b3b3b3 !important;
    font-size: 16px;
}

.section-title {
    color: #1DB954 !important;
    font-size: 23px;
    font-weight: 700;
    margin-top: 20px;
}


/* =====================================
   SIDEBAR DESIGN
===================================== */

[data-testid="stSidebar"] {
    background-color: #101820;
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] h4,
[data-testid="stSidebar"] h5,
[data-testid="stSidebar"] h6 {
    color: #ffffff !important;
}

[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] li,
[data-testid="stSidebar"] strong {
    color: #ffffff !important;
}

[data-testid="stSidebar"] [data-testid="stCaption"] {
    color: #b3b3b3 !important;
}

[data-testid="stSidebar"] hr {
    border-color: #52616b !important;
}


/* =====================================
   SONG RECOMMENDATION CARDS
===================================== */

.song-card {
    background-color: #202e38;
    padding: 18px;
    border-radius: 12px;
    border: 1px solid #344550;
    margin-bottom: 12px;
}

.song-name {
    color: #ffffff !important;
    font-size: 20px;
    font-weight: 700;
}

.artist-name {
    color: #b3b3b3 !important;
    font-size: 15px;
    margin-top: 8px;
}

.genre-name {
    color: #1DB954 !important;
    font-size: 14px;
    margin-top: 8px;
}


/* =====================================
   SONG SELECTION DROPDOWN
===================================== */

/* Dropdown background */

.stSelectbox [data-baseweb="select"] {
    background-color: #ffffff !important;
    border-radius: 10px !important;
}

/* Dropdown selected text */

.stSelectbox [data-baseweb="select"] * {
    color: #111111 !important;
}

/* Dropdown arrow */

.stSelectbox [data-baseweb="select"] svg {
    fill: #111111 !important;
    color: #111111 !important;
}

/* Dropdown options background */

[data-baseweb="popover"],
[data-baseweb="menu"] {
    background-color: #ffffff !important;
}

/* Dropdown options text */

[data-baseweb="option"] {
    color: #111111 !important;
    background-color: #ffffff !important;
}

/* Dropdown hover */

[data-baseweb="option"]:hover {
    background-color: #e8f5ed !important;
    color: #111111 !important;
}

/* Selectbox label */

.stSelectbox label,
.stSelectbox label p {
    color: #ffffff !important;
}


/* =====================================
   RECOMMENDATION SETTINGS SLIDER
===================================== */

/* Slider heading */

.stSlider label,
.stSlider label p,
.stSlider [data-testid="stWidgetLabel"],
.stSlider [data-testid="stWidgetLabel"] p {
    color: #ffffff !important;
    font-size: 16px !important;
    font-weight: 600 !important;
}

/* Slider value */

.stSlider [data-testid="stThumbValue"] {
    color: #1DB954 !important;
    font-weight: bold !important;
}

/* Slider active track */

.stSlider [data-baseweb="slider"] div[role="slider"] {
    background-color: #1DB954 !important;
    border-color: #1DB954 !important;
}

/* Slider number */

.stSlider {
    color: #ffffff !important;
}


/* =====================================
   DISCOVER BUTTON
===================================== */

div.stButton > button {
    background-color: #1DB954 !important;
    color: #07140b !important;
    border: none !important;
    border-radius: 25px !important;
    padding: 12px 25px !important;
    font-weight: bold !important;
    font-size: 16px !important;
    width: 100%;
    min-height: 48px;
}

div.stButton > button:hover {
    background-color: #1ed760 !important;
    color: #000000 !important;
}


/* =====================================
   DOWNLOAD BUTTON
===================================== */

[data-testid="stDownloadButton"] {
    width: 100%;
}

[data-testid="stDownloadButton"] button {
    background-color: #1DB954 !important;
    color: #07140b !important;
    border: none !important;
    border-radius: 25px !important;
    padding: 12px 25px !important;
    font-size: 16px !important;
    font-weight: 700 !important;
    width: 100% !important;
    min-height: 48px !important;
}

/* Download button text and icon */

[data-testid="stDownloadButton"] button p,
[data-testid="stDownloadButton"] button span,
[data-testid="stDownloadButton"] button div,
[data-testid="stDownloadButton"] button svg {
    color: #07140b !important;
    fill: #07140b !important;
    font-weight: 700 !important;
}

/* Download button hover */

[data-testid="stDownloadButton"] button:hover {
    background-color: #1ed760 !important;
    color: #000000 !important;
}


/* =====================================
   METRIC CARDS
===================================== */

[data-testid="stMetric"] {
    background-color: #202e38;
    padding: 15px;
    border-radius: 12px;
    border: 1px solid #344550;
}

[data-testid="stMetricLabel"],
[data-testid="stMetricValue"] {
    color: #ffffff !important;
}


/* =====================================
   EXPANDER AND TABLE
===================================== */

[data-testid="stExpander"] {
    background-color: #202e38;
    border: 1px solid #344550;
    border-radius: 10px;
}

[data-testid="stDataFrame"] {
    color: #ffffff;
}


/* =====================================
   SUCCESS MESSAGE
===================================== */

[data-testid="stAlert"] {
    border-radius: 12px;
}


/* =====================================
   FOOTER
===================================== */

.footer {
    text-align: center;
    color: #b3b3b3;
    padding: 20px;
}

</style>
""", unsafe_allow_html=True)



# 3. LOAD SAVED MODEL


@st.cache_resource
def load_model():

    file_path = "spotify_recommender.pkl"

    if not os.path.exists(file_path):
        raise FileNotFoundError(
            "spotify_recommender.pkl was not found."
        )

    with open(file_path, "rb") as file:
        model_data = pickle.load(file)

    return (
        model_data["music"],
        model_data["similarity"]
    )


try:

    music, similarity = load_model()

except Exception as e:

    st.error(f"Unable to load model: {e}")
    st.stop()


# ==========================================
# 4. VALIDATE MODEL
# ==========================================

if (
    len(music) != similarity.shape[0]
    or len(music) != similarity.shape[1]
):

    st.error(
        "Data and similarity matrix dimensions do not match."
    )
    st.stop()


if len(music) < 2:

    st.error(
        "At least two songs are required for recommendations."
    )
    st.stop()


required_columns = [
    "Song Name",
    "Artist",
    "Genre"
]

if not all(column in music.columns for column in required_columns):

    st.error(
        "Required columns are missing from the music dataset."
    )
    st.stop()



# 5. SIDEBAR


with st.sidebar:

    st.markdown("## 🎵 Music Recommender")

    st.markdown("---")

    st.markdown("### About Project")

    st.write(
        "A content-based music recommendation "
        "system using NLP, TF-IDF and Cosine Similarity."
    )

    st.markdown("---")

    st.markdown("### Model Information")

    st.write(
        f"🎧 Total Songs: {len(music):,}"
    )

    st.write(
        f"🎤 Unique Artists: {music['Artist'].nunique():,}"
    )

    st.write(
        f"🎼 Unique Genres: {music['Genre'].nunique():,}"
    )

    st.markdown("---")

    st.caption(
        "Built with Python, NLP and Streamlit"
    )



# 6. MAIN HEADER


st.markdown(
    '<div class="main-title">'
    '🎵 Music Discovery Studio'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Discover your next favourite song with intelligent music recommendations.'
    '</div>',
    unsafe_allow_html=True
)

st.markdown("---")



# 7. SONG SELECTION


st.markdown(
    '<div class="section-title">'
    '🎧 Choose Your Favourite Song'
    '</div>',
    unsafe_allow_html=True
)

song_options = list(range(len(music)))

selected_song = st.selectbox(
    "Search and select a song",

    options=song_options,

    format_func=lambda i: (
        f"{music.iloc[i]['Song Name']} - "
        f"{music.iloc[i]['Artist']}"
    ),

    key="song_selection"
)



# 8. DISPLAY SELECTED SONG DETAILS

selected_details = music.iloc[selected_song]

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "Selected Song",
        str(selected_details["Song Name"])
    )

with col2:

    st.metric(
        "Artist",
        str(selected_details["Artist"])
    )

with col3:

    st.metric(
        "Genre",
        str(selected_details["Genre"])
    )



# 9. RECOMMENDATION SETTINGS


st.markdown(
    '<div class="section-title">'
    '⚙️ Recommendation Settings'
    '</div>',
    unsafe_allow_html=True
)

number = st.slider(
    "How many songs would you like?",

    min_value=1,

    max_value=min(10, len(music) - 1),

    value=min(5, len(music) - 1),

    key="recommendation_count"
)



# 10. RECOMMENDATION FUNCTION


def recommended_songs(index, number):

    # Get similarity scores for selected song

    scores = list(enumerate(similarity[index]))

    # Sort songs by similarity score

    scores = sorted(
        scores,
        key=lambda x: x[1],
        reverse=True
    )

    # Remove selected song itself

    scores = [
        item for item in scores
        if item[0] != index
    ]

    # Select top recommendations

    top_scores = scores[:number]

    # Get recommended song indices

    recommended_indices = [
        item[0] for item in top_scores
    ]

    # Get recommended song details

    recommendations = music.iloc[
        recommended_indices
    ][
        ["Song Name", "Artist", "Genre"]
    ].copy()

    # Add similarity percentage

    recommendations["Similarity (%)"] = [
        round(float(score) * 100, 2)
        for _, score in top_scores
    ]

    return recommendations



# 11. RECOMMENDATION BUTTON


st.markdown("---")

if st.button(
    "✨ Discover Recommended Songs",
    key="discover_songs"
):

    recommendations = recommended_songs(
        selected_song,
        number
    )

    st.markdown(
        '<div class="section-title">'
        '🎶 Your Recommended Songs'
        '</div>',
        unsafe_allow_html=True
    )

    st.success(
        f"Found {len(recommendations)} recommendations "
        f"based on your selected song!"
    )



# DISPLAY RECOMMENDATION CARDS


    for i, row in recommendations.iterrows():

        st.markdown(
            f"""<div class="song-card">
<div class="song-name">🎵 {row['Song Name']}</div>
<div class="artist-name">Artist: {row['Artist']}</div>
<div class="genre-name">Genre: {row['Genre']}</div>
<div class="genre-name">Similarity: {row['Similarity (%)']}%</div>
</div>""",

            unsafe_allow_html=True
        )



# RECOMMENDATION TABLE


    with st.expander(
        "View recommendations in table format"
    ):

        st.dataframe(
            recommendations.reset_index(drop=True),
            use_container_width=True,
            hide_index=True
        )



# DOWNLOAD RECOMMENDATIONS


    csv = recommendations.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="⬇️ Download Recommendations",

        data=csv,

        file_name="spotify_recommendations.csv",

        mime="text/csv",

        key="spotify_recommendations_download"
    )



# 12. FOOTER


st.markdown(
    """
    <div class="footer">
        Music Discovery Studio |
        Powered by Python, NLP, TF-IDF & Cosine Similarity
    </div>
    """,
    unsafe_allow_html=True
)
