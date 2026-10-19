"""Model data untuk aplikasi Perpustakaan Mini."""

from dataclasses import dataclass, asdict
from datetime import date
from typing import Optional


@dataclass
class Book:
    """Representasi satu buku di perpustakaan."""

    isbn: str
    title: str
    author: str
    year: int
    available: bool = True

    def to_dict(self) -> dict:
        return asdict(self)

    @staticmethod
    def from_dict(data: dict) -> "Book":
        return Book(
            isbn=data["isbn"],
            title=data["title"],
            author=data["author"],
            year=int(data["year"]),
            available=bool(data.get("available", True)),
        )


@dataclass
class Loan:
    """Representasi peminjaman buku oleh seorang anggota."""

    isbn: str
    member: str
    loan_date: str
    return_date: Optional[str] = None

    @staticmethod
    def create(isbn: str, member: str) -> "Loan":
        return Loan(isbn=isbn, member=member, loan_date=date.today().isoformat())

    def to_dict(self) -> dict:
        return asdict(self)

    @staticmethod
    def from_dict(data: dict) -> "Loan":
        return Loan(
            isbn=data["isbn"],
            member=data["member"],
            loan_date=data["loan_date"],
            return_date=data.get("return_date"),
        )
