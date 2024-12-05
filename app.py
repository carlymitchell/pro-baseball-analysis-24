import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Title for the Streamlit app
st.markdown("<h1 style='font-size:32px;'>Majorr and Minor League Baseball Stats 2024</h1>", unsafe_allow_html=True)

# Load MLB Batters Data
@st.cache_data
def load_mlb_batters_data():
    return pd.read_csv('mlb-batters.csv')

# Load MLB Pitchers Data
@st.cache_data
def load_mlb_pitchers_data():
    return pd.read_csv('mlb-pitching.csv')

# Load MiLB Data (ALL)
@st.cache_data
def load_csv_data():
    df_milb_pitchers = pd.read_csv('milb-pitchers.csv')
    df_milb_batters = pd.read_csv('milb-batters.csv')
    return df_milb_pitchers, df_milb_batters

# Load FA Hitters
@st.cache_data
def load_free_agents_data():
    return pd.read_csv('upcoming_fa_hit.csv')

# Load FA Pitchers
@st.cache_data
def load_free_agent_pitchers_data():
    return pd.read_csv('upcoming_fa_pitch.csv')

# Spinner while data fetching
with st.spinner('Loading data...'):
    df_mlb_batters = load_mlb_batters_data()
    df_mlb_pitchers = load_mlb_pitchers_data()
    df_milb_pitchers, df_milb_batters = load_csv_data()
    df_free_agents = load_free_agents_data()
    df_free_agent_pitchers = load_free_agent_pitchers_data()

# Function to create comparison bar graphs
def create_comparison_bar_graph(df, selected_players, stats_to_plot, title="Comparison of Selected Players"):
    """Generate a bar graph for comparing selected players."""
    comparison_df = df[df['Name'].isin(selected_players)]
    if not comparison_df.empty:
        comparison_df = comparison_df.set_index('Name')
        fig, ax = plt.subplots()
        comparison_df[stats_to_plot].plot(kind='bar', ax=ax)
        ax.set_title(title)
        plt.xticks(rotation=45)
        plt.tight_layout()
        st.pyplot(fig)
    else:
        st.error("No data available for the selected players.")

# Tabs for Batting, Pitching Stats, MiLB data, and Upcoming Free Agents
tab1, tab2, tab3, tab4 = st.tabs(["MLB Batting", "MLB Pitching", "Minor League Baseball", "Upcoming MLB Free Agents"])

# Tab 1: MLB Batting
with tab1:
    st.subheader('2024 Major League Baseball Batting Stats')
    
    if not df_mlb_batters.empty:
        # Filter by Team
        teams_batting = df_mlb_batters['Team'].unique()
        selected_team_batting = st.selectbox(
            "Select Team for Batting Stats", 
            options=['All Teams'] + list(teams_batting), 
            key="mlb_batting_team_select"
        )

        # Apply Team Filter
        filtered_df_batting = (
            df_mlb_batters 
            if selected_team_batting == 'All Teams' 
            else df_mlb_batters[df_mlb_batters['Team'] == selected_team_batting]
        )

        # Filter by Minimum Plate Appearances (PA)
        if 'PA' in filtered_df_batting.columns:
            min_pa = st.slider(
                "Select Minimum Plate Appearances (PA)", 
                min_value=0, 
                max_value=int(filtered_df_batting['PA'].max()), 
                value=100, 
                step=10, 
                key="mlb_batting_min_pa_slider"
            )
            filtered_df_batting = filtered_df_batting[filtered_df_batting['PA'] >= min_pa]
        else:
            st.warning("The dataset does not contain a 'PA' column for filtering.")
        
        # Display Filtered Data
        st.dataframe(filtered_df_batting)

        # Player and Stat Selection for Comparison
        players_batting = filtered_df_batting['Name'].unique()
        selected_players_batting = st.multiselect(
            "Select Players to Compare", 
            options=players_batting, 
            key="mlb_batting_players_select"
        )
        stats_to_plot_batting = st.multiselect(
            "Select Stats to Compare", 
            options=filtered_df_batting.select_dtypes(include='number').columns, 
            key="mlb_batting_stats_select"
        )

        # Generate Comparison Bar Graph
        if selected_players_batting and stats_to_plot_batting:
            create_comparison_bar_graph(
                filtered_df_batting, 
                selected_players_batting, 
                stats_to_plot_batting, 
                title="MLB Batting Comparison"
            )
    else:
        st.error("No data available for MLB batters.")


# Tab 2: MLB Pitching
with tab2:
    st.subheader('2024 Major League Baseball Pitching Stats')
    
    if not df_mlb_pitchers.empty:
        # Filter by Team
        teams_pitching = df_mlb_pitchers['Team'].unique()
        selected_team_pitching = st.selectbox(
            "Select Team for Pitching Stats", 
            options=['All Teams'] + list(teams_pitching), 
            key="mlb_pitching_team_select"
        )

        # Apply Team Filter
        filtered_df_pitching = (
            df_mlb_pitchers 
            if selected_team_pitching == 'All Teams' 
            else df_mlb_pitchers[df_mlb_pitchers['Team'] == selected_team_pitching]
        )

        # Filter by Minimum Innings Pitched (IP)
        if 'IP' in filtered_df_pitching.columns:
            min_ip = st.slider(
                "Select Minimum Innings Pitched (IP)", 
                min_value=0, 
                max_value=int(filtered_df_pitching['IP'].max()), 
                value=10, 
                step=1, 
                key="mlb_pitching_min_ip_slider"
            )
            filtered_df_pitching = filtered_df_pitching[filtered_df_pitching['IP'] >= min_ip]
        else:
            st.warning("The dataset does not contain an 'IP' column for filtering.")
        
        # Display Filtered Data
        st.dataframe(filtered_df_pitching)

        # Player and Stat Selection for Comparison
        players_pitching = filtered_df_pitching['Name'].unique()
        selected_players_pitching = st.multiselect(
            "Select Players to Compare", 
            options=players_pitching, 
            key="mlb_pitching_players_select"
        )
        stats_to_plot_pitching = st.multiselect(
            "Select Stats to Compare", 
            options=filtered_df_pitching.select_dtypes(include='number').columns, 
            key="mlb_pitching_stats_select"
        )

        # Generate Comparison Bar Graph
        if selected_players_pitching and stats_to_plot_pitching:
            create_comparison_bar_graph(
                filtered_df_pitching, 
                selected_players_pitching, 
                stats_to_plot_pitching, 
                title="MLB Pitching Comparison"
            )
    else:
        st.error("No data available for MLB pitchers.")


# Tab 3: MiLB Data
with tab3:
    st.subheader('2024 Minor League Baseball Stats')

    # MiLB Pitchers Section
    st.write("### MiLB Pitchers")
    if 'Team' in df_milb_pitchers.columns:
        teams_pitchers_milb = df_milb_pitchers['Team'].unique()
        selected_team_pitchers_milb = st.selectbox("Select Team for MiLB Pitchers", options=['All Teams'] + list(teams_pitchers_milb), key="milb_pitchers_team_select")
        
        filtered_milb_pitchers = df_milb_pitchers if selected_team_pitchers_milb == 'All Teams' else df_milb_pitchers[df_milb_pitchers['Team'] == selected_team_pitchers_milb]
        st.dataframe(filtered_milb_pitchers)

        pitchers_milb = filtered_milb_pitchers['Name'].unique()
        selected_pitchers_milb = st.multiselect("Select MiLB Pitchers to Compare", options=pitchers_milb, key="milb_pitchers_select")
        stats_to_plot_pitchers_milb = st.multiselect("Select Stats to Compare", options=filtered_milb_pitchers.select_dtypes(include='number').columns, key="milb_pitching_stats_select")
        
        if selected_pitchers_milb and stats_to_plot_pitchers_milb:
            create_comparison_bar_graph(filtered_milb_pitchers, selected_pitchers_milb, stats_to_plot_pitchers_milb, title="MiLB Pitching Comparison")

    st.write("### MiLB Batters")
    if 'Team' in df_milb_batters.columns:
        teams_batters_milb = df_milb_batters['Team'].unique()
        selected_team_batters_milb = st.selectbox("Select Team for MiLB Batters", options=['All Teams'] + list(teams_batters_milb), key="milb_batters_team_select")
        
        filtered_milb_batters = df_milb_batters if selected_team_batters_milb == 'All Teams' else df_milb_batters[df_milb_batters['Team'] == selected_team_batters_milb]
        st.dataframe(filtered_milb_batters)

        batters_milb = filtered_milb_batters['Name'].unique()
        selected_batters_milb = st.multiselect("Select MiLB Batters to Compare", options=batters_milb, key="milb_batters_select")
        stats_to_plot_batters_milb = st.multiselect("Select Stats to Compare", options=filtered_milb_batters.select_dtypes(include='number').columns, key="milb_batting_stats_select")
        
        if selected_batters_milb and stats_to_plot_batters_milb:
            create_comparison_bar_graph(filtered_milb_batters, selected_batters_milb, stats_to_plot_batters_milb, title="MiLB Batting Comparison")

# Tab 4: Upcoming MLB Free Agents
with tab4:
    st.subheader("Upcoming MLB Free Agents - 2024 Offseason")
    st.write("Explore the list of players expected to hit free agency. Filter by team or compare key metrics.")

    free_agent_type = st.radio("Select Player Type", options=["Hitters", "Pitchers"], key="fa_type_radio")

    if free_agent_type == "Hitters":
        if not df_free_agents.empty:
            teams = df_free_agents['Team'].unique() if 'Team' in df_free_agents.columns else []
            selected_team = st.selectbox("Select Team", options=['All Teams'] + list(teams), key="hitters_team_select")

            filtered_df_hitters = df_free_agents if selected_team == 'All Teams' else df_free_agents[df_free_agents['Team'] == selected_team]
            st.dataframe(filtered_df_hitters)

            players_hitters = filtered_df_hitters['Name'].unique()
            selected_players_hitters = st.multiselect("Select Hitters to Compare", options=players_hitters, key="free_agents_hitters_select")
            stats_to_plot_hitters = st.multiselect("Select Stats to Compare", options=filtered_df_hitters.select_dtypes(include='number').columns, key="free_agents_hitters_stats_select")

            if selected_players_hitters and stats_to_plot_hitters:
                create_comparison_bar_graph(filtered_df_hitters, selected_players_hitters, stats_to_plot_hitters, title="Free Agent Hitters Comparison")

    elif free_agent_type == "Pitchers":
        if not df_free_agent_pitchers.empty:
            teams = df_free_agent_pitchers['Team'].unique() if 'Team' in df_free_agent_pitchers.columns else []
            selected_team = st.selectbox("Select Team", options=['All Teams'] + list(teams), key="pitchers_team_select")

            filtered_df_pitchers = df_free_agent_pitchers if selected_team == 'All Teams' else df_free_agent_pitchers[df_free_agent_pitchers['Team'] == selected_team]
            st.dataframe(filtered_df_pitchers)

            players_pitchers = filtered_df_pitchers['Name'].unique()
            selected_players_pitchers = st.multiselect("Select Pitchers to Compare", options=players_pitchers, key="free_agents_pitchers_select")
            stats_to_plot_pitchers = st.multiselect("Select Stats to Compare", options=filtered_df_pitchers.select_dtypes(include='number').columns, key="free_agents_pitchers_stats_select")

            if selected_players_pitchers and stats_to_plot_pitchers:
                create_comparison_bar_graph(filtered_df_pitchers, selected_players_pitchers, stats_to_plot_pitchers, title="Free Agent Pitchers Comparison")



