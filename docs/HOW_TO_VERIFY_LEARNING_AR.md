# كيفية التحقق من أن الـ Agent تعلم وحفظ المعلومات
## How to Verify Agent Learning

## 📍 أين تُخزن المعلومات؟ Where is Information Stored?

المعلومات تُخزن في مكانين رئيسيين:

### 1. قاعدة المعرفة (Knowledge Base)
**المسار:** `data/knowledge_base/`

كل تقنية لها مجلد خاص بها. على سبيل المثال:
- `data/knowledge_base/system_info/` - معلومات عن System Info
- `data/knowledge_base/docker/` - معلومات عن Docker
- `data/knowledge_base/python/` - معلومات عن Python

**الملفات:**
- `overview.md` - نظرة عامة
- `system_info_best_practices.md` - أفضل الممارسات
- `system_info_examples.md` - أمثلة

### 2. قاعدة بيانات الذاكرة (Memory Database)
**المسار:** `data/agent_memory.db`

تحتوي على:
- الحلول السابقة (Solutions)
- الأدوات المخصصة (Custom Tools)
- تفضيلات المستخدم (Preferences)

---

## ✅ كيفية التحقق How to Verify

### الطريقة 1: فحص قاعدة المعرفة

```powershell
# فحص إذا كان مجلد system_info موجود
Test-Path "data\knowledge_base\system_info"

# عرض محتويات المجلد
dir "data\knowledge_base\system_info"

# قراءة ملف محدد
Get-Content "data\knowledge_base\system_info\system_info_best_practices.md"
```

### الطريقة 2: استخدام Python Script

```python
from pathlib import Path

# فحص قاعدة المعرفة
kb_path = Path("data/knowledge_base/system_info")
if kb_path.exists():
    print("✅ المعلومات موجودة!")
    for file in kb_path.glob("*.md"):
        print(f"  - {file.name}")
        print(f"    الحجم: {file.stat().st_size} bytes")
else:
    print("❌ المعلومات غير موجودة - الـ Agent لم يحفظ")
```

### الطريقة 3: فحص قاعدة البيانات

```python
from src.core.memory import Memory

memory = Memory()
stats = memory.get_statistics()
print(f"عدد الحلول المحفوظة: {stats['total_solutions']}")
print(f"متوسط التقييم: {stats['average_rating']}")
```

---

## 🔍 مثال عملي: التحقق من System Info

بعد تشغيل الـ Agent على المهمة:
**"Learn system info best practices and save examples for offline use"**

### ما يجب أن يحدث:
1. ✅ إنشاء مجلد `data/knowledge_base/system_info/`
2. ✅ حفظ ملف `system_info_best_practices.md`
3. ✅ حفظ ملف `system_info_examples.md`
4. ✅ عرض رسالة نجاح من الـ Agent

### إذا لم يحدث:
- ❌ المجلد غير موجود = الأدوات لم تُنفذ
- ❌ الملفات غير موجودة = المعلومات لم تُحفظ

---

## 🛠️ حل المشكلة Fixing the Issue

إذا كانت الأدوات لم تُنفذ (كما في حالتك):

### السبب:
الـ Agent كان يرسل JSON بصيغة `{"action": "...", "action_input": {...}}` 
لكن الكود كان يبحث عن `{"tool": "...", "args": [...]}`

### الحل:
✅ تم إصلاح المشكلة في `src/agents/expert_agent.py`

الآن الـ Agent يدعم كلا الصيغتين:
- `{"tool": "...", "args": [...]}` (الصيغة القديمة)
- `{"action": "...", "action_input": {...}}` (الصيغة الجديدة)

### الخطوة التالية:
**جرّب تشغيل المهمة مرة أخرى!** الآن يجب أن تعمل الأدوات بشكل صحيح.

---

## 📝 سكريبت للتحقق السريع Quick Verification Script

أنشئ ملف `verify_learning.py`:

```python
"""سكريبت للتحقق من حفظ المعلومات"""
from pathlib import Path

def verify_learning(technology: str):
    """التحقق من حفظ معلومات تقنية معينة"""
    kb_path = Path("data/knowledge_base") / technology.lower().replace(" ", "_")
    
    if not kb_path.exists():
        print(f"❌ {technology}: غير موجود - لم يتم الحفظ")
        return False
    
    files = list(kb_path.glob("*.md"))
    if not files:
        print(f"⚠️ {technology}: المجلد موجود لكن فارغ")
        return False
    
    print(f"✅ {technology}: موجود!")
    for file in files:
        size = file.stat().st_size
        print(f"   📄 {file.name} ({size} bytes)")
    return True

# مثال
if __name__ == "__main__":
    verify_learning("system_info")
    verify_learning("docker")
    verify_learning("python")
```

---

## 🎯 الخلاصة Summary

1. **أين تُخزن؟** → `data/knowledge_base/[technology_name]/`
2. **كيف تتحقق؟** → فحص وجود المجلد والملفات
3. **المشكلة السابقة؟** → تم إصلاحها ✅
4. **الخطوة التالية؟** → جرّب المهمة مرة أخرى!

