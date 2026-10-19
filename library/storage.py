"""Penyimpanan data buku dan peminjaman ke berkas JSON."""

import json
import os
from typing import List, Tuple

from .models import Book, Loan


class JsonStorage:
    """Menyimpan dan membaca data dari satu berkas JSON."""

    def __init__(self, path: str = "data.json"):
        self.path = path

    def load(self) -> Tuple[List[Book], List[Loan]]:
        if not os.path.exists(self.path):
            return [], []
        with open(self.path, "r", encoding="utf-8") as fh:
            raw = json.load(fh)
        books = [Book.from_dict(b) for b in raw.get("books", [])]
        loans = [Loan.from_dict(l) for l in raw.get("loans", [])]
        return books, loans

    def save(self, books: List[Book], loans: List[Loan]) -> None:
        payload = {
            "books": [b.to_dict() for b in books],
            "loans": [l.to_dict() for l in loans],
        }
        with open(self.path, "w", encoding="utf-8") as fh:
            json.dump(payload, fh, indent=2, ensure_ascii=False)
