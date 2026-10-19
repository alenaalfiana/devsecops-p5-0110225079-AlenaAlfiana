"""Fungsi validasi input pengguna."""

import re

ISBN_PATTERN = re.compile(r"^\d{10}(\d{3})?$")
MEMBER_PATTERN = re.compile(r"^[A-Za-z][A-Za-z .'-]{1,49}$")


class ValidationError(ValueError):
    """Dilempar ketika input tidak valid."""


def validate_isbn(isbn: str) -> str:
    """Pastikan ISBN berisi 10 atau 13 digit (tanda hubung diabaikan)."""
    cleaned = isbn.replace("-", "").strip()
    if not ISBN_PATTERN.match(cleaned):
        raise ValidationError("ISBN harus 10 atau 13 digit angka")
    return cleaned


def validate_title(title: str) -> str:
    title = title.strip()
    if not 1 <= len(title) <= 200:
        raise ValidationError("Judul harus 1-200 karakter")
    return title


def validate_year(year: int) -> int:
    if not 1000 <= int(year) <= 2100:
        raise ValidationError("Tahun terbit tidak masuk akal")
    return int(year)


def validate_member(name: str) -> str:
    name = name.strip()
    if not MEMBER_PATTERN.match(name):
        raise ValidationError("Nama anggota tidak valid")
    return name
