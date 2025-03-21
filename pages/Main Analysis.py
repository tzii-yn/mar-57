import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates

### PAGE CONFIGURATIONS ###
st.header("Number of Endangered Animals Analysis")

#import data
df = pd.read_csv("data/2024-2_RL_Table_2.csv", skiprows=1)

#data cleaning
for col in df.columns[1:]: 
  df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', ''), errors='coerce')

df['Year'] = pd.to_numeric(df['Year'], errors='coerce')

#clean data (only want animals)
#columns with animals
animal_columns = ["Mammals", "Birds", "Reptiles", "Amphibians", "Fishes", "Insects", "Molluscs", "Other invertebrates"]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15,5), constrained_layout=True)

for col in animal_columns:
  ax1.plot(df['Year'], df[col], label=col)

# Plot total
ax2.plot(df['Year'], df["TOTAL"], label="Total", linewidth=2, color='black')
sns.regplot(df, x=df["Year"], y=df["TOTAL"], label="Best Fit Line") #plot best fit line

# Add labels and title
ax1.set_xlabel("Year")
ax1.set_ylabel("Number of Species")
ax1.set_title("Number of Critically Endangered Species Over Time")
ax1.legend(title="Category", loc='upper left') 

ax2.set_xlabel("Year")
ax2.set_ylabel("Number of Species")
ax2.set_title("Number of Critically Endangered Species Over Time")
ax2.legend(title="Category", loc='upper left')

ax1.grid(color = 'green', linestyle = '--', linewidth = 0.5)
ax2.grid(color = 'green', linestyle = '--', linewidth = 0.5)

st.pyplot(plt)

#button for where data was retrieved
st.link_button(":small[:gray[Retrieved from IUCN Red List of Threatened Species]]",
  "https://www.iucnredlist.org/resources/summary-statistics#Summary%20Tables",
  type="tertiary",
  icon="➡️"
  )

st.divider()

#graph explanation
st.write("From these two graphs we can see that the number of critically endangered species are **increasing** over time.")
col1, col2 = st.columns([0.5, 0.5])
with col1:
  st.write("In the first graph, we can see that there was a huge spike in the number of **critically endangered Amphibians** at around **2002 to 2004**")
  st.markdown(":red[**Why is this so?**]")
  
with col2:
  st.metric("Critically Endangered Amphibian Species in 2004", "413", "1,276% rise compared to 2003", delta_color="inverse")

st.divider()


st.subheader("Potential Factors")
st.markdown("**Climate Change**")

#data from 1961, 2023
df2 = pd.read_csv('data/Annual_Surface_Temperature_Change.csv')
columns_to_remove = ['ObjectId', 'Indicator', 'ISO2', 'ISO3', 'Unit', 'Source', 'CTS_Code', 'CTS_Name', 'CTS_Full_Descriptor']
df2 = df2.drop(columns=columns_to_remove)

#remove F in the years
column_names = df2.columns
new_columns = []
for x in column_names:
    if x == 'Country':
        new_columns.append(x)
    else:
        new_columns.append(x.replace('F', ''))

df2.columns = new_columns

#multiselect
countries = df2['Country'].unique()
selected_country = st.multiselect('Select Countries', countries, default=countries[0])

#filter data based on selected country
filtered_data = df2[df2['Country'].isin(selected_country)]

#set country as index
filtered_data_transposed = filtered_data.set_index('Country').T

#convert years to int
filtered_data_transposed.index = filtered_data_transposed.index.astype(int)

#world temperature
# world_data = df2[df2.Country == 'World'].loc[:,'F2010':'F2014']
fig1, ax = plt.subplots(figsize=(10, 6))

for country in filtered_data_transposed.columns:
    ax.plot(filtered_data_transposed.index, filtered_data_transposed[country], label=country)

ax.set_title('Temperature Change Over Time')
ax.set_xlabel('Year')
ax.set_ylabel('Temperature Change (°C)')
ax.legend(title='Country', bbox_to_anchor=(1.05, 1), loc='upper left')
ax.grid(True)

st.pyplot(fig1)

st.write("According to our research, rising temperatures from climate change force species beyond their thermal "
         "limits, causing habitat loss, disrupting ecological relationships, and increasing disease exposure, "
         "all of which contribute to higher extinction rates.")
