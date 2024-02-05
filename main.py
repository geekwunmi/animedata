import pandas as pd
import seaborn as sns
import numpy as np
import streamlit as st

anime = pd.read_csv(r"C:\Users\Ade\Desktop\Personal\Python\Project Portfolio\animedashboard\animefile2024.csv")
anime_df = pd.DataFrame(anime)
print(anime_df.head(5))

anime_df_2023 = anime_df[anime_df['year'] == 2023]
anime_df_2022 = anime_df[anime_df['year'] == 2022]
anime_df_2021 = anime_df[anime_df['year'] == 2021]
anime_df_2020 = anime_df[anime_df['year'] == 2020]

st.line_chart(anime_df['popularity'])