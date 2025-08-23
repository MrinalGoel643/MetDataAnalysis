import streamlit as st
from met_api import get_objectsWithImages, get_images

# Caching Section
@st.cache_data
def cache_objectsWithImages():
    return get_objectsWithImages()

@st.cache_data
def cache_images(total, objectIDs, limit):
    return get_images(total, objectIDs, limit)



# Page setup
st.set_page_config(page_title="The METrics", layout="centered")

st.markdown("<h1 style='text-align: center;'>The METrics</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center;'>Data Analysis of the Met Museum's Art Collection</h4>",
            unsafe_allow_html=True)

st.write("")

# CSS for fixed-height image boxes
st.markdown(
    """
    <style>
    .img-box {
        height: 150px;
        width: 150px;
        overflow: hidden;
        border: 1px solid #ccc;
        border-radius: 6px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .img-box img {
        height: 100%;
        width: auto;
        object-fit: cover;
    }
    </style>
    """,
    unsafe_allow_html=True
)

total, ids = cache_objectsWithImages()
images = cache_images(total, ids, limit=3)


if images:
    # Columns with fixed-height images
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            f"<div class='img-box'><img src='{images[0][0]}'></div>",
            unsafe_allow_html=True
        )
        st.markdown(f"<div>{images[0][1]}</div>", unsafe_allow_html=True)
    with col2:
        st.markdown(
            f"<div class='img-box'><img src='{images[1][0]}'></div>",
            unsafe_allow_html=True
        )
        st.markdown(f"<div>{images[1][1]}</div>", unsafe_allow_html=True)
    with col3:
        st.markdown(
            f"<div class='img-box'><img src='{images[2][0]}'></div>",
            unsafe_allow_html=True
        )
        st.markdown(f"<div>{images[2][1]}</div>", unsafe_allow_html=True)

st.write("")
st.write("")
# Search bar
st.markdown("""
<div style='display: flex; justify-content: center;'>
    <input type="text" placeholder=" 🔎  Search Met's Art Collection...."
           style="padding: 10px; width: 250px; border-radius: 20px; border: 1px solid #ccc;">
</div>
""", unsafe_allow_html=True)

st.write("")

# Footer
st.markdown("""
<div style='position: fixed; bottom: 10px; left: 0; right: 0; text-align: center; font-size: 12px;'>
    <span style="font-size: 14px;">ℹ️ Met API and data related information is available at –
    <a href="https://metmuseum.github.io/" target="_blank">https://metmuseum.github.io/</a></span>
</div>
""", unsafe_allow_html=True)
