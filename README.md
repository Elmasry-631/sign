# Odoo 19 - Sale Signature Flow Module

هذا المستودع يحتوي الآن على موديول Odoo 19 باسم `odoo_signature_flow` يطبق المطلوب:

- **عرض السعر (Quotation)**: 3 توقيعات
  1. مسؤول المبيعات
  2. المعتمد الأول (من الإعدادات)
  3. المعتمد الثاني (من الإعدادات)
- **أمر البيع (Sales Order)**: توقيعان
  1. الشركة (من الإعدادات)
  2. العميل (Partner الطلب)

## المسارات الأساسية

- `odoo_signature_flow/__manifest__.py`
- `odoo_signature_flow/models/sale_order.py`
- `odoo_signature_flow/models/res_company.py`
- `odoo_signature_flow/models/res_config_settings.py`
- `odoo_signature_flow/views/sale_order_views.xml`
- `odoo_signature_flow/views/res_config_settings_views.xml`

## ملاحظات تشغيل

1. أضف الموديول إلى `addons_path` في Odoo 19.
2. حدث قائمة التطبيقات ثم ثبّت `Sale Signature Flow`.
3. من إعدادات المبيعات عيّن:
   - Quotation Approver 1
   - Quotation Approver 2
   - Sales Order Company Signer
