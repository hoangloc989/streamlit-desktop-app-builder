<<<<<<< HEAD
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def main():
    st.title("Dashboard")
    st.write("This dashboard shows some sample graphs.")

    # Create sample data
    data = {
        'Category': ['A', 'B', 'C', 'D'],
        'Values': [10, 20, 30, 40]
    }
    df = pd.DataFrame(data)

    # Bar chart
    st.subheader("Bar Chart")
    plt.bar(df['Category'], df['Values'], color='skyblue')
    plt.xlabel('Category')
    plt.ylabel('Values')
    plt.title('Sample Bar Chart')
    st.pyplot(plt)

    # Clear the figure for the next plot
    plt.clf()

    # Line chart
    st.subheader("Line Chart")
    x = np.arange(1, 11)
    y = np.random.randn(10).cumsum()

    plt.plot(x, y, marker='o', color='orange')
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.title('Sample Line Chart')
    st.pyplot(plt)

if __name__ == "__main__":
=======
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def main():
    st.title("Dashboard")
    st.write("This dashboard shows some sample graphs.")

    # Create sample data
    data = {
        'Category': ['A', 'B', 'C', 'D'],
        'Values': [10, 20, 30, 40]
    }
    df = pd.DataFrame(data)

    # Bar chart
    st.subheader("Bar Chart")
    plt.bar(df['Category'], df['Values'], color='skyblue')
    plt.xlabel('Category')
    plt.ylabel('Values')
    plt.title('Sample Bar Chart')
    st.pyplot(plt)

    # Clear the figure for the next plot
    plt.clf()

    # Line chart
    st.subheader("Line Chart")
    x = np.arange(1, 11)
    y = np.random.randn(10).cumsum()

    plt.plot(x, y, marker='o', color='orange')
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.title('Sample Line Chart')
    st.pyplot(plt)

if __name__ == "__main__":
>>>>>>> d411d8c93ed13ff240ec2be16abd6e834477f0da
    main()