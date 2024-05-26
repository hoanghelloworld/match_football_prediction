import numpy as np
import pandas as pd
import pickle
from sklearn import preprocessing
import matplotlib.pyplot as plt

def calculate_rolling_averages_home_l5m(df, team, n=5):
    # Các cột sẽ không tính toán trung bình
    exclude_columns = ['FTR', 'HomeTeam', 'AwayTeam']
    
    # Lọc DataFrame cho các hàng mà đội được chỉ định là đội nhà
    team_df = df[(df['HomeTeam'] == team)]
    
    # Các cột để tính toán trung bình 
    columns_to_average = team_df.columns.difference(exclude_columns)
    
    # Tính toán trung bình cho các cột được chỉ định
    rolling_stats = team_df[columns_to_average].rolling(window=n).mean().shift(1)
    
    # Nối thông tin đội với các thống kê 
    rolling_stats = pd.concat([team_df[exclude_columns], rolling_stats], axis=1)
    
    return rolling_stats
def calculate_rolling_averages_away_l5m(df, team, n=5):
    # Các cột sẽ không tính toán trung bình 
    exclude_columns = ['FTR', 'HomeTeam', 'AwayTeam']
    
    # Lọc DataFrame cho các hàng mà đội được chỉ định là đội khách
    team_df = df[(df['AwayTeam'] == team)]
    
    # Các cột để tính toán trung bình 
    columns_to_average = team_df.columns.difference(exclude_columns)
    
    # Tính toán trung bình cho các cột được chỉ định
    rolling_stats = team_df[columns_to_average].rolling(window=n).mean().shift(1)
    
    # Nối thông tin đội với các thống kê 
    rolling_stats = pd.concat([team_df[exclude_columns], rolling_stats], axis=1)
    
    return rolling_stats
def calculate_rolling_averages_home_l10m(df, team, n=10):
    # Các cột sẽ không tính toán trung bình
    exclude_columns = ['FTR', 'HomeTeam', 'AwayTeam']
    
    # Lọc DataFrame cho các hàng mà đội được chỉ định là đội nhà
    team_df = df[(df['HomeTeam'] == team)]
    
    # Các cột để tính toán trung bình 
    columns_to_average = team_df.columns.difference(exclude_columns)
    
    # Tính toán trung bình cho các cột được chỉ định
    rolling_stats = team_df[columns_to_average].rolling(window=n).mean().shift(1)
    
    # Nối thông tin đội với các thống kê 
    rolling_stats = pd.concat([team_df[exclude_columns], rolling_stats], axis=1)
    
    return rolling_stats
def calculate_rolling_averages_away_l10m(df, team, n=10):
    # Các cột sẽ không tính toán trung bình 
    exclude_columns = ['FTR', 'HomeTeam', 'AwayTeam']
    
    # Lọc DataFrame cho các hàng mà đội được chỉ định là đội khách
    team_df = df[(df['AwayTeam'] == team)]
    
    # Các cột để tính toán trung bình 
    columns_to_average = team_df.columns.difference(exclude_columns)
    
    # Tính toán trung bình cho các cột được chỉ định
    rolling_stats = team_df[columns_to_average].rolling(window=n).mean().shift(1)
    
    # Nối thông tin đội với các thống kê 
    rolling_stats = pd.concat([team_df[exclude_columns], rolling_stats], axis=1)
    
    return rolling_stats
def prepare_dataset_away_l5m(data, teams):
    # Danh sách để lưu trữ dữ liệu cho tất cả các đội
    all_data = []
    # Lặp qua từng đội trong danh sách các đội
    for team in teams:
        # Tính toán các chỉ số trung bình cuộn cho đội khách
        rolling_stats = calculate_rolling_averages_away_l5m(data, team)
        # Thêm các chỉ số trung bình cuộn vào danh sách
        all_data.append(rolling_stats)
    # Kết hợp tất cả các dữ liệu lại thành một DataFrame duy nhất
    return pd.concat(all_data)
def prepare_dataset_home_l5m(data, teams):
    # Danh sách để lưu trữ dữ liệu cho tất cả các đội
    all_data = []
    # Lặp qua từng đội trong danh sách các đội
    for team in teams:
        # Tính toán các chỉ số trung bình cuộn cho đội nhà
        rolling_stats = calculate_rolling_averages_home_l5m(data, team)
        # Thêm các chỉ số trung bình cuộn vào danh sách
        all_data.append(rolling_stats)
    # Kết hợp tất cả các dữ liệu lại thành một DataFrame duy nhất
    return pd.concat(all_data)
def prepare_dataset_away_l10m(data, teams):
    # Danh sách để lưu trữ dữ liệu cho tất cả các đội
    all_data = []
    # Lặp qua từng đội trong danh sách các đội
    for team in teams:
        # Tính toán các chỉ số trung bình cuộn cho đội khách
        rolling_stats = calculate_rolling_averages_away_l10m(data, team)
        # Thêm các chỉ số trung bình cuộn vào danh sách
        all_data.append(rolling_stats)
    # Kết hợp tất cả các dữ liệu lại thành một DataFrame duy nhất
    return pd.concat(all_data)
def prepare_dataset_home_l10m(data, teams):
    # Danh sách để lưu trữ dữ liệu cho tất cả các đội
    all_data = []
    # Lặp qua từng đội trong danh sách các đội
    for team in teams:
        # Tính toán các chỉ số trung bình cuộn cho đội nhà
        rolling_stats = calculate_rolling_averages_home_l10m(data, team)
        # Thêm các chỉ số trung bình cuộn vào danh sách
        all_data.append(rolling_stats)
    # Kết hợp tất cả các dữ liệu lại thành một DataFrame duy nhất
    return pd.concat(all_data)
