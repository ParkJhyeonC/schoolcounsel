from __future__ import annotations

import csv
import io
import json
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Iterable


@dataclass
class CounselingRecord:
    date: str
    student_id: str
    student_name: str
    grade: str
    class_name: str
    counselor: str
    topic: str
    method: str
    duration_minutes: int
    notes: str = ""


class RecordRepository:
    def __init__(self, path: Path):
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self.path.write_text("[]", encoding="utf-8")

    def load(self) -> list[CounselingRecord]:
        data = json.loads(self.path.read_text(encoding="utf-8"))
        return [CounselingRecord(**item) for item in data]

    def save(self, records: Iterable[CounselingRecord]) -> None:
        data = [asdict(r) for r in records]
        self.path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    def append_many(self, records: Iterable[CounselingRecord]) -> int:
        current = self.load()
        incoming = list(records)
        self.save([*current, *incoming])
        return len(incoming)


def parse_nice_csv(content: bytes) -> list[CounselingRecord]:
    text = content.decode("utf-8-sig")
    reader = csv.DictReader(io.StringIO(text))
    required = {
        "date",
        "student_id",
        "student_name",
        "grade",
        "class_name",
        "counselor",
        "topic",
        "method",
        "duration_minutes",
    }
    if not reader.fieldnames or not required.issubset(set(reader.fieldnames)):
        missing = sorted(required - set(reader.fieldnames or []))
        raise ValueError(f"나이스 CSV 필수 컬럼 누락: {', '.join(missing)}")

    records: list[CounselingRecord] = []
    for row in reader:
        records.append(
            CounselingRecord(
                date=row["date"],
                student_id=row["student_id"],
                student_name=row["student_name"],
                grade=row["grade"],
                class_name=row["class_name"],
                counselor=row["counselor"],
                topic=row["topic"],
                method=row["method"],
                duration_minutes=int(row["duration_minutes"]),
                notes=row.get("notes", ""),
            )
        )
    return records


def month_filter(records: Iterable[CounselingRecord], year_month: str) -> list[CounselingRecord]:
    return [r for r in records if r.date.startswith(year_month)]


def monthly_approval_ledger(records: Iterable[CounselingRecord], year_month: str) -> list[dict]:
    monthly = month_filter(records, year_month)
    grouped: dict[tuple[str, str], dict] = {}
    for rec in monthly:
        key = (rec.date, rec.counselor)
        if key not in grouped:
            grouped[key] = {
                "date": rec.date,
                "counselor": rec.counselor,
                "count": 0,
                "total_minutes": 0,
                "students": set(),
            }
        grouped[key]["count"] += 1
        grouped[key]["total_minutes"] += rec.duration_minutes
        grouped[key]["students"].add(f"{rec.student_name}({rec.student_id})")

    rows = []
    for row in grouped.values():
        rows.append(
            {
                "date": row["date"],
                "counselor": row["counselor"],
                "count": row["count"],
                "total_minutes": row["total_minutes"],
                "students": ", ".join(sorted(row["students"])),
            }
        )
    rows.sort(key=lambda x: (x["date"], x["counselor"]))
    return rows


def student_card(records: Iterable[CounselingRecord], student_id: str) -> dict:
    filtered = [r for r in records if r.student_id == student_id]
    if not filtered:
        raise ValueError("해당 학생 상담 기록이 없습니다.")
    filtered.sort(key=lambda r: r.date)
    student = filtered[0]
    return {
        "student_id": student.student_id,
        "student_name": student.student_name,
        "grade": student.grade,
        "class_name": student.class_name,
        "history": [asdict(r) for r in filtered],
    }


class MonthlyScheduleStore:
    def __init__(self, directory: Path):
        self.directory = directory
        self.directory.mkdir(parents=True, exist_ok=True)

    def save(self, year_month: str, schedules: list[dict]) -> Path:
        payload = {
            "year_month": year_month,
            "saved_at": datetime.now().isoformat(timespec="seconds"),
            "schedules": schedules,
        }
        path = self.directory / f"{year_month}.json"
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        return path

    def restore(self, year_month: str) -> dict:
        path = self.directory / f"{year_month}.json"
        if not path.exists():
            raise FileNotFoundError("저장된 월간 일정이 없습니다.")
        return json.loads(path.read_text(encoding="utf-8"))

    def list_saved(self) -> list[str]:
        return sorted(p.stem for p in self.directory.glob("*.json"))
