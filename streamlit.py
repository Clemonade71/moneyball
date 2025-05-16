import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the tournament data
file_path = 'tournament_statistical_ranges.csv'
df = pd.read_csv(file_path)

# Load the BYU data
byu_data_path = 'byu_metrics.csv'
byu_df = pd.read_csv(byu_data_path)

# Adjust column names for compatibility
df.columns = df.columns.str.strip()
byu_df.columns = ['Metric', 'Season', 'Conference']

# Define metrics
metrics = df['Metric'].unique().tolist()

# Title
st.title('March Madness Analysis and BYU Metrics ')

# Tabs for each metric
tabs = st.tabs(metrics)

for tab, metric in zip(tabs, metrics):
    with tab:
        # Display Tournament Data
        st.subheader(f"{metric} - Tournament Data")
        metric_data = df[df['Metric'] == metric]
        rounds = metric_data['Round'].unique()

        # Display BYU Data
        st.subheader(f"BYU {metric}")
        byu_season_value = byu_df[byu_df['Metric'] == metric]['Season'].values
        byu_conference_value = byu_df[byu_df['Metric'] == metric]['Conference'].values
        if len(byu_season_value) > 0 and len(byu_conference_value) > 0:
            st.metric(label=f"BYU {metric} (Season)", value=byu_season_value[0])
            st.metric(label=f"BYU {metric} (Conference)", value=byu_conference_value[0])
        else:
            st.write("No BYU data available for this metric.")

        # Display statistical ranges in list form with mean and 95% confidence intervals
        st.subheader("Statistical Ranges by Round")
        for round_name in rounds:
            round_data = metric_data[metric_data['Round'] == round_name]
            if not round_data.empty:
                min_val = round_data['Min'].values[0]
                max_val = round_data['Max'].values[0]
                mean_val = round_data['Mean'].values[0]
                lower_bound = round_data['95% CI Low'].values[0]
                upper_bound = round_data['95% CI Upper'].values[0]
                st.markdown(f"**{round_name}:** <span style='color: #1f77b4;'>{min_val} - {max_val}</span>", unsafe_allow_html=True)
                st.markdown(f"**Mean:** <span style='color: #ff7f0e;'>{mean_val:.2f}</span>, **95% CI:** (<span style='color: #2ca02c;'>{lower_bound:.2f}</span>, <span style='color: #2ca02c;'>{upper_bound:.2f}</span>)", unsafe_allow_html=True)
            else:
                st.write(f"No data available for {round_name} in {metric}")

        # Line Chart for Metric
        st.subheader(f"{metric} - Tournament Ranges")
        plt.figure(figsize=(10, 5))
        for round_name in rounds:
            round_data = metric_data[metric_data['Round'] == round_name]
            if not round_data.empty:
                plt.plot(round_name, round_data['Mean'].values[0], marker='o', label=round_name)
        plt.title(f'{metric} - Tournament Ranges')
        plt.xlabel('Round')
        plt.ylabel('Mean Value')
        plt.grid(alpha=0.3)
        plt.legend()
        st.pyplot(plt)
        plt.clf()


