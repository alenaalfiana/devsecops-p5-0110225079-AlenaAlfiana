"""Antarmuka baris perintah (CLI) Perpustakaan Mini."""

import argparse
import sys

from .services import LibraryError, LibraryService
from .storage import JsonStorage
from .validators import ValidationError


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="perpustakaan", description="Perpustakaan Mini")
    parser.add_argument("--data", default="data.json", help="Lokasi berkas data JSON")
    sub = parser.add_subparsers(dest="command", required=True)

    add = sub.add_parser("add", help="Tambah buku baru")
    add.add_argument("isbn")
    add.add_argument("title")
    add.add_argument("author")
    add.add_argument("year", type=int)

    search = sub.add_parser("search", help="Cari buku berdasarkan judul/penulis")
    search.add_argument("keyword")

    borrow = sub.add_parser("borrow", help="Pinjam buku")
    borrow.add_argument("isbn")
    borrow.add_argument("member")

    ret = sub.add_parser("return", help="Kembalikan buku")
    ret.add_argument("isbn")

    sub.add_parser("loans", help="Tampilkan peminjaman aktif")
    return parser


def run(argv=None) -> int:
    args = build_parser().parse_args(argv)
    service = LibraryService(JsonStorage(args.data))
    try:
        if args.command == "add":
            book = service.add_book(args.isbn, args.title, args.author, args.year)
            print(f"Buku ditambahkan: {book.title} ({book.isbn})")
        elif args.command == "search":
            for b in service.search(args.keyword):
                status = "tersedia" if b.available else "dipinjam"
                print(f"{b.isbn} | {b.title} - {b.author} ({b.year}) [{status}]")
        elif args.command == "borrow":
            loan = service.borrow(args.isbn, args.member)
            print(f"{loan.member} meminjam buku {loan.isbn} pada {loan.loan_date}")
        elif args.command == "return":
            loan = service.return_book(args.isbn)
            print(f"Buku {loan.isbn} dikembalikan pada {loan.return_date}")
        elif args.command == "loans":
            for loan in service.active_loans():
                print(f"{loan.isbn} dipinjam {loan.member} sejak {loan.loan_date}")
    except (LibraryError, ValidationError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    return 0
