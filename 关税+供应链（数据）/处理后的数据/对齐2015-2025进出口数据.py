import csv
from collections import defaultdict
from pathlib import Path

import openpyxl
from openpyxl.styles import Alignment, Font


BASE = Path(r"C:\Users\97328\Desktop\学习\论文、项目\供应链冲击\关税+供应链（数据）")
INPUT = BASE / "2015-2025进出口"
MAPPING = BASE / "所有行业和 hs2017 匹配（GB2017）" / "国民经济行业分类（GB2017）所有行业和hs2017匹配结果.xlsx"
OUTPUT = BASE / "处理后的数据" / "2015-2025进出口_含GB行业"
OUTPUT.mkdir(parents=True, exist_ok=True)

OUTPUT_HEADERS = ["商品编码", "商品名称", "贸易伙伴编码", "贸易伙伴名称", "人民币", "hs2017", "gb2017", "gb行业"]


def normalize_hs6(raw):
    value = "".join(str(raw or "").strip().split())
    if not value:
        return None
    digits = "".join(ch for ch in value if ch.isdigit())
    if not digits:
        return None
    # Raw customs codes are HS8, while the mapping workbook stores numeric
    # HS2017 codes without leading zeroes. Preserve already-short codes.
    return int(digits[:6]) if len(digits) > 6 else int(digits)


def number(raw):
    value = str(raw or "").strip().replace(",", "")
    if not value:
        return 0
    try:
        return float(value)
    except ValueError:
        return 0


def load_mapping():
    workbook = openpyxl.load_workbook(MAPPING, read_only=True, data_only=True)
    sheet = workbook.active
    headers = list(next(sheet.iter_rows(values_only=True)))
    positions = {str(value).strip(): index for index, value in enumerate(headers)}
    required = ["hs2017", "gb2017", "gb行业"]
    missing = [name for name in required if name not in positions]
    if missing:
        raise RuntimeError(f"Mapping columns missing: {missing}")
    mapping = {}
    conflicts = defaultdict(set)
    for row in sheet.iter_rows(min_row=2, values_only=True):
        hs = normalize_hs6(row[positions["hs2017"]])
        if hs is None:
            continue
        value = (row[positions["gb2017"]], row[positions["gb行业"]])
        conflicts[hs].add(value)
        mapping.setdefault(hs, value)
    conflicting = {hs: values for hs, values in conflicts.items() if len(values) > 1}
    return mapping, conflicting


def read_and_aggregate(path):
    grouped = {}
    with path.open("r", encoding="gb18030", newline="") as handle:
        reader = csv.DictReader(handle)
        required = ["商品编码", "商品名称", "贸易伙伴编码", "贸易伙伴名称", "人民币"]
        missing = [name for name in required if name not in reader.fieldnames]
        if missing:
            raise RuntimeError(f"{path.name}: missing columns {missing}")
        rows = 0
        months = set()
        for row in reader:
            rows += 1
            months.add(str(row.get("数据年月", "")).strip())
            product_raw = str(row.get("商品编码", "")).strip()
            partner_code = str(row.get("贸易伙伴编码", "")).strip()
            key = (product_raw, partner_code)
            if key not in grouped:
                grouped[key] = {
                    "商品编码": int(product_raw) if product_raw.isdigit() else product_raw,
                    "商品名称": str(row.get("商品名称", "")).strip(),
                    "贸易伙伴编码": int(partner_code) if partner_code.isdigit() else partner_code,
                    "贸易伙伴名称": str(row.get("贸易伙伴名称", "")).strip(),
                    "人民币": 0,
                }
            grouped[key]["人民币"] += number(row.get("人民币"))
    return list(grouped.values()), rows, sorted(months)


def write_workbook(path, rows):
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "Sheet1"
    sheet.append(OUTPUT_HEADERS)
    for cell in sheet[1]:
        cell.font = Font(bold=True)
        cell.alignment = Alignment(horizontal="center")
    for row in rows:
        sheet.append([row.get(header) for header in OUTPUT_HEADERS])
    widths = [14, 34, 16, 18, 18, 12, 12, 22]
    for index, width in enumerate(widths, start=1):
        sheet.column_dimensions[openpyxl.utils.get_column_letter(index)].width = width
    sheet.freeze_panes = "A2"
    sheet.auto_filter.ref = sheet.dimensions
    workbook.save(path)


def main():
    mapping, conflicts = load_mapping()
    all_rows = []
    report = []
    for csv_path in sorted(INPUT.glob("*.csv")):
        year = csv_path.stem
        rows, source_rows, months = read_and_aggregate(csv_path)
        unmatched = 0
        for row in rows:
            hs = normalize_hs6(row["商品编码"])
            row["hs2017"] = hs
            row["gb2017"], row["gb行业"] = mapping.get(hs, (None, None))
            if hs not in mapping:
                unmatched += 1
            all_rows.append({"year": int(year), **row})
        output_path = OUTPUT / f"{year}年合并结果_含GB行业.xlsx"
        write_workbook(output_path, rows)
        report.append((year, source_rows, len(rows), ",".join(months), unmatched))

    combined_path = OUTPUT / "2015-2025合并结果_含GB行业.xlsx"
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "Sheet1"
    combined_headers = ["year"] + OUTPUT_HEADERS
    sheet.append(combined_headers)
    for cell in sheet[1]:
        cell.font = Font(bold=True)
    for row in all_rows:
        sheet.append([row.get(header) for header in combined_headers])
    for index, width in enumerate([10, 14, 34, 16, 18, 18, 12, 12, 22], start=1):
        sheet.column_dimensions[openpyxl.utils.get_column_letter(index)].width = width
    sheet.freeze_panes = "A2"
    sheet.auto_filter.ref = sheet.dimensions
    workbook.save(combined_path)

    report_path = OUTPUT / "对齐处理报告.csv"
    with report_path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["年份", "原始行数", "商品×伙伴聚合后行数", "数据年月", "未匹配GB行业行数"])
        writer.writerows(report)
    readme = OUTPUT / "README.md"
    readme.write_text(
        "# 2015至2025进出口数据对齐结果\n\n"
        "处理方式：按 `商品编码` 与 `贸易伙伴编码` 汇总人民币金额，计算 HS2017 六位编码，并按照既有 `HS2017 → GB2017` 映射补充 `gb2017` 和 `gb行业`。每个年度文件保持参考文件的八列格式。\n\n"
        "重要数据限制：当前输入目录中的每个年度 CSV 都是 10,000 行，且 `数据年月` 仅包含该年度 1 月。这说明当前下载结果很可能是分页首批数据，不应解释为完整年度数据。完整年度数据补齐后，重新运行同一脚本即可生成完整结果。\n\n"
        "`2015-2025合并结果_含GB行业.xlsx` 额外保留 `year` 列，便于跨年度使用；各年度文件不含 year 列，以保持与参考 Excel 完全一致。处理明细见 `对齐处理报告.csv`。\n",
        encoding="utf-8",
    )
    print(f"OUTPUT: {OUTPUT}")
    print(f"YEAR_FILES: {len(report)}")
    print(f"COMBINED_ROWS: {len(all_rows)}")
    print(f"MAPPING_CONFLICT_HS: {len(conflicts)}")
    for item in report:
        print("REPORT:", *item)


if __name__ == "__main__":
    main()
