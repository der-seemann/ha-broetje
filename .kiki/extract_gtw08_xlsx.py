#!/usr/bin/env python3
"""Extract GTW-08 Modbus register rows from the vendor XLSX without openpyxl."""
from __future__ import annotations

import csv
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from zipfile import ZipFile

XLSX = Path("GTW-08-Modbus-parameterlijst.xlsx")
OUT = Path(".kiki/cache/extracted/GTW-08-Modbus-parameterlijst_extracted_registers.csv")
NS = {
    "m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
}
REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"


def col_to_idx(cell_ref: str) -> int:
    letters = "".join(ch for ch in cell_ref if ch.isalpha())
    n = 0
    for ch in letters:
        n = n * 26 + (ord(ch.upper()) - 64)
    return n - 1


def norm(s: object) -> str:
    return re.sub(r"\s+", " ", str(s or "").replace("\xa0", " ")).strip()


def load_shared_strings(z: ZipFile) -> list[str]:
    if "xl/sharedStrings.xml" not in z.namelist():
        return []
    root = ET.fromstring(z.read("xl/sharedStrings.xml"))
    out: list[str] = []
    for si in root.findall("m:si", NS):
        texts = [t.text or "" for t in si.iter(f"{{{NS['m']}}}t")]
        out.append("".join(texts))
    return out


def cell_value(c: ET.Element, sst: list[str]) -> str:
    t = c.attrib.get("t")
    v = c.find("m:v", NS)
    if t == "s" and v is not None:
        return sst[int(v.text or 0)]
    if t == "inlineStr":
        return "".join(x.text or "" for x in c.iter(f"{{{NS['m']}}}t"))
    return v.text if v is not None and v.text is not None else ""


def iter_sheets(z: ZipFile):
    wb = ET.fromstring(z.read("xl/workbook.xml"))
    rels = ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
    relmap = {rel.attrib["Id"]: rel.attrib["Target"] for rel in rels.findall(f"{{{REL_NS}}}Relationship")}
    for sh in wb.find("m:sheets", NS):
        name = sh.attrib["name"]
        rid = sh.attrib[f"{{{NS['r']}}}id"]
        target = relmap[rid]
        path = "xl/" + target if not target.startswith("/") else target[1:]
        yield name, path


def sheet_rows(root: ET.Element, sst: list[str]) -> list[list[str]]:
    rows: list[list[str]] = []
    for r in root.findall(".//m:sheetData/m:row", NS):
        vals: list[str] = []
        for c in r.findall("m:c", NS):
            idx = col_to_idx(c.attrib.get("r", "A"))
            while len(vals) <= idx:
                vals.append("")
            vals[idx] = cell_value(c, sst)
        rows.append(vals)
    return rows


def main() -> int:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    records: list[dict[str, str]] = []
    with ZipFile(XLSX) as z:
        sst = load_shared_strings(z)
        for sheet, path in iter_sheets(z):
            if sheet == "DataTypes":
                continue
            root = ET.fromstring(z.read(path))
            for row_num, vals in enumerate(sheet_rows(root, sst), start=1):
                modbus = norm(vals[0] if vals else "")
                # Accept single numeric addresses and explicit ranges; ignore header/note rows.
                if not re.fullmatch(r"\d+(?:\s*-\s*\d+)?", modbus):
                    continue
                rec = {
                    "sheet": sheet,
                    "row": str(row_num),
                    "register_raw": modbus,
                    "register_start": "",
                    "register_end": "",
                    "is_range": "false",
                    "friendly_name": norm(vals[1] if len(vals) > 1 else ""),
                    "description": norm(vals[2] if len(vals) > 2 else ""),
                    "bytes": norm(vals[3] if len(vals) > 3 else ""),
                    "data_type": norm(vals[4] if len(vals) > 4 else ""),
                    "format": norm(vals[5] if len(vals) > 5 else ""),
                    "access": norm(vals[6] if len(vals) > 6 else ""),
                    "present_from_version": norm(vals[7] if len(vals) > 7 else ""),
                    "extra_col_i": norm(vals[8] if len(vals) > 8 else ""),
                    "extra_col_j": norm(vals[9] if len(vals) > 9 else ""),
                    "extra_col_k": norm(vals[10] if len(vals) > 10 else ""),
                    "parser_note": "",
                }
                if "-" in modbus:
                    a, b = [int(x) for x in re.split(r"\s*-\s*", modbus)]
                    rec.update({"register_start": str(a), "register_end": str(b), "is_range": "true"})
                    if "reserved" in (rec["friendly_name"] + " " + rec["description"]).lower():
                        rec["parser_note"] = "reserved range in source; not expanded for gap count"
                    else:
                        rec["parser_note"] = "range row in source; not expanded automatically"
                else:
                    rec.update({"register_start": modbus, "register_end": modbus})
                records.append(rec)
    fields = [
        "sheet", "row", "register_raw", "register_start", "register_end", "is_range",
        "friendly_name", "description", "bytes", "data_type", "format", "access",
        "present_from_version", "extra_col_i", "extra_col_j", "extra_col_k", "parser_note",
    ]
    with OUT.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(records)
    print(f"wrote {OUT} ({len(records)} rows)")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
