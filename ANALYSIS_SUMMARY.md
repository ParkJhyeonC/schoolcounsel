# ANALYSIS SUMMARY

- 원본 문서/코드가 없는 상태에서 요구된 핵심 기능을 먼저 작동 가능한 MVP 형태로 재구현.
- 입력 포맷은 나이스 업로드용 CSV 표준 컬럼으로 통일.
- 데이터 저장은 `data/records.json`, `data/schedules/*.json` 로컬 파일 저장 방식 사용.
- 월별 결재대장은 (일자, 상담자) 기준 집계로 결재단위 확인에 초점.
