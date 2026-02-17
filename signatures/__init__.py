"""Signature workflow module for quotations and sales orders."""

from .module import (
    SignatureSlot,
    SignatureDocument,
    build_quotation_document,
    build_sales_order_document,
)

__all__ = [
    "SignatureSlot",
    "SignatureDocument",
    "build_quotation_document",
    "build_sales_order_document",
]
