import re
import os

def extract_tariff_codes(pdf_path):
    from PyPDF2 import PdfReader
    pattern = r'\b\d{1,4}\.\d{1,2}\.\d{1,2}\b'
    tariff_codes = set()
    
    with open(pdf_path, 'rb') as file:
        reader = PdfReader(file)
        for page in reader.pages:
            text = page.extract_text()
            if text:
                matches = re.findall(pattern, text)
                tariff_codes.update(matches)
    
    return sorted(list(tariff_codes))

def save_to_txt(codes, output_path):
    with open(output_path, 'w', encoding='utf-8') as f:
        for code in codes:
            f.write(code + '\n')

if __name__ == '__main__':
    pdf_path = r'E:\科研\关税与供应链\处理税率数据\301附加关税\2019年9月1日-清单4.pdf'
    output_path = pdf_path.replace('.pdf', '.txt')
    
    codes = extract_tariff_codes(pdf_path)
    save_to_txt(codes, output_path)
    
    print(f'提取完成，共找到 {len(codes)} 个编码')
    print(f'已保存到: {output_path}')
