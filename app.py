import streamlit as st
import pandas as pd
from utils.data_processing import load_player_data, load_team_data, filter_player_data

# Page config
st.set_page_config(layout="wide", page_title="Recruitment Dashboard")
st.title("Recruitment Dashboard")

# Load data
player_df = load_player_data()
team_df = load_team_data()

#get other filtering details

summary_list = ['Game Average','Game Totals','Individual Games']

stat_options = {'allRuns':'R',
                'allRunMetres':'R-Met',
                'postContactMetres':'PC-Met',
                'tries':'T',
                'tryAssists':'TA',
                'tryInvolvement':'TI',
                'linebreaks':'LB',
                'linebreakAssists':'LBA',
                'tackleBreaks':'TB',
                'supports':'Supp',
                'decoys':'Dec',
                'receipts':'Rec',
                'Passes':'Pass',
                'offloads':'Off',
                'errors':'Err',
                'tackles':'Tk-Made',
                'ineffectiveTackles':'Tk-Ine',
                'missedTackles':'Tk-Mis',
                'effectiveTacklePercentage':'T%',
                'forcedTurnover':'FT',
                'tryCause':'T-Cause',
                'trySaves':'T-Save',
                'kickPressures':'KP',
                'penalties':'Pens',
                'ruckInfringements':'6A-RI',
                'setRestartConceded10mOffside':'6A-10m',
                'kicks': 'K',
                'kickMetres': 'K-Met',
                'kickTryAssist': 'K-TA',
                'fortyTwentyKicks': 'K-4020',
                'longKicksSpace': 'K-Space',
                'forcedDropoutKicker': 'K-FD',
                'kickDead': 'K-Dead',
                'kicksDefused': 'K-Def',
                'kicksNotDefused': 'K-NotDef',
                'allGoalsAttempted':'G-Att',
                'allGoals':'G-Made',
                'allGoalsMissed':'G-Mis',
                'kickReturns':'KR',
                'kickReturnMetres':'KR-Met',
                'dummyHalfRuns':'DHR',
                'dummyHalfRunMetres':'DHR-Met',
                }
stat_default = ['tries','tryAssists','allRuns','allRunMetres','linebreaks','linebreakAssists','tackleBreaks','supports','errors','tackles','missedTackles','effectiveTacklePercentage']

seasons_list = player_df.season.unique()

comps_dict = {'nrl': 111,
         'nswcup': 113,
         'qcup': 114,
         'origin': 116,
         'superleague': 121,
         'haroldmatthews': 143,
         'sgball': 144,
         'cyrilconnell': 154,
         'malmeninga': 155,
         'jerseyflegg': 159,
         'nrlw': 161}

positions_dict = {'Fullback': 'FB',
             'Winger': 'WG',
             'Centre': 'CT',
             'Five-Eighth': 'FE',
             'Halfback': 'HB',
             'Prop': 'PR',
             'Hooker': 'HK',
             '2nd Row': '2R',
             'Lock': 'LK',
             'Interchange': 'INT',
             'Replacement': '18TH',
             'Reserve': 'RES'}

with st.sidebar:
    st.header("Filters")

    #Summary
    summary_selection = st.selectbox("Summary Type", options=summary_list)

    #Comps
    comps_selection = st.multiselect("Competitions (none = ALL)",options=comps_dict.keys(),default=['nrl'])

    #Seasons
    season_selection = st.multiselect("Seasons (none = ALL)",options=seasons_list,default=[seasons_list.max()])
    season_separate = st.checkbox("Separate seasons")


    #Positions
    position_selection = st.multiselect("Positions (none = ALL)", options=positions_dict.keys(), default=[])
    position_separate = st.checkbox("Separate positions")

    #Teams
    if len(comps_selection) > 0:
        filtered_teams = team_df[team_df['compName'].isin(comps_selection)]
    else:
        filtered_teams = team_df
    team_options = filtered_teams['teamName']

    team_selection = st.multiselect("Teams (none = ALL)", options=team_options, default=[])
    team_separate = st.checkbox("Separate teams")

    #Min Games
    minimum_games_selection = st.number_input("Minimum games played", min_value=1)

    #Players
    filtered_players = player_df[['compName','season','teamName','playerId','playerName']].drop_duplicates()
    if len(comps_selection) > 0:
        filtered_players = filtered_players[filtered_players['compName'].isin(comps_selection)]
    if len(season_selection) > 0:
        filtered_players = filtered_players[filtered_players['season'].isin(season_selection)]
    if len(team_selection) > 0:
        filtered_players = filtered_players[filtered_players['teamName'].isin(team_selection)]
    player_options = filtered_players['playerName'].sort_values().unique().tolist()

    player_selection = st.multiselect("Players (none = ALL)",options=player_options, default=[])

    #Stats
    stat_selection = st.multiselect("Stats",options=stat_options,default=stat_default)

filters = {
    "summary_selection": summary_selection,
    "comps_selection": comps_selection,
    "season_selection": season_selection,
    "season_separate": season_separate,
    "position_selection": position_selection,
    "position_separate": position_separate,
    "team_selection": team_selection,
    "team_separate": team_separate,
    "minimum_games_selection": minimum_games_selection,
    "player_selection": player_selection,
    "stat_selection": stat_selection,
}

filtered_df = filter_player_data(player_df,filters,stat_options)

st.dataframe(filtered_df,use_container_width=True,height=600)

