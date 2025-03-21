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
st.write("Experiment with the graph by selecting different countries!")

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

#singleselect
countries = df2['Country'].unique()
default_country = "World" if "World" in countries else countries[0]
selected_country = st.selectbox('Select a Country', countries, index=countries.tolist().index(default_country))

#filter data based on selected country
filtered_data = df2[df2['Country'] == selected_country]

#set country as index
filtered_data_transposed = filtered_data.set_index('Country').T

#convert years to int
filtered_data_transposed.index = filtered_data_transposed.index.astype(int)

#world temperature
# world_data = df2[df2.Country == 'World'].loc[:,'F2010':'F2014']
fig1, ax = plt.subplots(figsize=(10, 6))

for country in filtered_data_transposed.columns:
    ax.plot(filtered_data_transposed.index, filtered_data_transposed[country], label=country)
    sns.regplot(filtered_data_transposed,
            x=filtered_data_transposed.index,
            y=filtered_data_transposed[country],
            scatter=False,
            label="Best Fit Line",
            color='peachpuff'
            )  # plot best fit line


ax.set_title('Change in Temperature Over Time')
ax.set_xlabel('Year')
ax.set_ylabel('Temperature Change (°C)')
ax.legend(title='Country', bbox_to_anchor=(1.05, 1), loc='upper left')
ax.grid(True)

st.pyplot(fig1, clear_figure=True)

st.link_button(":small[:gray[Retrieved from IMF Climate Change Dashboard]]",
  "https://climatedata.imf.org/pages/climatechange-data",
  type="tertiary",
  icon="➡️"
  )

st.write("From the graph, we can see that there is a positive change in temperature over time overall. This shows that "
         "**temperatures have been rising**")
st.write("According to our research, rising temperatures from climate change force species beyond their thermal "
         "limits, causing habitat loss, disrupting ecological relationships, and increasing disease exposure, "
         "all of which contribute to higher extinction rates.")

st.divider()

##Next Factor
st.markdown("**Invasive Species**")
df3 = pd.read_csv("data/invasive_species_population_millions(invasive_species_population_mil).csv")

st.line_chart(df3, x="Year", y="Invasive Species (Global) Population Estimate (Millions)", y_label="Invasive Species Population (Millions)", color="#efa190")

#info column
colx, coly = st.columns([0.4, 0.6])
with colx:
    with st.expander("What are **invasive species**?", icon='🤔'):
        st.write("Invasive species are introduced, nonnative organism (disease, parasite, plant, or animal) that "
                 "begins to spread from the site of its original introduction. They often "
                 "outcompete native species for resources, leading to reduced biodiversity and altered habitats.")
        st.image("https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/s3fs-public/styles/masonry/public/lionfish.jpg?itok=AMlU21_u")
        st.caption("Invasive Adult Lionfish")

with coly:
    st.write("In the graph, it can be seen that the global invasive species population has been **increasing**. ")
    st.write("An increase in invasive species would then lead to a rise in extinction. This happens because more "
             "invasive species mean more competition, predation, habitat destruction, and disease spread—all of which "
             "put native species at risk.")

st.divider()

st.subheader("Conclusion")
col3, col4 = st.columns([0.5, 0.5])
with col3:
    st.write(
        "Regulatory Methods: "
        "\nProtected Areas: Establishing national parks and wildlife reserves. \nAnti-Poaching Laws: Stricter penalties and use of surveillance technology (e.g., drones, tracking systems). \nInternational Agreements: Enforcement of treaties like CITES to regulate wildlife trade.\nPublic Education & Community Involvement: Raising awareness and promoting sustainable practices."
    )

with col4:
    st.write("In conclusion, the decline of endangered animals is a pressing issue driven by various human and environmental factors. Climate change, distruption of ecosystems due to invasive species habitat destruction for urbanisation have all contributed to the rapid decrease in wildlife populations. Our findings highlight the urgent need for conservation efforts, stricter regulations, and public awareness to protect these species from extinction. By addressing these threats and promoting sustainable practices, we can help preserve biodiversity and ensure a balanced ecosystem for future generations.")
