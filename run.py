from __future__ import annotations

import argparse

from app.app import run


def main() -> None:
    parser = argparse.ArgumentParser(description="학교상담기록 관리 프로그램 실행")
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    run(host=args.host, port=args.port)


if __name__ == "__main__":
    main()
