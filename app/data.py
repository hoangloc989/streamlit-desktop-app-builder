<<<<<<< HEAD
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from urllib.error import URLError

def main():
    st.markdown("# DataFrame Demo")
    st.sidebar.header("DataFrame Demo")
    st.write(
        """This demo shows how to use `st.write` to visualize Pandas DataFrames.
        (Data courtesy of the [UN Data Explorer](http://data.un.org/Explorer.aspx).)"""
    )

    @st.cache_data
    def get_UN_data():
        AWS_BUCKET_URL = "http://streamlit-demo-data.s3-us-west-2.amazonaws.com"
        df = pd.read_csv(AWS_BUCKET_URL + "/agri.csv.gz")
        return df.set_index("Region")

    try:
        df = get_UN_data()
        countries = st.multiselect(
            "Choose countries", list(df.index), ["China", "United States of America"]
        )
        if not countries:
            st.error("Please select at least one country.")
        else:
            data = df.loc[countries]
            data /= 1000000.0
            st.write("### Gross Agricultural Production ($B)", data.sort_index())

            # Prepare data for plotting
            data = data.T.reset_index()
            data = pd.melt(data, id_vars=["index"]).rename(
                columns={"index": "year", "value": "Gross Agricultural Product ($B)"}
            )

            # Create a line plot using Matplotlib
            plt.figure(figsize=(10, 6))
            for country in countries:
                plt.plot(data[data['Region'] == country]['year'], 
                         data[data['Region'] == country]['Gross Agricultural Product ($B)'], 
                         marker='o', label=country)

            plt.title('Gross Agricultural Production ($B) Over Years')
            plt.xlabel('Year')
            plt.ylabel('Gross Agricultural Product ($B)')
            plt.xticks(rotation=45)
            plt.legend(title='Countries')
            plt.tight_layout()

            # Display the plot in Streamlit
            st.pyplot(plt)
            plt.clf()  # Clear the current figure for future plots
    except URLError as e:
        st.error(
            """
            **This demo requires internet access.**
            Connection error: %s
            """
            % e.reason
        )

if __name__ == "__main__":
=======
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from urllib.error import URLError

def main():
    st.markdown("# DataFrame Demo")
    st.sidebar.header("DataFrame Demo")
    st.write(
        """This demo shows how to use `st.write` to visualize Pandas DataFrames.
        (Data courtesy of the [UN Data Explorer](http://data.un.org/Explorer.aspx).)"""
    )

    @st.cache_data
    def get_UN_data():
        AWS_BUCKET_URL = "http://streamlit-demo-data.s3-us-west-2.amazonaws.com"
        df = pd.read_csv(AWS_BUCKET_URL + "/agri.csv.gz")
        return df.set_index("Region")

    try:
        df = get_UN_data()
        countries = st.multiselect(
            "Choose countries", list(df.index), ["China", "United States of America"]
        )
        if not countries:
            st.error("Please select at least one country.")
        else:
            data = df.loc[countries]
            data /= 1000000.0
            st.write("### Gross Agricultural Production ($B)", data.sort_index())

            # Prepare data for plotting
            data = data.T.reset_index()
            data = pd.melt(data, id_vars=["index"]).rename(
                columns={"index": "year", "value": "Gross Agricultural Product ($B)"}
            )

            # Create a line plot using Matplotlib
            plt.figure(figsize=(10, 6))
            for country in countries:
                plt.plot(data[data['Region'] == country]['year'], 
                         data[data['Region'] == country]['Gross Agricultural Product ($B)'], 
                         marker='o', label=country)

            plt.title('Gross Agricultural Production ($B) Over Years')
            plt.xlabel('Year')
            plt.ylabel('Gross Agricultural Product ($B)')
            plt.xticks(rotation=45)
            plt.legend(title='Countries')
            plt.tight_layout()

            # Display the plot in Streamlit
            st.pyplot(plt)
            plt.clf()  # Clear the current figure for future plots
    except URLError as e:
        st.error(
            """
            **This demo requires internet access.**
            Connection error: %s
            """
            % e.reason
        )

if __name__ == "__main__":
>>>>>>> d411d8c93ed13ff240ec2be16abd6e834477f0da
    main()