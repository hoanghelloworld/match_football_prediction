import urllib.request
import json
import pandas as pd
import numpy as np
# Make the request to the API
req = urllib.request.Request('https://livescore-api.com/api-client/matches/live.json?&key=EK1eku7elS97TWeu&secret=Mftt1BgcE8KJzGLdqMsLhz0CsaKl6YPT')
response = urllib.request.urlopen(req)
# Read the response and convert it from JSON to a Python dictionary
data = json.loads(response.read())
# Assuming the relevant data is in a key named 'data' (you will need to adjust this based on the actual structure of the JSON response)
# Convert the dictionary to a pandas DataFrame
dframe = pd.DataFrame(data['data']['match'])
dframe['home_id'] = dframe['home'].apply(lambda x: x['id'])
dframe['away_id'] = dframe['away'].apply(lambda x: x['id'])
dframe['home_name'] = dframe['home'].apply(lambda x: x['name'])
dframe['away_name'] = dframe['away'].apply(lambda x: x['name'])

dframe['score'] = dframe['scores'].apply(lambda x: x['score'])
columns_to_drop = ['federation','competition','scheduled','country','odds','added','last_changed','away','home','outcomes','scores','urls']
# Loại bỏ các cột không mong muốn
dframe = dframe.drop(columns=columns_to_drop)
pd.set_option('display.max_columns', None)
dframe['team1.overall_form'] = None
dframe['team1.h2h_form'] = None
dframe['team2.overall_form'] = None
dframe['team2.h2h_form'] = None

# Function to make the request to the API
def fetch_head2head_data(team1_id, team2_id):
    url = f'https://livescore-api.com/api-client/teams/head2head.json?team1_id={team1_id}&team2_id={team2_id}&key=h5v5oR8HzTPeQ41G&secret=3I0FK43hPoL81itjoZoMRxuqqjEgoGXr'
    req = urllib.request.Request(url)
    response = urllib.request.urlopen(req)
    data = json.loads(response.read())
    df = pd.DataFrame(data)
    return df

# Function to extract and normalize JSON data
def extract_and_normalize(json_data):
    normalized_data = pd.json_normalize(json_data)
    return normalized_data

# Iterate over each row in the DataFrame
# Create an empty list to store the row data
row_data = []

for index, row in dframe.iterrows():
    team1_id = row['home_id']
    team2_id = row['away_id']
    
    # Fetch data from the API
    df = fetch_head2head_data(team1_id, team2_id)
    
    # Extract and normalize the data
    team1_overall_form = df['data'].iloc[0]
    team1_h2h_form = df['data'].iloc[0]
    team2_overall_form = df['data'].iloc[1]
    team2_h2h_form = df['data'].iloc[1]
    
    # Normalize the data
    team1_overall_form = pd.json_normalize(team1_overall_form)
    team1_h2h_form = pd.json_normalize(team1_h2h_form)
    team2_overall_form = pd.json_normalize(team2_overall_form)
    team2_h2h_form = pd.json_normalize(team2_h2h_form)
    
    # Update the original DataFrame
    dframe.at[index, 'team1.overall_form'] = team1_overall_form['overall_form'].iloc[0]
    dframe.at[index, 'team1.h2h_form'] = team1_h2h_form['h2h_form'].iloc[0]
    dframe.at[index, 'team2.overall_form'] = team2_overall_form['overall_form'].iloc[0]
    dframe.at[index, 'team2.h2h_form'] = team2_h2h_form['h2h_form'].iloc[0]

df=dframe.copy()
def calculate_ratios(form):
    win_count = form.count('W')
    draw_count = form.count('D')
    loss_count = form.count('L')
    total = len(form)
    win_ratio = win_count / 6
    draw_ratio = draw_count / 6
    loss_ratio = loss_count / 6
    return win_ratio, draw_ratio, loss_ratio
df['team1.overall_win_ratio'], df['team1.overall_draw_ratio'], df['team1.overall_loss_ratio'] = zip(*df['team1.overall_form'].apply(calculate_ratios))
df['team1.h2h_win_ratio'], df['team1.h2h_draw_ratio'], df['team1.h2h_loss_ratio'] = zip(*df['team1.h2h_form'].apply(calculate_ratios))
df['team2.overall_win_ratio'], df['team2.overall_draw_ratio'], df['team2.overall_loss_ratio'] = zip(*df['team2.overall_form'].apply(calculate_ratios))
df['team2.h2h_win_ratio'], df['team2.h2h_draw_ratio'], df['team2.h2h_loss_ratio'] = zip(*df['team2.h2h_form'].apply(calculate_ratios))
columns_to_keep = ['home_id','away_id','team1.overall_win_ratio', 'team1.overall_draw_ratio', 'team1.overall_loss_ratio',
                   'team1.h2h_win_ratio', 'team1.h2h_draw_ratio', 'team1.h2h_loss_ratio',
                   'team2.overall_draw_ratio','team2.overall_loss_ratio','team2.h2h_win_ratio',
                   'team2.h2h_draw_ratio','team2.h2h_loss_ratio']
df = df[columns_to_keep]

# Assuming your DataFrame is named 'dfram' and has a column named 'match_id'
api_key = 'EK1eku7elS97TWeu'
api_secret = 'Mftt1BgcE8KJzGLdqMsLhz0CsaKl6YPT'

# Create an empty list to store the DataFrames for each match
match_data_list = []

# Iterate over each row in the DataFrame
for index, row in dframe.iterrows():
    match_id = row['id']

    # Make the request to the API
    url = f'https://livescore-api.com/api-client/matches/stats.json?match_id={match_id}&key={api_key}&secret={api_secret}'
    req = urllib.request.Request(url)
    response = urllib.request.urlopen(req)
    # Read the response and convert it from JSON to a Python dictionary
    data = json.loads(response.read())
    # Assuming the relevant data is in a key named 'data' (adjust based on the actual JSON structure)
    # Convert the dictionary to a pandas DataFrame
    # Modify the line to include an index
    match_df = pd.DataFrame(data['data'], index=[match_id])
    # Add the match_id as a column to the DataFrame
    match_df['match_id'] = match_id
    # Append the DataFrame to the list
    match_data_list.append(match_df)
# Concatenate all the DataFrames into a single DataFrame
final_df = pd.concat(match_data_list, ignore_index=True)

def split_and_add_columns(final_df, dframe):
    # Define the columns to be split
    columns_to_split = [
        'yellow_cards', 'red_cards', 'substitutions', 'possesion', 'free_kicks',
        'goal_kicks', 'throw_ins', 'offsides', 'corners', 'shots_on_target',
        'shots_off_target', 'attempts_on_goal', 'saves', 'fauls', 'treatments',
        'penalties', 'shots_blocked', 'dangerous_attacks', 'attacks'
    ]

    # Iterate through each row in final_df
    for _, row in final_df.iterrows():
        match_id = row['match_id']

        # Find the corresponding row in dframe
        dframe_row = dframe[dframe['id'] == match_id]

        if not dframe_row.empty:
            index = dframe_row.index[0]

            # Split the values and add them to dframe
            for col in columns_to_split:
                if pd.notna(row[col]):
                    home_value, away_value = row[col].split(':')
                    dframe.at[index, f'home_{col}'] = home_value
                    dframe.at[index, f'away_{col}'] = away_value
                else:
                    dframe.at[index, f'home_{col}'] = None
                    dframe.at[index, f'away_{col}'] = None

# Apply the function
split_and_add_columns(final_df, dframe)
merged_df = pd.merge(dframe, df, on=['home_id', 'away_id'], how='left')
merged_df=merged_df.drop(columns=['team1.overall_form',	'team1.h2h_form','team2.overall_form','team2.h2h_form'])
merged_df=merged_df.fillna(0)
# Split the 'score' column into 'ht_score_home' and 'ht_score_team'
merged_df['score'] = merged_df['score'].replace('? - ?', '0-0')

# Split the 'score' column into 'ht_score_home' and 'ht_score_team'
merged_df[['ht_score_home', 'ht_score_team']] = merged_df['score'].str.split('-', expand=True)

# Convert the new columns to integers
merged_df['ht_score_home'] = merged_df['ht_score_home'].astype(float)
merged_df['ht_score_team'] = merged_df['ht_score_team'].astype(float)

# Drop the original 'score' column if no longer needed
merged_df.drop(columns=['score'], inplace=True)
merged_df.rename(columns={
    'home_yellow_cards': 'yellow_cards_home',
    'away_yellow_cards': 'yellow_cards_away',
    'home_red_cards': 'red_cards_home',
    'away_red_cards': 'red_cards_away',
    'home_possesion': 'possesion_home',
    'away_possesion': 'possesion_away',
    'home_corners': 'corners_home',
    'away_corners': 'corners_away',
    'home_shots_on_target': 'shots_on_target_home',
    'away_shots_on_target': 'shots_on_target_away',
    'home_shots_off_target': 'shots_off_target_home',
    'away_shots_off_target': 'shots_off_target_away',
    'home_dangerous_attacks': 'dangerous_attacks_home',
    'away_dangerous_attacks': 'dangerous_attacks_away',
    'home_attacks': 'attacks_home',
    'away_attacks': 'attacks_away',
    'home_offsides': 'offsides_home',
    'away_offsides': 'offsides_away',
    'home_attempts_on_goal': 'attempts_on_goal_home',
    'away_attempts_on_goal': 'attempts_on_goal_away',
    'home_saves': 'saves_home',
    'away_saves': 'saves_away',
    'home_fauls': 'fauls_home',
    'away_fauls': 'fauls_away',
    'home_shots_blocked': 'shots_blocked_home',
    'away_shots_blocked': 'shots_blocked_away',
    'home_free_kicks': 'free_kicks_home',
    'away_free_kicks': 'free_kicks_away',
    'home_throw_ins': 'throw_ins_home',
    'away_throw_ins': 'throw_ins_away',
    'home_penalties': 'penalties_home',
    'away_penalties': 'penalties_away',
    'home_substitutions': 'substitutions_home',
    'away_substitutions': 'substitutions_away',
    'home_goal_kicks': 'goal_kicks_home',
    'away_goal_kicks': 'goal_kicks_away',
    'home_treatments': 'treatments_home',
    'away_treatments': 'treatments_away',
    'ht_score_team': 'ht_score_away'
}, inplace=True)

# Reorder columns
new_order = [
    'home_name', 'away_name', 'yellow_cards_home', 'yellow_cards_away', 'red_cards_home', 'red_cards_away',
    'possesion_home', 'possesion_away', 'corners_home', 'corners_away', 'shots_on_target_home', 'shots_on_target_away',
    'shots_off_target_home', 'shots_off_target_away', 'dangerous_attacks_home', 'dangerous_attacks_away',
    'attacks_home', 'attacks_away', 'offsides_home', 'offsides_away', 'attempts_on_goal_home', 'attempts_on_goal_away',
    'saves_home', 'saves_away', 'fauls_home', 'fauls_away', 'shots_blocked_home', 'shots_blocked_away',
    'free_kicks_home', 'free_kicks_away', 'throw_ins_home', 'throw_ins_away', 'penalties_home', 'penalties_away',
    'substitutions_home', 'substitutions_away', 'goal_kicks_home', 'goal_kicks_away', 'treatments_home', 'treatments_away', 'ht_score_home', 'ht_score_away', 'team1.overall_win_ratio', 'team1.overall_draw_ratio',
    'team1.overall_loss_ratio', 'team1.h2h_win_ratio', 'team1.h2h_draw_ratio', 'team1.h2h_loss_ratio',
    'team2.overall_draw_ratio', 'team2.overall_loss_ratio', 'team2.h2h_win_ratio', 'team2.h2h_draw_ratio', 'team2.h2h_loss_ratio'
]

merged_df = merged_df[new_order]
import pandas as pd
# Các cột không cần chia giá trị
exclude_columns = ['home_name', 'away_name',
    'team1.overall_win_ratio', 'team1.overall_draw_ratio', 'team1.overall_loss_ratio',
    'team1.h2h_win_ratio', 'team1.h2h_draw_ratio', 'team1.h2h_loss_ratio',
    'team2.overall_draw_ratio', 'team2.overall_loss_ratio',
    'team2.h2h_win_ratio', 'team2.h2h_draw_ratio', 'team2.h2h_loss_ratio']
columns_to_divide = [col for col in merged_df.columns if col not in exclude_columns]

# Convert columns to numeric, coercing errors to NaN
merged_df[columns_to_divide] = merged_df[columns_to_divide].apply(pd.to_numeric, errors='coerce')
# Perform the division operation
merged_df[columns_to_divide] = merged_df[columns_to_divide].div(2)
from flask import Flask, render_template
import pandas as pd
import joblib
best_rf_loaded = joblib.load(r'/workspaces/match_football_prediction/dangdienra/best_model.joblib')
app = Flask(__name__)
merged_df = merged_df.join(dframe[['location', 'status', 'time']])
@app.route('/')
def home():
    if 'outcome' in merged_df.columns:
        X = merged_df.drop(columns=['home_name', 'away_name', 'outcome', 'location', 'status', 'time'])
    else:
        X = merged_df.drop(columns=['home_name', 'away_name', 'location', 'status', 'time'])
    
    predictions = best_rf_loaded.predict(X)
    outcome_map = {0: 'draw', 1: 'home win', -1: 'away win'}
    merged_df['outcome'] = [outcome_map[pred] for pred in predictions]
    
    # Chọn các cột cần hiển thị
    columns_to_display = ['home_name', 'away_name', 'location', 'status', 'time', 'outcome']
    hidden_columns = ['yellow_cards_home', 'yellow_cards_away', 'red_cards_home', 'red_cards_away', 
                      'possesion_home', 'possesion_away', 'corners_home', 'corners_away', 
                      'shots_on_target_home', 'shots_on_target_away', 'shots_off_target_home', 
                      'shots_off_target_away', 'dangerous_attacks_home', 'dangerous_attacks_away', 
                      'attacks_home', 'attacks_away', 'offsides_home', 'offsides_away', 
                      'attempts_on_goal_home', 'attempts_on_goal_away', 'saves_home', 'saves_away', 
                      'fauls_home', 'fauls_away', 'shots_blocked_home', 'shots_blocked_away', 
                      'free_kicks_home', 'free_kicks_away', 'throw_ins_home', 'throw_ins_away', 
                      'penalties_home', 'penalties_away', 'substitutions_home', 'substitutions_away', 
                      'goal_kicks_home', 'goal_kicks_away', 'treatments_home', 'treatments_away', 
                      'ht_score_home', 'ht_score_away', 'team1.overall_win_ratio', 
                      'team1.overall_draw_ratio', 'team1.overall_loss_ratio', 'team1.h2h_win_ratio', 
                      'team1.h2h_draw_ratio', 'team1.h2h_loss_ratio', 'team2.overall_draw_ratio', 
                      'team2.overall_loss_ratio', 'team2.h2h_win_ratio', 'team2.h2h_draw_ratio', 
                      'team2.h2h_loss_ratio']
    
    # Thêm cột nút hiển thị
    merged_df['show_details'] = '<button onclick="toggleDetails(this)">Show Details</button>'
    columns_to_display.append('show_details')
    
    # Thêm lớp CSS cho các cột ẩn
    for col in hidden_columns:
        merged_df[col] = merged_df[col].apply(lambda x: f'<span class="hidden-column">{x}</span>')
    
    # Trả về kết quả dưới dạng HTML với các cột đã chọn
    return render_template('index.html', tables=[merged_df[columns_to_display + hidden_columns].to_html(classes='data', header=True, escape=False)])

if __name__ == '__main__':
    app.run(debug=True)