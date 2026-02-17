# Signature Workflow Specification

## 1) Quotation (عرض السعر)

The quotation document must support **3 signatures**:

1. **Signature #1 (Sales Person)**
   - Source: the assigned sales person on the quotation.
   - Required by default.

2. **Signature #2 (Approver A)**
   - Source: configurable responsible user/role (selected by business/admin).
   - Required.

3. **Signature #3 (Approver B)**
   - Source: configurable responsible user/role (selected by business/admin).
   - Required.

### Quotation Data Contract (example)

```json
{
  "documentType": "quotation",
  "signatures": [
    {
      "slot": 1,
      "role": "sales_person",
      "label": "Sales Person",
      "userId": "<sales-user-id>",
      "required": true,
      "signed": false
    },
    {
      "slot": 2,
      "role": "approver_a",
      "label": "Approver 1",
      "userId": "<configurable-user-id>",
      "required": true,
      "signed": false
    },
    {
      "slot": 3,
      "role": "approver_b",
      "label": "Approver 2",
      "userId": "<configurable-user-id>",
      "required": true,
      "signed": false
    }
  ]
}
```

## 2) Sales Order (أمر البيع)

The sales order document must support **2 signatures**:

1. **Company Signature**
   - Source: authorized company signer.
   - Required.

2. **Customer Signature**
   - Source: customer contact signer.
   - Required.

### Sales Order Data Contract (example)

```json
{
  "documentType": "sales_order",
  "signatures": [
    {
      "slot": 1,
      "role": "company",
      "label": "Company",
      "userId": "<company-signer-id>",
      "required": true,
      "signed": false
    },
    {
      "slot": 2,
      "role": "customer",
      "label": "Customer",
      "userId": "<customer-signer-id>",
      "required": true,
      "signed": false
    }
  ]
}
```

## 3) Validation Rules

- A document is considered fully signed only when all required signature slots are signed.
- Signature slots must preserve order (`slot` ascending).
- For quotations, slot #1 must always map to the sales person.
- For quotations, slots #2 and #3 must be configurable and cannot be left unassigned.
- For sales orders, both company and customer signatures must be present before final approval.

## 4) Suggested UI Labels (Arabic)

- Quotation:
  - `توقيع مسؤول المبيعات`
  - `توقيع المعتمد الأول`
  - `توقيع المعتمد الثاني`
- Sales Order:
  - `توقيع الشركة`
  - `توقيع العميل`
