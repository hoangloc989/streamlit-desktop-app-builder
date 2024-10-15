import streamlit as st

# Importing the pages
import home, about, dashboard, data
st.set_page_config(
    page_title="My Awesome Streamlit App",  
    page_icon="app/assets/apps.ico",  
    layout="wide",  
    initial_sidebar_state="expanded"  # Initial state of the sidebar
)
# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ("Home", "About", "Dashboard", "Data"))

# Display the selected page
if page == "Home":
    home.main()
elif page == "About":
    about.main()
elif page == "Dashboard":
    dashboard.main()
elif page == "Data":
    data.main()