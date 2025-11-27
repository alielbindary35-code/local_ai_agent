# 🔧 كيفية تشغيل السكريبتات / How to Run Scripts

## ⚠️ خطأ شائع / Common Mistake

**❌ خطأ / Wrong:**
```powershell
python merge_colab_results.ps1  # ❌ هذا خطأ!
```

**✅ صحيح / Correct:**
```powershell
.\merge_colab_results.ps1  # ✅ هذا صحيح!
```

---

## 📋 طرق تشغيل PowerShell Scripts

### الطريقة 1: مباشرة (الأسهل)
**Method 1: Direct (Easiest)**

```powershell
.\merge_colab_results.ps1
```

### الطريقة 2: مع Execution Policy
**Method 2: With Execution Policy**

إذا واجهت مشكلة Execution Policy:
```powershell
powershell -ExecutionPolicy Bypass -File .\merge_colab_results.ps1
```

### الطريقة 3: من PowerShell ISE
**Method 3: From PowerShell ISE**

1. افتح PowerShell ISE
2. File → Open → اختر `merge_colab_results.ps1`
3. اضغط F5 أو Run

---

## 🔍 حل مشاكل Execution Policy

إذا ظهرت رسالة:
```
cannot be loaded because running scripts is disabled on this system
```

**الحل / Solution:**

```powershell
# تحقق من السياسة الحالية
Get-ExecutionPolicy

# غيّر السياسة للجلسة الحالية فقط
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process

# الآن شغّل السكريبت
.\merge_colab_results.ps1
```

أو بشكل دائم (يحتاج صلاحيات Admin):
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## 📝 جميع السكريبتات المتاحة

| السكريبت / Script | الوصف / Description | طريقة التشغيل / How to Run |
|-------------------|---------------------|---------------------------|
| `merge_colab_results.ps1` | دمج نتائج Colab | `.\merge_colab_results.ps1` |
| `verify_knowledge_base.ps1` | التحقق من قاعدة المعرفة | `.\verify_knowledge_base.ps1` |
| `setup_github.ps1` | إعداد GitHub | `.\setup_github.ps1` |
| `run_auto_learning.ps1` | تشغيل التعلم التلقائي | `.\run_auto_learning.ps1` |

---

## 🐍 Python Scripts (ملفات Python)

ملفات Python (`.py`) يتم تشغيلها بـ Python:
```powershell
python src/tools/auto_learner.py
python generate_colab_notebook.py
```

---

## ✅ Checklist

- [ ] أنت في PowerShell (ليس Python shell)
- [ ] أنت في مجلد المشروع
- [ ] استخدم `.\` قبل اسم السكريبت
- [ ] إذا لزم الأمر، غيّر Execution Policy

---

## 🎯 مثال كامل / Complete Example

```powershell
# 1. تأكد أنك في المجلد الصحيح
cd "C:\Users\engha\Music\New folder1\local_ai_agent"

# 2. تحقق من Execution Policy
Get-ExecutionPolicy

# 3. إذا لزم الأمر، غيّره
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process

# 4. شغّل السكريبت
.\merge_colab_results.ps1
```

---

**Remember: `.ps1` = PowerShell, `.py` = Python!** 🚀

