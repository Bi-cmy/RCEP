import os
import pandas as pd

input_dir = r"e:\科研\关税与供应链\处理税率数据\基础税率\extracted_data"
output_dir = r"e:\科研\关税与供应链\处理税率数据\基础税率\processed_data"

os.makedirs(output_dir, exist_ok=True)

excel_files = [f for f in os.listdir(input_dir) if f.endswith(('.xlsx', '.xls')) and not f.startswith('~$')]

for excel_file in excel_files:
    file_path = os.path.join(input_dir, excel_file)
    
    try:
        print(f"Processing: {excel_file}")
        df = pd.read_excel(file_path)
        
        if 'mfn_ad_val_rate' in df.columns:
            original_count = (df['mfn_ad_val_rate'] > 1).sum()
            
            if original_count > 0:
                df_valid = df[df['mfn_ad_val_rate'] <= 1]
                
                mean_value = df_valid['mfn_ad_val_rate'].mean()
                
                print(f"  Found {original_count} values greater than 1")
                print(f"  Mean value (excluding values > 1): {mean_value:.4f}")
                
                df.loc[df['mfn_ad_val_rate'] > 1, 'mfn_ad_val_rate'] = mean_value
                
                replaced_count = (df['mfn_ad_val_rate'] == mean_value).sum()
                print(f"  Replaced {replaced_count} values with mean")
            else:
                print(f"  No values greater than 1 found in this file")
        else:
            print(f"  Warning: 'mfn_ad_val_rate' column not found in {excel_file}")
        
        output_path = os.path.join(output_dir, excel_file)
        df.to_excel(output_path, index=False)
        print(f"  Saved to: {output_path}")
        print(f"  Total rows: {len(df)}")
        print()
        
    except Exception as e:
        print(f"  Error processing {excel_file}: {str(e)}")
        print()

print("Processing completed!")
