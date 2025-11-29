# دليل تشغيل الاختبارات - Test Running Guide

## 🚀 تشغيل سريع - Quick Start

### من مجلد المشروع:
```bash
cd "C:\Users\engha\Music\New folder1\local_ai_agent"
python run_tests.py
```

### أو استخدم السكريبت:
```bash
scripts\run_tests.bat
```

## 📋 المتطلبات - Requirements

تأكد من تثبيت:
```bash
pip install pytest pytest-cov pytest-mock
```

أو:
```bash
pip install -r requirements.txt
```

## ✅ الاختبارات المتوفرة - Available Tests

- `test_agents.py` - اختبارات الوكيلات
- `test_tools.py` - اختبارات الأدوات
- `test_memory.py` - اختبارات الذاكرة
- `test_knowledge_base.py` - اختبارات قاعدة المعرفة
- `test_core_components.py` - اختبارات المكونات الأساسية
- `test_utils.py` - اختبارات الأدوات المساعدة

## 🎯 أوامر مفيدة - Useful Commands

```bash
# تشغيل جميع الاختبارات
python run_tests.py

# تشغيل اختبارات الوحدة فقط
python run_tests.py --unit

# تشغيل الاختبارات السريعة
python run_tests.py --fast

# أو استخدم pytest مباشرة
pytest tests/
pytest tests/test_memory.py
pytest tests/test_memory.py::TestMemory::test_save_solution
```

## 📊 تقرير التغطية - Coverage Report

بعد تشغيل الاختبارات، افتح:
```
htmlcov/index.html
```

لعرض تقرير التغطية الكامل.

---

**ملاحظة**: تأكد من أنك في مجلد المشروع الرئيسي عند التشغيل!

