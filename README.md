# 학교상담기록 관리 프로그램 (재구현)

파이썬 표준 라이브러리 기반이라 **추가 설치 없이 바로 실행**할 수 있습니다.

## 빠른 실행 (권장)
```bash
python run.py
```

브라우저에서 `http://localhost:8000` 접속.

## 샘플 데이터 미리 넣기 (선택)
```bash
python -m app.bootstrap
```
- `sheet_previews/nice_upload_sample.csv` 데이터를 `data/records.json`에 적재합니다.

## 포트 변경
```bash
python run.py --port 9000
```

## 우선 구현 기능
1. **나이스 업로드**: CSV 업로드 후 상담기록 저장
2. **월별 결재대장**: 월 단위 집계 조회 + CSV 다운로드
3. **상담카드 PDF**: 학생별 상담 이력 PDF 다운로드
4. **월간일정 저장/복원**: 월 단위 일정 JSON 저장/복원
