from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass
class SignatureSlot:
    slot: int
    role: str
    label: str
    user_id: str
    required: bool = True
    signed: bool = False

    def to_dict(self) -> dict:
        return {
            "slot": self.slot,
            "role": self.role,
            "label": self.label,
            "userId": self.user_id,
            "required": self.required,
            "signed": self.signed,
        }


@dataclass
class SignatureDocument:
    document_type: str
    signatures: List[SignatureSlot]

    def validate(self) -> None:
        if not self.signatures:
            raise ValueError("signatures list cannot be empty")

        ordered = sorted(self.signatures, key=lambda s: s.slot)
        if [s.slot for s in ordered] != [s.slot for s in self.signatures]:
            raise ValueError("signatures must be in ascending slot order")

        for sig in self.signatures:
            if sig.required and not sig.user_id:
                raise ValueError(f"required signature in slot {sig.slot} must have user_id")

        if self.document_type == "quotation":
            if len(self.signatures) != 3:
                raise ValueError("quotation must contain exactly 3 signature slots")
            if self.signatures[0].role != "sales_person":
                raise ValueError("quotation slot #1 must be sales_person")
            if self.signatures[1].role not in {"approver_a", "approver_b"}:
                raise ValueError("quotation slot #2 must be an approver")
            if self.signatures[2].role not in {"approver_a", "approver_b"}:
                raise ValueError("quotation slot #3 must be an approver")
            if self.signatures[1].role == self.signatures[2].role:
                raise ValueError("quotation approver roles must be distinct")

        if self.document_type == "sales_order":
            if len(self.signatures) != 2:
                raise ValueError("sales_order must contain exactly 2 signature slots")
            if self.signatures[0].role != "company":
                raise ValueError("sales_order slot #1 must be company")
            if self.signatures[1].role != "customer":
                raise ValueError("sales_order slot #2 must be customer")

    def is_fully_signed(self) -> bool:
        return all(not s.required or s.signed for s in self.signatures)

    def to_dict(self) -> dict:
        return {
            "documentType": self.document_type,
            "signatures": [s.to_dict() for s in self.signatures],
        }


def build_quotation_document(
    sales_person_user_id: str,
    approver_a_user_id: str,
    approver_b_user_id: str,
) -> SignatureDocument:
    doc = SignatureDocument(
        document_type="quotation",
        signatures=[
            SignatureSlot(1, "sales_person", "Sales Person", sales_person_user_id),
            SignatureSlot(2, "approver_a", "Approver 1", approver_a_user_id),
            SignatureSlot(3, "approver_b", "Approver 2", approver_b_user_id),
        ],
    )
    doc.validate()
    return doc


def build_sales_order_document(
    company_user_id: str,
    customer_user_id: str,
) -> SignatureDocument:
    doc = SignatureDocument(
        document_type="sales_order",
        signatures=[
            SignatureSlot(1, "company", "Company", company_user_id),
            SignatureSlot(2, "customer", "Customer", customer_user_id),
        ],
    )
    doc.validate()
    return doc
