import os
import pandas as pd

base_dir = r"e:\科研\关税与供应链\处理税率数据\基础税率\2015-2025 dataweb- annual tariff data"
output_dir = r"e:\科研\关税与供应链\处理税率数据\基础税率\extracted_data"

columns_to_extract = ["hts8", "mfn_ad_val_rate", "begin_effect_date", "end_effective_date"]

os.makedirs(output_dir, exist_ok=True)

year_folders = [f for f in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, f))]

for year_folder in year_folders:
    folder_path = os.path.join(base_dir, year_folder)
    
    excel_files = [f for f in os.listdir(folder_path) if f.endswith(('.xlsx', '.xls')) and not f.startswith('~$')]
    
    for excel_file in excel_files:
        file_path = os.path.join(folder_path, excel_file)
        
        try:
            print(f"Processing: {excel_file}")
            df = pd.read_excel(file_path)
            
            available_columns = [col for col in columns_to_extract if col in df.columns]
            
            if len(available_columns) == len(columns_to_extract):
                extracted_df = df[columns_to_extract].copy()
            else:
                extracted_df = df[available_columns].copy()
                missing_columns = set(columns_to_extract) - set(available_columns)
                print(f"  Warning: Missing columns in {excel_file}: {missing_columns}")
            
            output_filename = f"extracted_{excel_file}"
            output_path = os.path.join(output_dir, output_filename)
            
            extracted_df.to_excel(output_path, index=False)
            print(f"  Saved to: {output_filename}")
            print(f"  Rows: {len(extracted_df)}")
            
        except Exception as e:
            print(f"  Error processing {excel_file}: {str(e)}")

print("\nProcessing completed!")
