import unittest

from signatures.module import (
    SignatureDocument,
    SignatureSlot,
    build_quotation_document,
    build_sales_order_document,
)


class SignatureModuleTests(unittest.TestCase):
    def test_build_quotation_document_has_three_signatures(self):
        doc = build_quotation_document("u-sales", "u-app-1", "u-app-2")
        self.assertEqual(doc.document_type, "quotation")
        self.assertEqual(len(doc.signatures), 3)
        self.assertEqual(doc.signatures[0].role, "sales_person")
        self.assertEqual(doc.signatures[1].role, "approver_a")
        self.assertEqual(doc.signatures[2].role, "approver_b")

    def test_build_sales_order_document_has_two_signatures(self):
        doc = build_sales_order_document("u-company", "u-customer")
        self.assertEqual(doc.document_type, "sales_order")
        self.assertEqual(len(doc.signatures), 2)
        self.assertEqual(doc.signatures[0].role, "company")
        self.assertEqual(doc.signatures[1].role, "customer")

    def test_is_fully_signed_checks_required_slots(self):
        doc = build_sales_order_document("u-company", "u-customer")
        self.assertFalse(doc.is_fully_signed())
        doc.signatures[0].signed = True
        doc.signatures[1].signed = True
        self.assertTrue(doc.is_fully_signed())

    def test_validate_quotation_requires_sales_person_in_slot_one(self):
        doc = SignatureDocument(
            document_type="quotation",
            signatures=[
                SignatureSlot(1, "approver_a", "Approver 1", "u1"),
                SignatureSlot(2, "sales_person", "Sales", "u2"),
                SignatureSlot(3, "approver_b", "Approver 2", "u3"),
            ],
        )
        with self.assertRaises(ValueError):
            doc.validate()


if __name__ == "__main__":
    unittest.main()
