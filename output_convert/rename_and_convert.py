import os
import json
import pandas as pd

# 指定文件夹路径
folder_path = r'file_path'

# 遍历文件夹中的所有文件
for filename in os.listdir(folder_path):
    if filename.endswith('.json'):
        file_path = os.path.join(folder_path, filename)
        
        # 读取JSON文件
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        # 获取metadata信息
        metadata = data.get('metadata', {})
        otree_session = metadata.get('otree_session', 'unknown')
        participant = metadata.get('participant', 'unknown')
        participant_code = metadata.get('participant_code', 'unknown')
        participant_label = metadata.get('participant_label', 'unknown')
        
        # 创建新文件名
        new_filename = f"{metadata.get('otree_session_label', 'unknown')}--{participant}--{participant_code}--{participant_label}.json"
        new_file_path = os.path.join(folder_path, new_filename)
        
        # 重命名文件
        os.rename(file_path, new_file_path)
        print(f"重命名文件: {filename} -> {new_filename}")
        
        # 将JSON数据保存为CSV文件
        csv_filename = new_filename.replace('.json', '.csv')
        csv_file_path = os.path.join(folder_path, csv_filename)
        
        # 将数据转换为DataFrame并添加新列
        df = pd.DataFrame(data['history'])
        df['otree_session'] = otree_session
        df['participant_label'] = participant_label
        
        df = df.map(lambda x: x.replace('\n', '').replace('\r', '').replace(' ','') if isinstance(x, str) else x)
        # 重新排列列的顺序
        df = df[['otree_session', 'participant_label'] + df.columns[:-2].tolist()]
        
        # 保存为CSV
        df.to_csv(csv_file_path, index=False)
        print(f"保存为CSV文件: {new_filename} -> {csv_filename}")
