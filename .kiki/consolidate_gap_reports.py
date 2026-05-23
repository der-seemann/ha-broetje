#!/usr/bin/env python3
from __future__ import annotations

import csv
import re
from dataclasses import dataclass, field
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
REPORTS_DIR = ROOT / ".kiki" / "reports"
OUT_MD = REPORTS_DIR / "PHASE1_LUECKENLISTE_KONSOLIDIERT_2026-05-23.md"
OUT_CSV = REPORTS_DIR / "PHASE1_LUECKENLISTE_KONSOLIDIERT_2026-05-23.csv"
XLSX_SOURCE = "GTW-08-Modbus-parameterlijst_gap_report.md"


@dataclass
class GapEntry:
    block: str
    datatype: str
    access: str
    context: str
    description: str
    sources: set[str] = field(default_factory=set)

    def merge(self, other: "GapEntry") -> None:
        if not self.datatype and other.datatype:
            self.datatype = other.datatype
        if not self.access and other.access:
            self.access = other.access
        if not self.context and other.context:
            self.context = other.context
        if not self.description and other.description:
            self.description = other.description
        self.sources |= other.sources


STOPWORDS = {
    "the",
    "and",
    "der",
    "die",
    "das",
    "des",
    "de",
    "du",
    "of",
    "for",
    "to",
    "by",
    "bit",
    "read",
    "write",
    "register",
    "mode",
    "current",
    "actual",
    "temperature",
}


def clean(text: str) -> str:
    text = re.sub(r"\s+", " ", text.strip())
    return text.replace("\\|", "|")


def normalize_access(text: str) -> str:
    upper = clean(text).upper()
    if "W" in upper:
        return "R/W"
    if "R" in upper or "READ" in upper:
        return "R"
    return upper


def parse_span(block: str) -> tuple[int, int] | None:
    try:
        if "-" in block:
            start, end = block.split("-", 1)
            return int(start), int(end)
        value = int(block)
        return value, value
    except ValueError:
        return None


def description_tokens(text: str) -> set[str]:
    tokens = set(re.findall(r"[a-z0-9]+", clean(text).lower()))
    return {token for token in tokens if token not in STOPWORDS and len(token) > 1}


def choose_preferred(existing: GapEntry, new: GapEntry) -> GapEntry:
    existing_span = parse_span(existing.block)
    new_span = parse_span(new.block)
    if existing_span and new_span:
        existing_len = existing_span[1] - existing_span[0]
        new_len = new_span[1] - new_span[0]
        if new_len > existing_len:
            new.merge(existing)
            return new
    existing.merge(new)
    return existing


def upsert_entry(entries: dict[str, GapEntry], new: GapEntry) -> None:
    exact = entries.get(new.block)
    if exact is not None:
        exact.merge(new)
        return

    new_span = parse_span(new.block)
    new_tokens = description_tokens(new.description)
    if new_span and new_tokens:
        for key, existing in list(entries.items()):
            existing_span = parse_span(existing.block)
            if not existing_span:
                continue
            xlsx_primary = XLSX_SOURCE in existing.sources
            if xlsx_primary and existing_span[0] <= new_span[0] <= new_span[1] <= existing_span[1]:
                existing.merge(new)
                return
            contained = (
                existing_span[0] <= new_span[0] <= new_span[1] <= existing_span[1]
                or new_span[0] <= existing_span[0] <= existing_span[1] <= new_span[1]
            )
            if not contained:
                continue
            overlap = new_tokens & description_tokens(existing.description)
            if not overlap:
                continue
            preferred = choose_preferred(existing, new)
            if preferred is not existing:
                del entries[key]
                entries[preferred.block] = preferred
            return

    entries[new.block] = new


def parse_markdown_table(lines: list[str]) -> list[list[str]]:
    rows: list[list[str]] = []
    for line in lines:
        if not line.startswith("|"):
            continue
        if set(line.replace("|", "").replace("-", "").replace(":", "").strip()) == set():
            continue
        parts = [clean(part) for part in line.strip().strip("|").split("|")]
        rows.append(parts)
    return rows


def load_spec_report(entries: dict[str, GapEntry]) -> None:
    path = REPORTS_DIR / "GTW-08_ModBus-Spec_gap_report.md"
    lines = path.read_text(encoding="utf-8").splitlines()
    start = lines.index("## Fehlende Register") + 1
    end = lines.index("## Bereits abgedeckte Register")
    rows = parse_markdown_table(lines[start:end])
    for row in rows[1:]:
        if len(row) < 6:
            continue
        block = row[0]
        entry = GapEntry(
            block=block,
            datatype=row[1],
            access=normalize_access(row[2]),
            context=clean(row[4]),
            description=clean(row[5]),
            sources={path.name},
        )
        upsert_entry(entries, entry)


def load_param_pdf_report(entries: dict[str, GapEntry]) -> None:
    path = REPORTS_DIR / "Modbus_GTW-08_Liste_der_Parameter_gap_report.md"
    lines = path.read_text(encoding="utf-8").splitlines()
    start = lines.index("## Fehlende Register-Kandidaten") + 1
    section_lines: list[str] = []
    for line in lines[start:]:
        if line.startswith("## "):
            break
        section_lines.append(line)
    rows = parse_markdown_table(section_lines)
    for row in rows[1:]:
        if len(row) < 6:
            continue
        block = row[0]
        entry = GapEntry(
            block=block,
            datatype=row[1],
            access=normalize_access(row[2]),
            context=clean(row[4]),
            description=clean(row[5]),
            sources={path.name},
        )
        upsert_entry(entries, entry)


def load_xlsx_report(entries: dict[str, GapEntry]) -> None:
    path = REPORTS_DIR / "GTW-08-Modbus-parameterlijst_gap_report.md"
    lines = path.read_text(encoding="utf-8").splitlines()
    current_sheet = ""
    in_table = False
    headers: list[str] = []
    for line in lines:
        if line.startswith("### "):
            current_sheet = clean(line[4:])
            in_table = False
            headers = []
            continue
        if not line.startswith("|"):
            continue
        if not in_table:
            headers = [clean(p) for p in line.strip().strip("|").split("|")]
            in_table = True
            continue
        if set(line.replace("|", "").replace("-", "").replace(":", "").strip()) == set():
            continue
        values = [clean(p) for p in line.strip().strip("|").split("|")]
        if len(values) != len(headers):
            continue
        row = dict(zip(headers, values))
        block = row.get("Register/Block", "")
        if not block:
            continue
        entry = GapEntry(
            block=block,
            datatype=row.get("Data Type", ""),
            access=normalize_access(row.get("Access", "")),
            context=current_sheet,
            description=clean(row.get("Description", "")),
            sources={path.name},
        )
        upsert_entry(entries, entry)


def block_sort_key(block: str) -> tuple[int, int, str]:
    first = block.split("-")[0]
    try:
        return (0, int(first), block)
    except ValueError:
        return (1, 0, block)


def classify(entry: GapEntry) -> str:
    return "enthält W laut Doku" if "W" in entry.access else "nur R laut Doku"


def write_outputs(entries: dict[str, GapEntry]) -> None:
    ordered = sorted(entries.values(), key=lambda item: block_sort_key(item.block))
    total = len(ordered)
    rw_count = sum(1 for item in ordered if "W" in item.access)
    r_count = total - rw_count

    with OUT_CSV.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(
            ["block", "datatype", "access", "classification", "context", "description", "sources"]
        )
        for item in ordered:
            writer.writerow(
                [
                    item.block,
                    item.datatype,
                    item.access,
                    classify(item),
                    item.context,
                    item.description,
                    ", ".join(sorted(item.sources)),
                ]
            )

    lines = [
        "# Phase-1 Lückenliste konsolidiert",
        "",
        "Stand: 2026-05-23",
        "",
        "## Kurzfazit",
        f"- Eindeutige fehlende Register/Blöcke über alle drei Quellen: {total}",
        f"- Nur R laut Doku: {r_count}",
        f"- Enthält W laut Doku: {rw_count}",
        "- Diese Liste dedupliziert die drei Einzelreports, ohne Schreibfunktion zu implementieren.",
        "",
        "## Artefakte",
        f"- CSV: `{OUT_CSV.relative_to(ROOT)}`",
        f"- Quelle 1: `.kiki/reports/GTW-08_ModBus-Spec_gap_report.md`",
        f"- Quelle 2: `.kiki/reports/Modbus_GTW-08_Liste_der_Parameter_gap_report.md`",
        f"- Quelle 3: `.kiki/reports/GTW-08-Modbus-parameterlijst_gap_report.md`",
        "",
        "## Konsolidierte Lückenliste",
        "| Block | Typ | Zugriff | Klasse | Kontext | Quellen | Beschreibung |",
        "|---|---|---|---|---|---|---|",
    ]
    for item in ordered:
        lines.append(
            "| {block} | {datatype} | {access} | {klass} | {context} | {sources} | {description} |".format(
                block=item.block,
                datatype=item.datatype or "-",
                access=item.access or "-",
                klass=classify(item),
                context=item.context or "-",
                sources=", ".join(sorted(item.sources)),
                description=item.description or "-",
            )
        )

    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    entries: dict[str, GapEntry] = {}
    load_xlsx_report(entries)
    load_spec_report(entries)
    load_param_pdf_report(entries)
    write_outputs(entries)


if __name__ == "__main__":
    main()
