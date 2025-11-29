# 🎓 Local AI Agent - Complete Project Guide
# دليل المشروع الكامل - وكيل الذكاء الاصطناعي المحلي

---

## Table of Contents - جدول المحتويات

### English
1. [Project Overview](#project-overview)
2. [Quick Start](#quick-start)
3. [Features](#features)
4. [Architecture](#architecture)
5. [Installation](#installation)
6. [Usage](#usage)
7. [Knowledge Harvester](#knowledge-harvester)
8. [Training & Evaluation](#training--evaluation)
9. [Tools & Capabilities](#tools--capabilities)
10. [Troubleshooting](#troubleshooting)

### العربية
1. [نظرة عامة على المشروع](#نظرة-عامة-على-المشروع)
2. [البدء السريع](#البدء-السريع)
3. [الميزات](#الميزات)
4. [البنية المعمارية](#البنية-المعمارية)
5. [التثبيت](#التثبيت)
6. [الاستخدام](#الاستخدام)
7. [جامع المعرفة](#جامع-المعرفة)
8. [التدريب والتقييم](#التدريب-والتقييم)
9. [الأدوات والقدرات](#الأدوات-والقدرات)
10. [حل المشاكل](#حل-المشاكل)

---

# English Documentation

## Project Overview

**Local AI Agent** is a powerful, self-improving AI system that runs entirely on your local server using Ollama. It combines advanced reasoning capabilities with 120+ specialized tools to help you with system administration, data analysis, development, and automation tasks.

### Key Highlights

- 🧠 **Advanced ReAct Loop**: Multi-step reasoning with self-reflection
- 🤖 **Multi-Model Intelligence**: Auto-selects best model based on task complexity
- 🛠️ **120+ Tools**: Comprehensive toolkit for various tasks
- 💾 **Continuous Learning**: SQLite-based memory system
- 🔒 **Security First**: Risk assessment and explicit permission
- 🌐 **Offline Capable**: Works completely offline with local knowledge base
- 📦 **Knowledge Harvester**: Automatically downloads and organizes documentation

## Quick Start

### Prerequisites

1. **Python 3.8+** installed
2. **Ollama** installed and running ([Download](https://ollama.ai/))
3. At least one Ollama model (e.g., `ollama pull qwen2.5:3b`)

### Using the Menu System

The easiest way to use the project is through the unified menu:

```cmd
menu.bat
```

This provides access to all features:
- Run Agent (Interactive Mode)
- Run Expert Agent
- Import Knowledge from Harvester
- Training & Evaluation
- Testing
- Knowledge Harvester Operations

### Manual Installation

```cmd
cd local_ai_agent
python -m pip install -r requirements.txt
python -m src.agents.simple_agent
```

## Features

### 1. Multi-Level Intelligence

- **Simple Agent**: Fast responses for basic tasks
- **Expert Agent**: Advanced reasoning for complex problems
- **Model Selection**: Automatic selection based on task complexity

### 2. Knowledge Harvester

Automatically downloads and organizes documentation from:
- Python (Pandas, NumPy)
- JavaScript & Node.js
- Docker
- PostgreSQL
- n8n
- Ollama
- General AI/ML resources

### 3. Continuous Learning

- Stores successful solutions
- Remembers custom tools
- Tracks package installations
- Learns from errors

### 4. Security & Privacy

- 100% Local processing
- No cloud dependencies
- Explicit permission for every action
- Color-coded risk levels (🟢🟡🔴)
- Complete audit log

## Architecture

```
┌─────────────────────────────────────┐
│           USER INPUT                │
│     (Natural Language)              │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│      EXPERT AGENT                   │
│  ┌──────────┐  ┌──────────────┐    │
│  │  ReAct   │  │ Multi-Model  │    │
│  │   Loop   │  │ Orchestrator │    │
│  └──────────┘  └──────────────┘    │
└────────────┬────────────────────────┘
             │
    ┌────────┼────────┐
    │        │        │
    ▼        ▼        ▼
┌────────┐ ┌────┐ ┌────────┐
│ TOOLS  │ │ KB │ │PROMPTS │
│  120+  │ │    │ │        │
└────────┘ └────┘ └────────┘
    │        │        │
    └────────┼────────┘
             │
             ▼
      ┌─────────────┐
      │   OLLAMA    │
      │ (Local AI)  │
      └─────────────┘
```

## Installation

### Step 1: Install Dependencies

```cmd
pip install -r requirements.txt
```

### Step 2: Pull Ollama Models

```cmd
ollama pull qwen2.5:3b
ollama pull qwen2.5:7b
```

### Step 3: Run Knowledge Harvester

```cmd
cd KnowledgeHarvester
python knowledge_harvester.py
```

### Step 4: Import Knowledge

```cmd
python scripts/import_knowledge.py
```

## Usage

### Interactive Mode

```cmd
python -m src.agents.simple_agent
```

### Expert Mode

```cmd
python -m src.agents.expert_agent
```

### Example Interactions

**System Administration:**
```
You: Check my disk space and warn me if it's low
Agent: [Executes df command] Your disk space is healthy. 45% used (120GB free).
```

**Data Analysis:**
```
You: Analyze sales.xlsx and show me the top 5 products
Agent: [Reads Excel file with pandas] Top 5 Products by Revenue: ...
```

**Docker Management:**
```
You: List all running containers
Agent: [Executes docker ps] Currently running: nginx, postgres, redis
```

## Knowledge Harvester

The Knowledge Harvester automatically downloads and organizes documentation.

### Configuration

Edit `KnowledgeHarvester/config.yaml` to add new sources:

```yaml
sources:
  my_category:
    urls:
      - url: "https://example.com/docs"
        title: "Example Documentation"
        type: "html"
```

### Running the Harvester

**All Topics:**
```cmd
cd KnowledgeHarvester
python knowledge_harvester.py
```

**Specific Category:**
```cmd
python knowledge_harvester.py --category docker
```

### Importing to Knowledge Base

```cmd
python scripts/import_knowledge.py
```

## Training & Evaluation

### Quick Training

```cmd
python -m src.core.train_agent
```

### Comprehensive Training

```cmd
python -m src.core.comprehensive_training
```

### Evaluation

```cmd
python -m src.core.comprehensive_evaluation
```

## Tools & Capabilities

### File System (20+ tools)
- Read/Write files
- List directories
- Search files
- Check permissions

### Command Execution
- Cross-platform command execution
- Background process management

### Web Access
- DuckDuckGo search
- Web scraping
- API requests
- File downloads

### Package Management
- pip, npm, apt, choco, brew support
- Automatic installation

### Code Execution
- Python REPL with pandas
- Safe code execution

### Docker
- Container management
- Image operations
- Docker Compose support

### Database
- PostgreSQL integration
- SQL execution
- Data analysis

### Security
- Port scanning
- SSL certificate checking
- Security audits

## Troubleshooting

### Ollama Not Running

```cmd
# Check if Ollama is running
ollama list

# Start Ollama service
ollama serve
```

### Import Errors

```cmd
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Knowledge Base Issues

```cmd
# Check database
python -c "from src.core.knowledge_base import KnowledgeBase; kb = KnowledgeBase(); print(kb.get_statistics())"
```

---

# التوثيق العربي

## نظرة عامة على المشروع

**وكيل الذكاء الاصطناعي المحلي** هو نظام ذكاء اصطناعي قوي ومتطور ذاتياً يعمل بالكامل على خادمك المحلي باستخدام Ollama. يجمع بين قدرات التفكير المتقدمة وأكثر من 120 أداة متخصصة لمساعدتك في إدارة النظام وتحليل البيانات والتطوير ومهام الأتمتة.

### النقاط الرئيسية

- 🧠 **حلقة ReAct متقدمة**: تفكير متعدد الخطوات مع التأمل الذاتي
- 🤖 **ذكاء متعدد النماذج**: يختار تلقائياً أفضل نموذج بناءً على تعقيد المهمة
- 🛠️ **120+ أداة**: مجموعة أدوات شاملة لمختلف المهام
- 💾 **التعلم المستمر**: نظام ذاكرة قائم على SQLite
- 🔒 **الأمان أولاً**: تقييم المخاطر والإذن الصريح
- 🌐 **قادر على العمل بدون اتصال**: يعمل بالكامل بدون اتصال بالإنترنت مع قاعدة معرفة محلية
- 📦 **جامع المعرفة**: يقوم تلقائياً بتنزيل وتنظيم الوثائق

## البدء السريع

### المتطلبات الأساسية

1. **Python 3.8+** مثبت
2. **Ollama** مثبت وقيد التشغيل ([تحميل](https://ollama.ai/))
3. نموذج Ollama واحد على الأقل (مثال: `ollama pull qwen2.5:3b`)

### استخدام نظام القائمة

أسهل طريقة لاستخدام المشروع هي من خلال القائمة الموحدة:

```cmd
menu.bat
```

توفر هذه القائمة الوصول إلى جميع الميزات:
- تشغيل الوكيل (الوضع التفاعلي)
- تشغيل الوكيل الخبير
- استيراد المعرفة من الجامع
- التدريب والتقييم
- الاختبار
- عمليات جامع المعرفة

### التثبيت اليدوي

```cmd
cd local_ai_agent
python -m pip install -r requirements.txt
python -m src.agents.simple_agent
```

## الميزات

### 1. الذكاء متعدد المستويات

- **الوكيل البسيط**: استجابات سريعة للمهام الأساسية
- **الوكيل الخبير**: تفكير متقدم للمشاكل المعقدة
- **اختيار النموذج**: اختيار تلقائي بناءً على تعقيد المهمة

### 2. جامع المعرفة

يقوم تلقائياً بتنزيل وتنظيم الوثائق من:
- Python (Pandas, NumPy)
- JavaScript و Node.js
- Docker
- PostgreSQL
- n8n
- Ollama
- موارد الذكاء الاصطناعي/التعلم الآلي العامة

### 3. التعلم المستمر

- يخزن الحلول الناجحة
- يتذكر الأدوات المخصصة
- يتتبع تثبيتات الحزم
- يتعلم من الأخطاء

### 4. الأمان والخصوصية

- معالجة محلية 100%
- لا توجد تبعيات سحابية
- إذن صريح لكل إجراء
- مستويات مخاطر مرمزة بالألوان (🟢🟡🔴)
- سجل تدقيق كامل

## البنية المعمارية

```
┌─────────────────────────────────────┐
│        إدخال المستخدم               │
│      (اللغة الطبيعية)              │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│      الوكيل الخبير                 │
│  ┌──────────┐  ┌──────────────┐    │
│  │  حلقة    │  │  منسق       │    │
│  │  ReAct   │  │  النماذج    │    │
│  └──────────┘  └──────────────┘    │
└────────────┬────────────────────────┘
             │
    ┌────────┼────────┐
    │        │        │
    ▼        ▼        ▼
┌────────┐ ┌────┐ ┌────────┐
│ الأدوات│ │ق.م│ │القوالب│
│  120+  │ │    │ │        │
└────────┘ └────┘ └────────┘
    │        │        │
    └────────┼────────┘
             │
             ▼
      ┌─────────────┐
      │   OLLAMA    │
      │  (ذكاء محلي)│
      └─────────────┘
```

## التثبيت

### الخطوة 1: تثبيت التبعيات

```cmd
pip install -r requirements.txt
```

### الخطوة 2: سحب نماذج Ollama

```cmd
ollama pull qwen2.5:3b
ollama pull qwen2.5:7b
```

### الخطوة 3: تشغيل جامع المعرفة

```cmd
cd KnowledgeHarvester
python knowledge_harvester.py
```

### الخطوة 4: استيراد المعرفة

```cmd
python scripts/import_knowledge.py
```

## الاستخدام

### الوضع التفاعلي

```cmd
python -m src.agents.simple_agent
```

### وضع الخبير

```cmd
python -m src.agents.expert_agent
```

### أمثلة على التفاعلات

**إدارة النظام:**
```
أنت: تحقق من مساحة القرص وحذرني إذا كانت منخفضة
الوكيل: [ينفذ أمر df] مساحة القرص لديك جيدة. 45% مستخدمة (120GB متاحة).
```

**تحليل البيانات:**
```
أنت: حلل ملف sales.xlsx وأظهر لي أفضل 5 منتجات
الوكيل: [يقرأ ملف Excel باستخدام pandas] أفضل 5 منتجات حسب الإيرادات: ...
```

**إدارة Docker:**
```
أنت: اعرض جميع الحاويات قيد التشغيل
الوكيل: [ينفذ docker ps] قيد التشغيل حالياً: nginx, postgres, redis
```

## جامع المعرفة

يقوم جامع المعرفة تلقائياً بتنزيل وتنظيم الوثائق.

### التكوين

قم بتحرير `KnowledgeHarvester/config.yaml` لإضافة مصادر جديدة:

```yaml
sources:
  my_category:
    urls:
      - url: "https://example.com/docs"
        title: "وثائق المثال"
        type: "html"
```

### تشغيل الجامع

**جميع المواضيع:**
```cmd
cd KnowledgeHarvester
python knowledge_harvester.py
```

**فئة محددة:**
```cmd
python knowledge_harvester.py --category docker
```

### الاستيراد إلى قاعدة المعرفة

```cmd
python scripts/import_knowledge.py
```

## التدريب والتقييم

### التدريب السريع

```cmd
python -m src.core.train_agent
```

### التدريب الشامل

```cmd
python -m src.core.comprehensive_training
```

### التقييم

```cmd
python -m src.core.comprehensive_evaluation
```

## الأدوات والقدرات

### نظام الملفات (20+ أداة)
- قراءة/كتابة الملفات
- عرض الدلائل
- البحث عن الملفات
- التحقق من الأذونات

### تنفيذ الأوامر
- تنفيذ الأوامر عبر الأنظمة الأساسية
- إدارة العمليات في الخلفية

### الوصول إلى الويب
- بحث DuckDuckGo
- استخراج محتوى الويب
- طلبات API
- تنزيل الملفات

### إدارة الحزم
- دعم pip, npm, apt, choco, brew
- التثبيت التلقائي

### تنفيذ الكود
- Python REPL مع pandas
- تنفيذ آمن للكود

### Docker
- إدارة الحاويات
- عمليات الصور
- دعم Docker Compose

### قاعدة البيانات
- تكامل PostgreSQL
- تنفيذ SQL
- تحليل البيانات

### الأمان
- فحص المنافذ
- التحقق من شهادات SSL
- عمليات التدقيق الأمني

## حل المشاكل

### Ollama لا يعمل

```cmd
# تحقق من تشغيل Ollama
ollama list

# ابدأ خدمة Ollama
ollama serve
```

### أخطاء الاستيراد

```cmd
# أعد تثبيت التبعيات
pip install -r requirements.txt --force-reinstall
```

### مشاكل قاعدة المعرفة

```cmd
# تحقق من قاعدة البيانات
python -c "from src.core.knowledge_base import KnowledgeBase; kb = KnowledgeBase(); print(kb.get_statistics())"
```

---

## 📞 Support - الدعم

For issues or questions:
- Check the logs in `data/logs_backup/`
- Review `data/agent_log.txt`
- Consult individual documentation files in `docs/`

للمشاكل أو الأسئلة:
- تحقق من السجلات في `data/logs_backup/`
- راجع `data/agent_log.txt`
- استشر ملفات الوثائق الفردية في `docs/`

---

**Built with ❤️ for secure, local AI assistance**
**مبني بـ ❤️ للمساعدة الآمنة بالذكاء الاصطناعي المحلي**

🔒 Secure • 🏠 Local • 🧠 Smart • 📈 Self-Improving
🔒 آمن • 🏠 محلي • 🧠 ذكي • 📈 متطور ذاتياً
