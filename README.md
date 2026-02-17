# Signature Module

Implemented a basic signature workflow module matching the requested rules:

- **Quotation**: 3 signatures
  1. Sales person
  2. Approver 1 (configurable)
  3. Approver 2 (configurable)
- **Sales Order**: 2 signatures
  1. Company
  2. Customer

## Run tests

```bash
python -m unittest discover -s tests -v
```

## Quick usage

```python
from signatures.module import build_quotation_document, build_sales_order_document

quotation = build_quotation_document("sales-id", "approver1-id", "approver2-id")
sales_order = build_sales_order_document("company-id", "customer-id")

print(quotation.to_dict())
print(sales_order.to_dict())
```
