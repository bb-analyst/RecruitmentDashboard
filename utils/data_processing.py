import pandas as pd
import streamlit as st


@st.cache_data
def load_player_data():
    df = pd.read_csv('data/player_match_stats.csv')
    return df

@st.cache_data
def load_team_data():
    df = pd.read_csv('data/teams.csv')
    return df

def filter_player_data(df,filters,stat_map):
    filtered_df = df.copy()

    #filter comps
    if len(filters["comps_selection"]) > 0:
        filtered_df = filtered_df[filtered_df["compName"].isin(filters["comps_selection"])]

    #filter seasons
    if len(filters["season_selection"]) > 0:
        filtered_df = filtered_df[filtered_df["season"].isin(filters["season_selection"])]

    #filter positions
    if len(filters["position_selection"]) > 0:
        filtered_df = filtered_df[filtered_df["playerPosition"].isin(filters["position_selection"])]

    #filter teams
    if len(filters["team_selection"]) > 0:
        filtered_df = filtered_df[filtered_df["teamName"].isin(filters["team_selection"])]

    #filter players
    if len(filters["player_selection"]) > 0:
        filtered_df = filtered_df[filtered_df["playerName"].isin(filters["player_selection"])]

    #summarise/separate
    index_cols = ['compName']
    if filters["season_separate"]:
        index_cols.append('season')
    if filters["position_separate"]:
        index_cols.append('playerPosition')
    if filters["team_separate"]:
        index_cols.append('teamName')

    index_cols.append('playerName')

    if filters["summary_selection"] == 'Individual Games':
        index_cols.append('roundName')

    filtered_df = filtered_df.set_index(index_cols)[['mins']+filters["stat_selection"]]

    filtered_df = filtered_df.query("mins > 0")

    appearances = filtered_df.groupby(index_cols)['mins'].count()
    # summarise data
    min_games = filters['minimum_games_selection']
    if filters["summary_selection"] == 'Game Average':
        filtered_df = filtered_df.groupby(index_cols).mean().round(2)

        filtered_df.insert(0,'App',appearances)
        filtered_df = filtered_df.query("App >= @min_games")

    elif filters["summary_selection"] == 'Game Totals':
        filtered_df = filtered_df.groupby(index_cols).sum()

        filtered_df.insert(0,'App',appearances)
        filtered_df = filtered_df.query("App >= @min_games")

    index_map = {'compName':'Comp','season':'Season','playerPosition':'Pos','teamName':'Team','playerName':'Player','roundName':'Round'}
    map = index_map|stat_map
    filtered_df = filtered_df.reset_index()
    filtered_df = filtered_df.rename(columns=map)
    filtered_df = filtered_df.set_index([map[i] for i in index_cols])
    return filtered_df