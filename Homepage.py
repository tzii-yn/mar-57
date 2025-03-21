import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from data.scientifctocommon import scientific_names, common_names
from images.scientific_images import images
import altair as alt
from vega_datasets import data


df1 = pd.read_csv("data/all_animals.csv")

### NOTES ###
# access images: <your-app-url>/app/static/<filename>
# http://localhost:8501/app/static/cat.png

### HOMEPAGE CONFIGURATIONS ###
st.set_page_config(page_title="mar-57 hackathon page!", page_icon="❤️‍🔥")
st.title("Analysis on Endangered Animals")
colx, coly, colz = st.columns([0.6, 0.2, 0.2], gap="small")
with colx:
  st.header("Overview")
  # insert comments/overview
  st.markdown(":small[Hello, we are :red[group 57] :heart: and we will be analyzing the number of endangered animal species around the world!]")
  
  #metric
  st.metric("Total Number of Extinctions", df1['EX'].iloc[:39].sum() + df1['EW'].iloc[:39].sum())
  
with coly:
  st.image("images/white fox.png", "ENDANGERED", width=100)

with colz:
  st.image("images/Panda8.jpg", "ENDANGERED", width=115)

st.divider()

### OVERVIEW PAGE ###

st.markdown("Species are classified as: **EX** - Extinct, **EW** - Extinct in the Wild, **CR** - Critically Endangered, **EN** - Endangered, **VU** - Vulnerable, **NT** - Near Threatened, **DD** - Data Deficient, **LC** - Least Concern, **PE** - Possibly Extinct, **PEW** - Possibly Extinct in Wild")
st.caption("Click on the individual points to understand more about the animal in Google")


#cleaning the file
for col in df1.columns[1:]:  #Skip the first column
  df1[col] = pd.to_numeric(df1[col].astype(str).str.replace(',', ''), errors='coerce')

#select all the rows without total
chart_df1 = df1.iloc[:39]

#select the columns for y-axis
y_columns = chart_df1.columns[1:3].tolist() + chart_df1.columns[4:6].tolist() + chart_df1.columns[7:10].tolist()

#sort the df in y-values ascending order
sorted_df = chart_df1.sort_values(by=y_columns)

#colors for the scatter dots
colors = ["#FF0000", "#FF7F00", "#FFFF00", "#00FF00", "#00FFFF", "#0000FF", "#7F00FF"]

#multiselect to filter y-columns
selected_y_columns = st.multiselect(
    "Select y-columns to display:",  
    y_columns,  
    default=y_columns  
)

#melt data to altair
melted_df = pd.melt(
    sorted_df,
    id_vars=["Name"],  
    value_vars=selected_y_columns,  
    var_name="Variable",  
    value_name="Value"  
)

#add color column to df
melted_df["Color"] = melted_df["Variable"].apply(lambda x: colors[y_columns.index(x)])


#selection for interactive legend
selection = alt.selection_point(fields=['Variable'], bind='legend')

#create altair chart
chart = alt.Chart(melted_df).transform_calculate(
    url='https://www.google.com/search?q=' + alt.datum.Name  
).mark_point().encode(
    x=alt.X('Name:N', title="Scientific Name"),  
    y=alt.Y('Value:Q', title="Value"),  
    # changing legend name
    color=alt.condition(
        selection,  #filtering data
        alt.Color('Variable:N', title="Legend", legend=alt.Legend(
            title="Legend", 
            orient="right",
        )),
        alt.value('lightgray')  #gray unselected points
    ),
    href='url:N',  
    tooltip=['Name:N', 'Value:Q', 'url:N']  
).properties(
    height=700,
    title="Various Threatened Species Data"
).add_params(
    selection  #add interactive legend
)

#display chart
st.altair_chart(chart, use_container_width=True)


#website we got the data from
st.link_button(":small[:gray[Retrieved from IUCN Red List of Threatened Species]]",
              "https://www.iucnredlist.org/resources/summary-statistics#Summary%20Tables",
              type="tertiary",
              icon="➡️"
              )



st.divider()

## make an info column to translate all the scientific names to english names
dict = {'Images': images, 'Scientific Name': scientific_names, 'Common Name': common_names}
df2 = pd.DataFrame(dict)

#search function
search_query = st.text_input("Search for an animal (by Scientific Name or Common Name):")

if search_query:
  search_query = search_query.lower()

  filtered_df = df2[
  df2['Scientific Name'].str.lower().str.contains(search_query) |
  df2['Common Name'].str.lower().str.contains(search_query)
  ]

else:
  filtered_df = df2

st.dataframe(
  filtered_df,
  height=700,
  column_config={
    "Images": st.column_config.ImageColumn(
      "Image",
      width="small"
    ),
    "Scientific Name": "Scientifc Name",
    "Common Name": "Common Name",
  },
  hide_index=True
)
