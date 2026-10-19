"""Logika bisnis perpustakaan."""

from datetime import date
from typing import List, Optional

from .models import Book, Loan
from .storage import JsonStorage
from .validators import (
    validate_isbn,
    validate_member,
    validate_title,
    validate_year,
)


class LibraryError(Exception):
    """Kesalahan logika bisnis (mis. buku tidak ditemukan)."""


class LibraryService:
    def __init__(self, storage: JsonStorage):
        self.storage = storage
        self.books, self.loans = storage.load()

    def _persist(self) -> None:
        self.storage.save(self.books, self.loans)

    def find_book(self, isbn: str) -> Optional[Book]:
        isbn = validate_isbn(isbn)
        return next((b for b in self.books if b.isbn == isbn), None)

    def add_book(self, isbn: str, title: str, author: str, year: int) -> Book:
        isbn = validate_isbn(isbn)
        if self.find_book(isbn):
            raise LibraryError("Buku dengan ISBN tersebut sudah ada")
        book = Book(isbn, validate_title(title), validate_title(author), validate_year(year))
        self.books.append(book)
        self._persist()
        return book

    def search(self, keyword: str) -> List[Book]:
        keyword = keyword.lower().strip()
        return [
            b for b in self.books
            if keyword in b.title.lower() or keyword in b.author.lower()
        ]

    def borrow(self, isbn: str, member: str) -> Loan:
        book = self.find_book(isbn)
        if book is None:
            raise LibraryError("Buku tidak ditemukan")
        if not book.available:
            raise LibraryError("Buku sedang dipinjam")
        loan = Loan.create(book.isbn, validate_member(member))
        book.available = False
        self.loans.append(loan)
        self._persist()
        return loan

    def return_book(self, isbn: str) -> Loan:
        book = self.find_book(isbn)
        if book is None:
            raise LibraryError("Buku tidak ditemukan")
        for loan in self.loans:
            if loan.isbn == book.isbn and loan.return_date is None:
                loan.return_date = date.today().isoformat()
                book.available = True
                self._persist()
                return loan
        raise LibraryError("Tidak ada peminjaman aktif untuk buku ini")

    def active_loans(self) -> List[Loan]:
        return [l for l in self.loans if l.return_date is None]
