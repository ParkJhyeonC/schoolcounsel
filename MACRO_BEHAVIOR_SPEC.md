# MACRO BEHAVIOR SPEC

## 나이스 업로드
- `POST /nice/upload`
- CSV 필수 컬럼 유효성 검사
- 성공 시 레코드 누적 저장

## 월별 결재대장
- `GET /ledger?month=YYYY-MM`
- 해당 월 데이터만 필터링
- 일자+상담자 단위 건수/총시간/학생 목록 집계
- `GET /ledger.csv?month=YYYY-MM` 다운로드 지원

## 상담카드 PDF
- `GET /student-card/<student_id>.pdf`
- 학생 기본정보 및 상담이력 출력

## 월간일정 저장/복원
- `POST /schedule/save` (year_month + schedules JSON)
- `GET /schedule/restore/<year_month>`
