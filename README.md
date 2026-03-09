# 학교상담기록 관리 프로그램 (재구현)

파이썬 표준 라이브러리(HTTP 서버) 기반의 경량 프로그램으로 아래 핵심 기능을 우선 제공합니다.

## 우선 구현 기능
1. **나이스 업로드**: CSV 업로드 후 상담기록 저장
2. **월별 결재대장**: 월 단위 집계 조회 + CSV 다운로드
3. **상담카드 PDF**: 학생별 상담 이력 PDF 다운로드
4. **월간일정 저장/복원**: 월 단위 일정 JSON 저장/복원

## 실행 방법
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m app.app
```

브라우저에서 `http://localhost:8000` 접속.
