import streamlit as st
import pandas as pd
from met_api import search_for_images, get_objectsWithImages, get_images, department_counts

@st.cache_data
def cached_search_for_images(query):
    return search_for_images(query, 2,departments=[1,3,4,5,6,7])

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


# Columns with fixed-height images
col1, col2, col3 = st.columns(3)

q = st.text_input("🔎  Search Met's Art Collection....",value="UFO", key="search_query")

r = cached_search_for_images(q)

summary = r[["primaryImageSmall","title","department","objectName"]]

config = {
    "primaryImageSmall": st.column_config.ImageColumn(),
}

event = st.dataframe(summary, column_config=config, use_container_width=True, on_select="rerun", selection_mode="single-row")

if event.selection.rows:
    selected_index = event.selection.rows[0] # Get the index of the first selected row
    selected_row_data = r.iloc[selected_index]

    st.subheader("Details of Selected Row:")
    st.image(selected_row_data["primaryImage"], caption=selected_row_data["title"], width=500)
    st.write(selected_row_data)
else:
    st.info("Select a row in the table to see its details.")

with col1:
    st.markdown(
        "<div class='img-box'><img src='https://images.metmuseum.org/CRDImages/ep/web-large/DP-29324-001.jpg'></div>",
        unsafe_allow_html=True
    )
with col2:
    st.markdown(
        "<div class='img-box'><img src='https://images.metmuseum.org/CRDImages/ad/web-large/DP124705.jpg'></div>",
        unsafe_allow_html=True
    )
with col3:
    st.markdown(
        "<div class='img-box'><img src='https://images.metmuseum.org/CRDImages/gr/web-large/DP21847edited.jpg'></div>",
        unsafe_allow_html=True
    )

st.write("")
st.write("")

# Department analytic
st.write("")
st.subheader("Departments for your search")

query = st.text_input("Search term (for images only)", value="cats", key="dept_query")
max_ids = st.slider("How many results to analyze", 20, 400, 150, 10, key="dept_max")

if st.button("Run department analytic", key="dept_run"):
    with st.spinner("Fetching and tallying departments…"):
        rows = department_counts(q=query, max_ids=max_ids)

    if not rows:
        st.info("No results found (or the API call failed). Try another term.")
    else:
        df = pd.DataFrame(rows, columns=["Department", "Count"])
        # show a quick bar chart + table
        st.bar_chart(df.set_index("Department"))
        st.dataframe(df, use_container_width=True)

st.write("")

# Footer
st.markdown("""
<div style='position: fixed; bottom: 10px; left: 0; right: 0; text-align: center; font-size: 12px;'>
    <span style="font-size: 14px;">ℹ️ Met API and data related information is available at –
    <a href="https://metmuseum.github.io/" target="_blank">https://metmuseum.github.io/</a></span>
</div>
""", unsafe_allow_html=True)
