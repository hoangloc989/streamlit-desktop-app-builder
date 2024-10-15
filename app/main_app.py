import streamlit as st

# Importing the pages
import home, about, dashboard, data

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