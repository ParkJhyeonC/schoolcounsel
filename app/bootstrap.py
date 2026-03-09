from __future__ import annotations

from pathlib import Path

from .services import RecordRepository, parse_nice_csv


def seed_sample() -> int:
    sample_path = Path("sheet_previews/nice_upload_sample.csv")
    content = sample_path.read_bytes()
    records = parse_nice_csv(content)
    repo = RecordRepository(Path("data/records.json"))
    return repo.append_many(records)


if __name__ == "__main__":
    inserted = seed_sample()
    print(f"샘플 데이터 적재 완료: {inserted}건")
