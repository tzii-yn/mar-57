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

