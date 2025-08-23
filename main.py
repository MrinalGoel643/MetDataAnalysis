import streamlit as st
import met_api
import pandas as pd
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
# Search bar
st.markdown("""
<div style='display: flex; justify-content: center;'>
    <input type="text" placeholder=" 🔎  Search Met's Art Collection...." 
           style="padding: 10px; width: 250px; border-radius: 20px; border: 1px solid #ccc;">
</div>
""", unsafe_allow_html=True)

# Department analytic
st.write("")
st.subheader("Departments for your search")

query = st.text_input("Search term (for images only)", value="cats", key="dept_query")
max_ids = st.slider("How many results to analyze", 20, 400, 150, 10, key="dept_max")

if st.button("Run department analytic", key="dept_run"):
    with st.spinner("Fetching and tallying departments…"):
        rows = met_api.department_counts(q=query, max_ids=max_ids)

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
