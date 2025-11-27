# 🎓 دليل الوكيل الخبير - Expert Agent Guide

## 🌟 نظرة عامة

الـ **Expert Agent** هو نسخة متقدمة من الـ AI Agent مع قدرات احترافية:

### ✨ المميزات الرئيسية:

1. **🤖 اختيار تلقائي للموديل**
   - يحلل المهمة ويختار أفضل موديل تلقائياً
   - 5 موديلات متاحة لمهام مختلفة
   - نظام scoring ذكي للاختيار الأمثل

2. **🛠️ 67+ أداة متخصصة**
   - 22 أداة أساسية (ملفات، أوامر، ويب)
   - 45 أداة متخصصة (برمجة، مواقع، سيرفرات، Docker، PostgreSQL، n8n)

3. **📚 تعلم أونلاين**
   - يبحث في الإنترنت عن حلول
   - يحفظ المعرفة للاستخدام offline
   - يحمّل tutorials ويحفظها

4. **🎯 كشف نوع المهمة**
   - يكتشف تلقائياً: برمجة، مواقع، سيرفرات، Docker، قواعد بيانات
   - يختار الموديل والأدوات المناسبة

---

## 📊 الموديلات المتاحة

| الموديل | الحجم | التخصص | الأفضل لـ |
|---------|-------|---------|-----------|
| **deepseek-r1:8b** | 5.2 GB | 💻 **برمجة** | Python, JavaScript, debugging, code review |
| **mistral:latest** | 4.4 GB | 🧠 عام | تحليل، تفكير، مهام عامة |
| **llama3.2:latest** | 2.0 GB | 💬 محادثة | أسئلة عامة، شرح |
| **qwen2.5:3b** | 1.9 GB | ⚡ سريع | عمليات ملفات، معلومات نظام |
| **qwen2.5:0.5b** | 0.4 GB | 🚀 أسرع | أسئلة بسيطة جداً |

---

## 🎯 أنواع المهام المدعومة

### 1. 💻 البرمجة (Coding)
**الموديل المختار**: deepseek-r1:8b

**أمثلة**:
```
- Create a Python function to calculate fibonacci
- Debug this JavaScript code
- Write a REST API with FastAPI
- Refactor this code for better performance
```

**الأدوات المتاحة**:
- `create_python_project` - إنشاء مشروع Python
- `generate_code` - توليد كود من وصف
- `analyze_code` - تحليل جودة الكود
- `refactor_code` - تحسين الكود
- `create_api` - إنشاء API

---

### 2. 🌐 تصميم المواقع (Web Design)
**الموديل المختار**: deepseek-r1:8b

**أمثلة**:
```
- Design a landing page with HTML/CSS
- Create a responsive navbar
- Generate a React component for user profile
- Optimize images for web
```

**الأدوات المتاحة**:
- `create_html_template` - قوالب HTML
- `generate_css` - توليد CSS
- `create_react_component` - مكونات React
- `optimize_images` - تحسين الصور
- `generate_responsive_layout` - تصميم responsive

---

### 3. 🖥️ إدارة السيرفرات (Server Management)
**الموديل المختار**: mistral:latest أو llama3.2

**أمثلة**:
```
- Check server health
- Setup nginx configuration
- Monitor server logs
- Create server backup
```

**الأدوات المتاحة**:
- `check_server_health` - فحص صحة السيرفر
- `manage_nginx` - إدارة nginx
- `setup_ssl` - إعداد SSL
- `monitor_logs` - مراقبة السجلات
- `backup_server` - نسخ احتياطي

---

### 4. 🐳 Docker & Containers
**الموديل المختار**: deepseek-r1:8b

**أمثلة**:
```
- Create a Dockerfile for Python app
- Generate docker-compose for PostgreSQL and n8n
- Deploy Docker container
- Check Docker health
```

**الأدوات المتاحة**:
- `create_dockerfile` - إنشاء Dockerfile
- `docker_compose_generate` - توليد docker-compose.yml
- `docker_build` - بناء image
- `docker_deploy` - نشر container
- `docker_logs` - عرض السجلات
- `docker_health_check` - فحص الصحة
- `docker_cleanup` - تنظيف الموارد

---

### 5. 🗄️ PostgreSQL & Databases
**الموديل المختار**: deepseek-r1:8b

**أمثلة**:
```
- Execute PostgreSQL query
- Backup PostgreSQL database
- Create table in PostgreSQL
- Optimize database performance
```

**الأدوات المتاحة**:
- `postgres_query` - تنفيذ استعلام
- `postgres_backup` - نسخ احتياطي
- `postgres_restore` - استعادة
- `postgres_create_table` - إنشاء جدول
- `postgres_optimize` - تحسين الأداء
- `postgres_health` - فحص الصحة

---

### 6. 🔄 n8n Workflows
**الموديل المختار**: mistral:latest

**أمثلة**:
```
- Create n8n workflow for automation
- Export n8n workflow
- Test n8n webhook
```

**الأدوات المتاحة**:
- `create_n8n_workflow` - إنشاء workflow
- `n8n_api_call` - استدعاء API
- `export_n8n_workflow` - تصدير
- `import_n8n_workflow` - استيراد
- `test_n8n_webhook` - اختبار webhook

---

### 7. 📚 التعلم الأونلاين (Online Learning)
**الموديل المختار**: أي موديل

**أمثلة**:
```
- Learn Docker basics
- Search PostgreSQL documentation
- Find solution on StackOverflow
- Save code snippet for later
```

**الأدوات المتاحة**:
- `search_documentation` - بحث في التوثيق
- `download_tutorial` - تحميل دروس
- `save_code_snippet` - حفظ أكواد
- `search_stackoverflow` - بحث في StackOverflow
- `learn_new_technology` - تعلم تقنية جديدة

---

## 🚀 كيفية الاستخدام

### الطريقة 1: استخدام مباشر
```python
from expert_agent import ExpertAgent

# إنشاء الـ agent
agent = ExpertAgent()

# تنفيذ مهمة (يختار الموديل تلقائياً)
response = agent.run("Create a Python function to calculate fibonacci")

# أو حدد نوع المهمة بنفسك
response = agent.run("Setup Docker container", task_type="docker")
```

### الطريقة 2: من Terminal
```bash
python expert_agent.py
```

---

## 💡 أمثلة عملية

### مثال 1: إنشاء مشروع Python
```python
agent = ExpertAgent()
agent.run("Create a new Python project called 'my_api' with tests and docs")
```
**النتيجة**:
- يختار deepseek-r1:8b (للبرمجة)
- ينشئ المشروع بالهيكل الكامل
- يضيف tests/ و docs/

---

### مثال 2: Docker Compose لـ PostgreSQL + n8n
```python
agent.run("Generate docker-compose file for PostgreSQL and n8n")
```
**النتيجة**:
- يختار deepseek-r1:8b
- يولد docker-compose.yml كامل
- يضبط الإعدادات والـ volumes

---

### مثال 3: تعلم تقنية جديدة
```python
agent.run("Learn Docker basics and save for offline use")
```
**النتيجة**:
- يبحث في الإنترنت
- يحمّل الدروس
- يحفظ في knowledge_base/

---

## 🎯 نظام اختيار الموديل

### كيف يختار الموديل؟

1. **كشف نوع المهمة** من الكلمات المفتاحية
2. **حساب Score لكل موديل**:
   - +100 للموديل المتخصص
   - +30 للموديلات الكبيرة (>4GB) في المهام المعقدة
   - +50-80 للموديلات المناسبة

3. **اختيار الموديل بأعلى Score**

### مثال:
```
Task: "Create a Python API"
→ Type: coding
→ Scores:
  - deepseek-r1:8b: 130 (100 coding + 30 size) ✅
  - mistral:latest: 75
  - qwen2.5:3b: 50
→ Selected: deepseek-r1:8b
```

---

## 📁 هيكل المشروع

```
local_ai_agent/
├── expert_agent.py          # الـ Agent الخبير
├── expert_tools.py          # 45+ أداة متخصصة
├── tools.py                 # 22 أداة أساسية
├── memory.py                # نظام الذاكرة
├── knowledge_base/          # المعرفة المحفوظة
│   ├── snippets/           # أكواد محفوظة
│   ├── tutorials/          # دروس محملة
│   └── documentation/      # توثيق محفوظ
└── logs/                    # السجلات
```

---

## 🔧 الإعدادات المتقدمة

### تخصيص الـ Agent
```python
agent = ExpertAgent(
    ollama_url="http://localhost:11434",
    max_iterations=8,              # عدد المحاولات
    auto_approve=False,            # طلب موافقة المستخدم
    enable_online_learning=True    # تفعيل التعلم الأونلاين
)
```

### إضافة موديل جديد
```bash
# حمّل موديل جديد
ollama pull codellama:13b

# سيظهر تلقائياً في Expert Agent
```

---

## 📊 مقارنة: Simple Agent vs Expert Agent

| الميزة | Simple Agent | Expert Agent |
|--------|--------------|--------------|
| **عدد الموديلات** | 1 (ثابت) | 5 (يختار تلقائياً) |
| **عدد الأدوات** | 22 | 67+ |
| **اختيار الموديل** | ❌ يدوي | ✅ تلقائي |
| **كشف نوع المهمة** | ❌ لا | ✅ نعم |
| **تعلم أونلاين** | ❌ لا | ✅ نعم |
| **تخصص** | عام | متعدد (برمجة، مواقع، سيرفرات، إلخ) |
| **الأفضل لـ** | مهام بسيطة | مهام احترافية معقدة |

---

## 🎓 نصائح للاستخدام الأمثل

### 1. كن محدداً في طلبك
❌ سيء: "Help with Docker"  
✅ جيد: "Create a Dockerfile for Python FastAPI app with PostgreSQL"

### 2. استخدم الكلمات المفتاحية
- للبرمجة: "code", "function", "debug", "python"
- للمواقع: "website", "HTML", "CSS", "design"
- للـ Docker: "docker", "container", "dockerfile"

### 3. استفد من التعلم الأونلاين
```python
# تعلم وحفظ للاستخدام offline
agent.run("Learn PostgreSQL optimization techniques and save examples")
```

### 4. راجع السجلات
```bash
# شوف الموديلات المستخدمة
cat logs/expert_agent_*.log
```

---

## 🚨 حل المشاكل

### المشكلة: "Model not found"
```bash
# تأكد من تحميل الموديلات
ollama list

# حمّل الموديل المطلوب
ollama pull deepseek-r1:8b
```

### المشكلة: "Tool not found"
- تأكد من استيراد `expert_tools.py`
- راجع قائمة الأدوات: `expert_tools.get_tool_descriptions()`

### المشكلة: بطء في الاستجابة
- استخدم موديل أصغر للمهام البسيطة
- قلل `max_iterations`

---

## 📞 الدعم

### أسئلة شائعة:
1. **كم عدد الأدوات المتاحة؟** 67+ أداة (22 أساسية + 45 متخصصة)
2. **هل يعمل offline؟** نعم، بعد تحميل المعرفة
3. **كيف أضيف أداة جديدة؟** أضفها في `expert_tools.py`

---

**آخر تحديث**: 2025-11-27  
**الإصدار**: 1.0 Expert Edition  
**الحالة**: ✅ جاهز للإنتاج
