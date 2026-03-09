# 학교상담기록 관리 프로그램 (재구현)

추가 설치 없이 실행 가능하며, **Windows 배치 파일**로 일반 웹앱처럼 쉽게 사용할 수 있습니다.

## Windows에서 바로 실행
- `start_webapp.bat` 더블클릭: 서버 실행
- `start_webapp_and_open.bat` 더블클릭: 서버 실행 + 브라우저 열기

접속 주소: `http://127.0.0.1:8000`

## 터미널 실행
```bash
python run.py
```

## 샘플 데이터 미리 넣기 (선택)
```bash
python -m app.bootstrap
```
- `sheet_previews/nice_upload_sample.csv` 데이터를 `data/records.json`에 적재합니다.

## 우선 구현 기능
1. **나이스 업로드**: CSV 업로드 후 상담기록 저장
2. **월별 결재대장**: 월 단위 집계 조회 + CSV 다운로드
3. **상담카드 PDF**: 학생별 상담 이력 PDF 다운로드
4. **월간일정 저장/복원**: 월 단위 일정 JSON 저장/복원

## 헬스체크
```bash
curl http://127.0.0.1:8000/health
```
