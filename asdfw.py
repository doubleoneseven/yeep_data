import os
import pandas as pd
import numpy as np

# 원본 데이터 파일 경로와 전처리 후 파일 저장 경로
input_file_path = r"C:\YEEP_test_Samplercode\yyeepp.csv"
output_file_path = r"C:\Users\gocom\OneDrive\바탕 화면\yqp\processed_data.csv"

# 디렉터리가 없으면 생성
os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

# 데이터 불러오기
data = pd.read_csv(input_file_path)

# 시간 변수 전처리: 시간이 1부터 시작하여 1씩 증가하도록 조정
data['TIME'] = range(1, len(data) + 1)

# 1. Total Time (total_time): 전체 작업 수행 시간
total_time = len(data)

# 2. Air Time (air_time): 공중에서 움직인 시간 (BUTTON이 0일 때)
air_time = len(data[data['BUTTON'] == 0])

# 3. Paper Time (paper_time): 종이 위에서 움직인 시간 (BUTTON이 1일 때)
paper_time = len(data[data['BUTTON'] == 1])

# 4. 종이 위에서의 평균 속도 (mean_speed_on_paper)
data['distance'] = np.sqrt(data['X'].diff()**2 + data['Y'].diff()**2)
data['speed'] = data['distance'] / data['TIME'].diff()
mean_speed_on_paper = data[data['BUTTON'] == 1]['speed'].mean()

# 5. 공중에서의 평균 속도 (mean_speed_in_air)
mean_speed_in_air = data[data['BUTTON'] == 0]['speed'].mean()

# 6. 종이 위에서의 평균 가속도 (mean_acc_on_paper, 절대값)
data['acceleration'] = data['speed'].diff().abs() / data['TIME'].diff()
mean_acc_on_paper = data[data['BUTTON'] == 1]['acceleration'].mean()

# 7. 공중에서의 평균 가속도 (mean_acc_in_air, 절대값)
mean_acc_in_air = data[data['BUTTON'] == 0]['acceleration'].mean()

# 8. 종이 위에서의 평균 가가속도 (mean_jerk_on_paper, 절대값)
data['jerk'] = data['acceleration'].diff().abs() / data['TIME'].diff()
mean_jerk_on_paper = data[data['BUTTON'] == 1]['jerk'].mean()

# 9. 공중에서의 평균 가가속도 (mean_jerk_in_air, 절대값)
mean_jerk_in_air = data[data['BUTTON'] == 0]['jerk'].mean()

# 10. 펜의 평균 압력 (pressure_mean)
pressure_mean = data['PRESSURE_NORMAL'].mean()

# 11. 펜 압력의 분산 (pressure_var)
pressure_var = data['PRESSURE_NORMAL'].var()

# 12. 종이 위에서의 GMRT (gmrt_on_paper)
data['GMRT_diff'] = np.sqrt(data['X'].diff()**2 + data['Y'].diff()**2)
gmrt_on_paper = (1 / (len(data[data['BUTTON'] == 1]) - 1)) * data[data['BUTTON'] == 1]['GMRT_diff'].abs().sum()

# 13. 공중에서의 GMRT (gmrt_in_air)
gmrt_in_air = (1 / (len(data[data['BUTTON'] == 0]) - 1)) * data[data['BUTTON'] == 0]['GMRT_diff'].abs().sum()

# 14. Mean GMRT (mean_gmrt): gmrt_on_paper와 gmrt_in_air의 평균
mean_gmrt = (gmrt_on_paper + gmrt_in_air) / 2

# 15. 펜이 종이에 닿은 횟수 (num_of_pendown)
num_of_pendown = data['BUTTON'].diff().abs().sum() // 2

# 16. X축 최대 확장 (max_x_extension)
max_x_extension = data['X'].max()

# 17. Y축 최대 확장 (max_y_extension)
max_y_extension = data['Y'].max()

# 가속도 스케일링: mean_acc_on_paper와 mean_acc_in_air를 1~10 사이로 변환
min_acc = min(mean_acc_on_paper, mean_acc_in_air)
max_acc = max(mean_acc_on_paper, mean_acc_in_air)

scaled_mean_acc_on_paper = 1 + 9 * (mean_acc_on_paper - min_acc) / (max_acc - min_acc) if max_acc != min_acc else 5
scaled_mean_acc_in_air = 1 + 9 * (mean_acc_in_air - min_acc) / (max_acc - min_acc) if max_acc != min_acc else 5

# 결과를 DataFrame으로 정리 (요청 순서에 맞게 정렬)
processed_data = pd.DataFrame({
    'air_time': [air_time],
    'gmrt_in_air': [gmrt_in_air],
    'gmrt_on_paper': [gmrt_on_paper],
    'max_x_extension': [max_x_extension],
    'max_y_extension': [max_y_extension],
    'mean_acc_in_air': [scaled_mean_acc_in_air],
    'mean_acc_on_paper': [scaled_mean_acc_on_paper],
    'mean_gmrt': [mean_gmrt],
    'mean_jerk_in_air': [mean_jerk_in_air],
    'mean_jerk_on_paper': [mean_jerk_on_paper],
    'mean_speed_in_air': [mean_speed_in_air],
    'mean_speed_on_paper': [mean_speed_on_paper],
    'num_of_pendown': [num_of_pendown],
    'paper_time': [paper_time],
    'pressure_mean': [pressure_mean],
    'pressure_var': [pressure_var],
    'total_time': [total_time]
})

# 전처리된 데이터 CSV 파일로 저장
processed_data.to_csv(output_file_path, index=False)
