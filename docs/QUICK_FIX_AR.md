# Quick Fix Guide - حل سريع

## المشكلة الحالية:
1. ❌ `gemma3:27b` بطيء جداً (timeout)
2. ❌ `qwen2.5:0.5b` ضعيف جداً (مش بيفهم)
3. ❌ الإيجنت مش بينفذ الأوامر صح

## الحل الفوري: 🚀

### استخدم `mistral:latest` أو `qwen2.5:3b`

عند تشغيل الإيجنت:
```
python examples/interactive_session.py
```

**اختار:**
```
Your choice (1/2/3): 2  ← Manual
Select model (1-6): 4   ← mistral:latest
```

أو:
```
Your choice (1/2/3): 2  ← Manual  
Select model (1-6): 2   ← qwen2.5:3b
```

## ليه الموديلات دي؟

| Model | Speed | Quality | Best For |
|-------|-------|---------|----------|
| **mistral:latest** | ⚡⚡⚡ سريع | ⭐⭐⭐⭐ ممتاز | كل حاجة |
| **qwen2.5:3b** | ⚡⚡⚡⚡ أسرع | ⭐⭐⭐ جيد | ملفات وأوامر |
| gemma3:27b | 🐌 بطيء جداً | ⭐⭐⭐⭐⭐ | معقد بس بطيء |
| deepseek-r1:8b | 🐌 بطيء | ⭐⭐⭐⭐ | كود بس بطيء |
| qwen2.5:0.5b | ⚡⚡⚡⚡⚡ | ⭐ ضعيف | ❌ مش مفيد |

## توصيتي ليك:

### استخدم `mistral:latest` دايماً! 🎯

**ليه؟**
- ✅ سريع (5-15 ثانية)
- ✅ ذكي (يفهم ويعمل صح)
- ✅ يشتغل على كل المهام
- ✅ مش بيعلق

## مثال:

```
👉 Your task: Create a Python calculator project

🚀 Executing with mistral:latest...
✅ First token received after 2.3s
✅ Complete - Received 150 tokens in 8.5s

💭 Thinking Draft
I need to create a calculator project with user input.

🔧 Executing Tool: create_project
✅ Tool Result: Project created successfully

🔧 Executing Tool: write_file  
✅ Tool Result: File created: calculator/main.py

🏁 Final Answer
I created a Python calculator project with:
- Project folder: calculator/
- Main file: calculator/main.py
- Features: Add, subtract, multiply, divide
```

## الخلاصة:

**استخدم `mistral:latest` = مشاكلك هتخلص! 🎉**

---

## ملحوظة مهمة:

لو عاوز الإيجنت يتعلم ويبقى أذكى، لازم:
1. تستخدم موديل كويس (mistral أو qwen2.5:3b)
2. تديله وقت يفكر
3. تشوف الـ "Thinking Draft" عشان تعرف بيفكر إزاي

**الموديلات الضعيفة (qwen2.5:0.5b) مش هتنفع أبداً!**
