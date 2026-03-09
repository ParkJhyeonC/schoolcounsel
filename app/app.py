from __future__ import annotations

import cgi
import csv
import io
import json
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from .pdf_utils import build_student_card_pdf
from .services import MonthlyScheduleStore, RecordRepository, monthly_approval_ledger, parse_nice_csv, student_card

repo = RecordRepository(Path("data/records.json"))
schedules = MonthlyScheduleStore(Path("data/schedules"))


def html_page(body: str) -> bytes:
    return f"<!doctype html><html><head><meta charset='utf-8'><title>학교상담기록 관리</title></head><body>{body}</body></html>".encode("utf-8")


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        qs = parse_qs(parsed.query)

        if path == "/":
            months = "".join([f"<li><a href='/schedule/restore/{m}'>{m} 복원(JSON)</a></li>" for m in schedules.list_saved()]) or "<li>없음</li>"
            body = f"""
            <h1>학교상담기록 관리 프로그램</h1>
            <h2>1) 나이스 업로드</h2>
            <form action='/nice/upload' method='post' enctype='multipart/form-data'>
              <input type='file' name='file' accept='.csv' required><button>업로드</button>
            </form>
            <h2>2) 월별 결재대장</h2>
            <form action='/ledger' method='get'><input name='month' placeholder='YYYY-MM' required><button>조회</button></form>
            <h2>3) 상담카드 PDF</h2>
            <form onsubmit="event.preventDefault();location='/student-card/'+this.student_id.value+'.pdf';"><input name='student_id' required><button>PDF</button></form>
            <h2>4) 월간일정 저장/복원</h2>
            <form action='/schedule/save' method='post'>
              <input name='year_month' placeholder='YYYY-MM' required>
              <textarea name='schedules' style='width:100%;height:120px'>[]</textarea>
              <button>저장</button>
            </form>
            <ul>{months}</ul>
            """
            self._send(200, html_page(body), "text/html; charset=utf-8")
            return

        if path == "/ledger":
            ym = qs.get("month", [""])[0]
            rows = monthly_approval_ledger(repo.load(), ym) if ym else []
            trs = "".join([f"<tr><td>{r['date']}</td><td>{r['counselor']}</td><td>{r['count']}</td><td>{r['total_minutes']}</td><td>{r['students']}</td></tr>" for r in rows]) or "<tr><td colspan='5'>데이터 없음</td></tr>"
            body = f"<h1>월별 결재대장</h1><form><input name='month' value='{ym}'><button>조회</button></form><p><a href='/ledger.csv?month={ym}'>CSV 다운로드</a></p><table border='1'><tr><th>일자</th><th>상담자</th><th>건수</th><th>총분</th><th>학생</th></tr>{trs}</table><p><a href='/'>홈</a></p>"
            self._send(200, html_page(body), "text/html; charset=utf-8")
            return

        if path == "/ledger.csv":
            ym = qs.get("month", [""])[0]
            rows = monthly_approval_ledger(repo.load(), ym)
            out = io.StringIO()
            writer = csv.DictWriter(out, fieldnames=["date", "counselor", "count", "total_minutes", "students"])
            writer.writeheader(); writer.writerows(rows)
            self._send(200, out.getvalue().encode("utf-8"), "text/csv; charset=utf-8", f"attachment; filename=approval_ledger_{ym}.csv")
            return

        if path.startswith("/student-card/") and path.endswith(".pdf"):
            student_id = path.split("/")[-1].removesuffix(".pdf")
            card = student_card(repo.load(), student_id)
            pdf = build_student_card_pdf(card)
            self._send(200, pdf, "application/pdf", f"attachment; filename=counsel_card_{student_id}.pdf")
            return

        if path.startswith("/schedule/restore/"):
            ym = path.split("/")[-1]
            payload = schedules.restore(ym)
            self._send(200, json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8"), "application/json; charset=utf-8")
            return

        self._send(404, b"Not Found", "text/plain")

    def do_POST(self):
        if self.path == "/nice/upload":
            form = cgi.FieldStorage(fp=self.rfile, headers=self.headers, environ={"REQUEST_METHOD": "POST"})
            file_item = form["file"] if "file" in form else None
            if not file_item or not getattr(file_item, "file", None):
                self._send(400, b"file missing", "text/plain")
                return
            records = parse_nice_csv(file_item.file.read())
            repo.append_many(records)
            self._redirect("/")
            return

        if self.path == "/schedule/save":
            length = int(self.headers.get("Content-Length", "0"))
            raw = self.rfile.read(length).decode("utf-8")
            body = parse_qs(raw)
            year_month = body.get("year_month", [""])[0]
            schedules_json = body.get("schedules", ["[]"])[0]
            schedules.save(year_month, json.loads(schedules_json))
            self._redirect("/")
            return

        self._send(404, b"Not Found", "text/plain")

    def _redirect(self, location: str):
        self.send_response(HTTPStatus.SEE_OTHER)
        self.send_header("Location", location)
        self.end_headers()

    def _send(self, status: int, body: bytes, ctype: str, disposition: str | None = None):
        self.send_response(status)
        self.send_header("Content-Type", ctype)
        if disposition:
            self.send_header("Content-Disposition", disposition)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def run():
    server = ThreadingHTTPServer(("0.0.0.0", 8000), Handler)
    print("Serving on http://0.0.0.0:8000")
    server.serve_forever()


if __name__ == "__main__":
    run()
