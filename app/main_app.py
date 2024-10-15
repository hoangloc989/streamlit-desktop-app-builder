<<<<<<< HEAD
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
=======
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
>>>>>>> d411d8c93ed13ff240ec2be16abd6e834477f0da
