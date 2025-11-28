# 📚 شرح نظام الـ AI Agent - دليل شامل

## نظرة عامة على النظام

نظام AI Agent محلي يعمل على Ollama ويتكون من 3 مستويات:

- **Simple Agent**: بسيط وسريع (22 أداة، موديل واحد)
- **Standard Agent**: متوسط (22 أداة، ReAct loop كامل)
- **Expert Agent**: احترافي (67+ أداة، اختيار تلقائي للموديل) ⭐

---

## البنية المعمارية الأساسية

### 1. المكونات الرئيسية

```
ExpertAgent (src/agents/expert_agent.py)
├── Tools (src/tools/tools.py) - 22 أداة أساسية
├── ExpertTools (src/tools/expert_tools.py) - 45+ أداة متخصصة
├── ExtendedTools (src/tools/extended_tools.py) - أدوات إضافية
├── Memory (src/core/memory.py) - نظام الذاكرة SQLite
└── AutoLearner (src/tools/auto_learner.py) - نظام التعلم التلقائي
```

### 2. تدفق العمل الرئيسي

```
User Input → Task Detection → Model Selection → ReAct Loop → Tool Execution → Response
```

---

## آلية عمل Expert Agent (المستوى الاحترافي)

### المرحلة 1: التهيئة (Initialization)

**الملف**: `src/agents/expert_agent.py` - دالة `__init__`

#### 1.1 جلب الموديلات المتاحة

عند بدء تشغيل الـ Agent، يقوم بالخطوات التالية:

```python
def _get_available_models(self) -> List[Dict[str, Any]]:
    """Get list of available models with their specs"""
    try:
        response = requests.get(f"{self.ollama_url}/api/tags")
        if response.status_code == 200:
            models = response.json().get('models', [])
            return [{
                'name': m['name'],
                'size': m.get('size', 0),
                'modified': m.get('modified_at', '')
            } for m in models]
        return []
    except Exception as e:
        console.print(f"[yellow]Warning: Could not fetch models: {e}[/yellow]")
        return []
```

**ما يحدث**:
- يرسل طلب GET إلى `http://localhost:11434/api/tags`
- يحصل على قائمة بجميع الموديلات المثبتة في Ollama
- يحفظ اسم الموديل، الحجم، وتاريخ التعديل

#### 1.2 تحليل قدرات الموديلات

```python
def _analyze_model_capabilities(self) -> Dict[str, Dict]:
    """Analyze capabilities of each model"""
    capabilities = {}
    
    for model in self.available_models:
        name = model['name']
        size = model.get('size', 0)
        
        # Determine capabilities based on model name and size
        caps = {
            'speed': 'fast',
            'accuracy': 'medium',
            'specialization': 'general',
            'best_for': []
        }
        
        # DeepSeek models - best for coding
        if 'deepseek' in name.lower():
            caps['specialization'] = 'coding'
            caps['accuracy'] = 'high'
            caps['best_for'] = ['programming', 'debugging', 'code_review', 'architecture']
        
        # Qwen models - balanced, good for reasoning
        elif 'qwen' in name.lower():
            if '0.5b' in name:
                caps['speed'] = 'very_fast'
                caps['accuracy'] = 'low'
                caps['best_for'] = ['simple_queries', 'quick_answers']
            elif '3b' in name:
                caps['speed'] = 'fast'
                caps['accuracy'] = 'medium'
                caps['best_for'] = ['general_tasks', 'file_operations', 'system_info']
            else:
                caps['accuracy'] = 'high'
                caps['best_for'] = ['complex_reasoning', 'analysis', 'planning']
        
        # Llama models - good for general tasks
        elif 'llama' in name.lower():
            caps['specialization'] = 'general'
            caps['accuracy'] = 'high'
            caps['best_for'] = ['conversation', 'general_tasks', 'reasoning']
        
        capabilities[name] = caps
    
    return capabilities
```

**ما يحدث**:
- دالة `_analyze_model_capabilities()` تحلل كل موديل
- تحدد التخصص (coding, general, conversation)
- تحدد السرعة والدقة بناءً على الحجم والاسم
- مثال: `deepseek-r1:8b` → تخصص: coding، دقة: high

#### 1.3 عرض المعلومات

```python
def _display_initialization(self):
    """Display initialization info"""
    # Create models table
    table = Table(title="🤖 Available Models", show_header=True)
    table.add_column("Model", style="cyan")
    table.add_column("Size", style="green")
    table.add_column("Specialization", style="yellow")
    table.add_column("Best For", style="blue")
    
    for model in self.available_models:
        name = model['name']
        size_gb = model.get('size', 0) / 1_000_000_000
        caps = self.model_capabilities.get(name, {})
        
        table.add_row(
            name,
            f"{size_gb:.1f} GB",
            caps.get('specialization', 'general'),
            ', '.join(caps.get('best_for', ['general'])[:2])
        )
    
    console.print(table)
```

**ما يحدث**:
- يعرض جدول بجميع الموديلات المتاحة
- يعرض عدد الأدوات المتاحة (67+)
- يعرض حالة التعلم الأونلاين

---

### المرحلة 2: استقبال الطلب (User Request)

**الملف**: `src/agents/expert_agent.py` - دالة `run()`

عندما يرسل المستخدم طلباً:

#### 2.1 عرض الطلب

```python
def run(self, user_input: str, task_type: str = None) -> str:
    """Run the expert agent with tool execution loop"""
    console.print(Panel(
        f"[bold cyan]{user_input}[/bold cyan]",
        title="🎯 Expert Task",
        border_style="cyan"
    ))
```

**ما يحدث**:
- يعرض الطلب في Panel باستخدام Rich library

#### 2.2 كشف نوع المهمة (Task Type Detection)

```python
def _detect_task_type(self, task_description: str) -> str:
    """Detect task type from description"""
    task_lower = task_description.lower()
    
    # Coding keywords
    if any(word in task_lower for word in ['code', 'program', 'function', 'class', 'debug', 'python', 'javascript', 'java', 'c++', 'algorithm']):
        return 'coding'
    
    # Web design keywords
    if any(word in task_lower for word in ['website', 'web', 'html', 'css', 'frontend', 'backend', 'ui', 'ux', 'design']):
        return 'web_design'
    
    # Server/DevOps keywords
    if any(word in task_lower for word in ['server', 'deploy', 'nginx', 'apache', 'linux', 'ubuntu', 'centos']):
        return 'server'
    
    # Docker keywords
    if any(word in task_lower for word in ['docker', 'container', 'dockerfile', 'compose', 'kubernetes', 'k8s']):
        return 'docker'
    
    # Database keywords
    if any(word in task_lower for word in ['database', 'sql', 'postgres', 'postgresql', 'mysql', 'mongodb', 'query']):
        return 'database'
    
    # n8n keywords
    if any(word in task_lower for word in ['n8n', 'workflow', 'automation', 'integration']):
        return 'automation'
    
    # Simple tasks
    if any(word in task_lower for word in ['what is', 'show', 'list', 'get', 'check', 'find']):
        return 'simple'
    
    return 'general'
```

**ما يحدث**:
- دالة `_detect_task_type()` تحلل النص
- تبحث عن كلمات مفتاحية:
  - `coding`: code, program, function, python, javascript
  - `web_design`: website, html, css, frontend
  - `server`: server, deploy, nginx, linux
  - `docker`: docker, container, dockerfile, compose
  - `database`: database, sql, postgres, mysql
  - `simple`: what is, show, list, get

#### 2.3 اختيار الموديل المناسب

```python
def _select_best_model(self, task_description: str, task_type: str = None) -> str:
    """Intelligently select the best model for the task"""
    if not self.available_models:
        return "qwen2.5:3b"  # Fallback
    
    # Auto-detect task type if not provided
    if not task_type:
        task_type = self._detect_task_type(task_description)
    
    console.print(f"[dim]🎯 Detected task type: {task_type}[/dim]")
    
    # Scoring system for model selection
    scores = {}
    
    for model in self.available_models:
        name = model['name']
        caps = self.model_capabilities.get(name, {})
        score = 0
        
        # Task-specific scoring
        if task_type == 'coding' or task_type == 'programming':
            if 'deepseek' in name.lower():
                score += 100  # DeepSeek is best for coding
            elif 'qwen' in name.lower() and '3b' not in name:
                score += 50
        
        elif task_type == 'web_design':
            if 'deepseek' in name.lower():
                score += 80
            elif 'qwen' in name.lower():
                score += 60
        
        elif task_type in ['server', 'docker', 'database', 'devops']:
            if 'deepseek' in name.lower():
                score += 90
            elif 'llama' in name.lower():
                score += 70
            elif 'mistral' in name.lower():
                score += 75
        
        elif task_type == 'simple':
            if '0.5b' in name or '3b' in name:
                score += 100  # Small models for simple tasks
        
        else:  # general tasks
            if 'mistral' in name.lower():
                score += 80
            elif 'llama' in name.lower():
                score += 75
            elif 'qwen' in name.lower() and '3b' not in name:
                score += 70
        
        # Size bonus (prefer larger models for complex tasks)
        size = model.get('size', 0)
        if task_type in ['coding', 'web_design', 'server', 'docker', 'database']:
            if size > 4_000_000_000:  # > 4GB
                score += 30
            elif size > 2_000_000_000:  # > 2GB
                score += 15
        
        scores[name] = score
    
    # Select model with highest score
    best_model = max(scores, key=scores.get)
    best_score = scores[best_model]
    
    console.print(f"[cyan]🤖 Selected model:[/cyan] [bold]{best_model}[/bold] (score: {best_score})")
    console.print(f"[dim]Reason: {self.model_capabilities.get(best_model, {}).get('specialization', 'general')} specialist[/dim]")
    
    return best_model
```

**نظام Scoring**:
```
إذا task_type == 'coding':
    deepseek-r1:8b: +100 (متخصص في البرمجة)
    qwen2.5:8b: +50
    mistral:latest: +30

إذا task_type == 'simple':
    qwen2.5:0.5b: +100 (صغير وسريع)
    qwen2.5:3b: +80

إذا task_type == 'docker' أو 'server':
    deepseek-r1:8b: +90
    llama3.2:latest: +70
```

**ما يحدث**:
- دالة `_select_best_model()` تحسب Score لكل موديل
- يختار الموديل بأعلى Score

---

### المرحلة 3: بناء الـ Prompt

**الملف**: `src/agents/expert_agent.py` - دالة `_build_expert_prompt()`

#### 3.1 جمع معلومات الأدوات

```python
def _build_expert_prompt(self, user_input: str, selected_model: str) -> str:
    """Build comprehensive prompt for expert agent"""
    
    # Get tool descriptions
    basic_tools = self.tools.get_tool_descriptions()
    expert_tools = self.expert_tools.get_tool_descriptions()
    extended_tools = self.extended_tools.get_tool_descriptions()
    
    all_tools = f"{basic_tools}\n\n{expert_tools}\n\n{extended_tools}"
```

**ما يحدث**:
- يجمع أوصاف جميع الأدوات من:
  - `tools.get_tool_descriptions()` (22 أداة أساسية)
  - `expert_tools.get_tool_descriptions()` (45+ أداة متخصصة)
  - `extended_tools.get_tool_descriptions()` (أدوات إضافية)

#### 3.2 بناء System Prompt

```python
    prompt = f"""You are an Expert AI Agent with access to powerful tools.

Available Tools:
{all_tools}

How to use tools:
- Use JSON format: {{"tool": "tool_name", "args": ["arg1", "arg2"]}}
- You can call multiple tools in sequence
- Read tool results before making decisions

Task: {user_input}

Instructions:
1. Analyze the task
2. Plan your approach
3. Use appropriate tools
4. Provide final answer

Start by thinking about the task, then use tools as needed.
"""
```

**ما يحدث**:
- يشرح للموديل:
  - ما هي الأدوات المتاحة
  - كيف يستخدمها (JSON format)
  - أمثلة على الاستخدام
  - التعليمات الخاصة بنوع المهمة

#### 3.3 إضافة السياق

```python
    # Add conversation history
    if self.conversation_history:
        prompt += "\n\nPrevious conversation:\n"
        for msg in self.conversation_history[-5:]:  # Last 5 messages
            prompt += f"- {msg}\n"
    
    # Add memory context if available
    similar_solutions = self.memory.search_similar(user_input)
    if similar_solutions:
        prompt += "\n\nSimilar past solutions:\n"
        for solution, rating in similar_solutions[:2]:
            prompt += f"- {solution[:200]}... (Rating: {rating}⭐)\n"
```

**ما يحدث**:
- يضيف تاريخ المحادثة السابق
- يضيف معلومات من الذاكرة (إن وجدت)

---

### المرحلة 4: استدعاء الموديل (Model Call)

**الملف**: `src/agents/expert_agent.py` - دالة `_call_ollama()`

#### 4.1 إرسال الطلب

```python
def _call_ollama(self, prompt: str, model: str, temperature: float = 0.7, use_fallback: bool = True) -> str:
    """Call Ollama API with streaming support"""
    try:
        url = f"{self.ollama_url}/api/generate"
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": True,
            "temperature": temperature,
            "options": {
                "num_predict": 4000,
                "top_p": 0.9,
                "top_k": 40
            }
        }
        
        response = requests.post(url, json=payload, stream=True, timeout=300)
        response.raise_for_status()
```

**ما يحدث**:
- يرسل POST request إلى `http://localhost:11434/api/generate`
- Body يحتوي على:
  ```json
  {
    "model": "deepseek-r1:8b",
    "prompt": "...",
    "stream": true,
    "temperature": 0.7
  }
  ```

#### 4.2 معالجة الرد المتدفق (Streaming)

```python
        # Stream response
        full_response = ""
        tokens_received = 0
        start_time = time.time()
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task(f"[cyan]Processing with {model}...", total=None)
            
            for line in response.iter_lines():
                if line:
                    try:
                        json_response = json.loads(line)
                        if 'response' in json_response:
                            token = json_response['response']
                            full_response += token
                            tokens_received += 1
                            
                            # Update progress
                            elapsed = time.time() - start_time
                            if elapsed > 0:
                                speed = tokens_received / elapsed
                                progress.update(
                                    task,
                                    description=f"[cyan]Processing... ({tokens_received} tokens @ {speed:.1f}/s, {elapsed:.0f}s elapsed)"
                                )
                        
                        if json_response.get('done', False):
                            break
                    except json.JSONDecodeError:
                        continue
```

**ما يحدث**:
- يستقبل الرد token بعد token
- يعرض Progress bar باستخدام Rich
- يجمع كل الـ tokens في response كامل

#### 4.3 معالجة الأخطاء

```python
        except requests.exceptions.Timeout:
            error_msg = "Error: Request timeout. Model may be overloaded or system resources are limited."
            console.print(f"[red]{error_msg}[/red]")
            
            if use_fallback:
                diagnostics = self._diagnose_ollama_issue()
                if diagnostics['issues']:
                    console.print("[red]Diagnostics:[/red]")
                    for issue in diagnostics['issues']:
                        console.print(f"  - {issue}")
                
                if use_fallback:
                    fallback_result = self._try_fallback_model(model, prompt, temperature)
                    if fallback_result:
                        return fallback_result
            
            return error_msg
```

**ما يحدث**:
- إذا فشل الموديل، يحاول Fallback model
- يعرض تشخيص للمشكلة (Diagnostics)

---

### المرحلة 5: تحليل الرد واستخراج Tool Calls

**الملف**: `src/agents/expert_agent.py` - دالة `run()` (بعد استدعاء الموديل)

#### 5.1 البحث عن Tool Calls

```python
        # Try to find tool calls in the response
        import re
        
        # === STEP 1: Try to parse JSON-style tool calls first ===
        json_tool_calls = []
        try:
            # Look for JSON objects with "tool" and "args" fields
            potential_jsons = []
            brace_count = 0
            start_idx = -1
            
            for i, char in enumerate(response):
                if char == '{':
                    if brace_count == 0:
                        start_idx = i
                    brace_count += 1
                elif char == '}':
                    brace_count -= 1
                    if brace_count == 0 and start_idx != -1:
                        json_str = response[start_idx:i+1]
                        potential_jsons.append(json_str)
                        start_idx = -1
            
            # Now try to parse each potential JSON
            for json_str in potential_jsons:
                try:
                    data = json.loads(json_str)
                    if isinstance(data, dict) and "tool" in data and "args" in data:
                        tool_name = data["tool"]
                        args_list = data["args"]
                        if not isinstance(args_list, list):
                            args_list = [args_list]
                        json_tool_calls.append((tool_name, args_list))
                        console.print(f"[cyan]📊 Status:[/cyan] [yellow]Found JSON tool call: {tool_name}[/yellow]")
                except (json.JSONDecodeError, KeyError):
                    continue
```

**ما يحدث**:
- يبحث عن JSON format في الرد:
  ```json
  {
    "tool": "write_file",
    "args": ["filepath", "content"]
  }
  ```
- يستخدم regex و JSON parsing لاستخراج Tool Calls

#### 5.2 التحقق من صحة الأداة

```python
        # === STEP 2: Execute JSON-style tool calls ===
        for tool_name, args_list in json_tool_calls:
            # Check if it's a valid tool
            if hasattr(self.tools, tool_name) or hasattr(self.expert_tools, tool_name) or hasattr(self.extended_tools, tool_name):
                console.print(f"[bold green]🔧 Executing Tool:[/bold green] {tool_name}")
```

**ما يحدث**:
- يتحقق إذا كانت الأداة موجودة في:
  - `self.tools` (الأدوات الأساسية)
  - `self.expert_tools` (الأدوات المتخصصة)
  - `self.extended_tools` (الأدوات الإضافية)

---

### المرحلة 6: تنفيذ الأدوات (Tool Execution)

**الملف**: `src/agents/expert_agent.py` - دالة `run()` (Tool Execution Section)

#### 6.1 تحويل الـ Args

```python
                # Convert args list to params dict based on tool signature
                params = {}
                try:
                    if tool_name == "write_file":
                        # args: [filepath, content]
                        if len(args_list) >= 2:
                            params["filepath"] = args_list[0]
                            params["content"] = args_list[1]
                        elif len(args_list) == 1:
                            params["filepath"] = args_list[0]
                            params["content"] = ""
                    
                    elif tool_name == "create_directory":
                        # args: [dirpath]
                        if args_list:
                            params["dirpath"] = args_list[0]
```

**مثال**:
```python
# من الموديل:
{"tool": "write_file", "args": ["math_calculator/calc.py", "def add()..."]}

# إلى:
params = {
    "filepath": "math_calculator/calc.py",
    "content": "def add()..."
}
```

**ما يحدث**:
- يحول args list إلى params dict بناءً على توقيع الأداة

#### 6.2 تنفيذ الأداة

```python
                    # Execute the tool
                    if hasattr(self.tools, tool_name):
                        tool_func = getattr(self.tools, tool_name)
                        result = tool_func(**params)
                    elif hasattr(self.expert_tools, tool_name):
                        tool_func = getattr(self.expert_tools, tool_name)
                        result = tool_func(**params)
                    elif hasattr(self.extended_tools, tool_name):
                        tool_func = getattr(self.extended_tools, tool_name)
                        result = tool_func(**params)
                    else:
                        result = f"Error: Tool {tool_name} not found"
                    
                    # Show what the tool is doing
                    if "learn" in tool_name.lower():
                        console.print(f"[dim]💡 Action: Learning and saving knowledge...[/dim]")
                    elif "search" in tool_name.lower():
                        console.print(f"[dim]🔍 Action: Searching for information...[/dim]")
                    elif "read" in tool_name.lower():
                        console.print(f"[dim]📖 Action: Reading from knowledge base...[/dim]")
                    elif "save" in tool_name.lower() or "update" in tool_name.lower():
                        console.print(f"[dim]💾 Action: Saving/updating knowledge...[/dim]")
                    
                    console.print(f"[green]✅ Tool Result:[/green] {result[:200]}...")
                    final_response += f"\n\nTool: {tool_name}\nResult: {result}"
                    tool_executed = True
                    tools_executed_count += 1
```

**ما يحدث**:
- يستدعي الأداة: `tool_instance.tool_name(**params)`
- يعرض رسالة تقدمية (Progress message)
- يجمع النتيجة

#### 6.3 معالجة الأخطاء

```python
                except Exception as e:
                    error_msg = f"Error executing {tool_name}: {str(e)}"
                    console.print(f"[red]{error_msg}[/red]")
                    final_response += f"\n\nError: {error_msg}"
                    continue
```

**ما يحدث**:
- إذا فشلت الأداة، يعرض رسالة خطأ
- يحاول الاستمرار مع أدوات أخرى

#### 6.4 عرض النتيجة

```python
        # Display final response
        if final_response:
            console.print(Panel(
                Markdown(final_response),
                title="✅ Expert Response",
                border_style="green"
            ))
        
        # Save to memory
        if tool_executed:
            self.memory.save_solution(user_input, final_response, rating=5)
```

**ما يحدث**:
- يعرض النتيجة في Panel
- يحفظ في الذاكرة (Memory) للاستخدام المستقبلي

---

### المرحلة 7: حلقة ReAct (Reasoning + Acting)

**الملف**: `src/agents/expert_agent.py` - دالة `run()` (ReAct Loop)

الحلقة تعمل كالتالي:

```
1. Think: الموديل يفكر في الحل
2. Act: يقرر استخدام أداة معينة
3. Observe: يرى نتيجة الأداة
4. Think Again: يفكر في الخطوة التالية
5. Repeat: حتى يكتمل الحل أو يصل لـ max_iterations
```

**مثال عملي**:

```
User: "Create math calculator using Python"

Iteration 1:
  Think: "I need to create a calculator. First, I should create a directory."
  Act: create_directory("math_calculator")
  Observe: Directory created successfully

Iteration 2:
  Think: "Now I need to create the calculator.py file with functions."
  Act: write_file("math_calculator/calculator.py", "def add()...")
  Observe: File created successfully

Iteration 3:
  Think: "I should also create a README file."
  Act: write_file("math_calculator/README.md", "...")
  Observe: File created successfully

Final: "Calculator project created successfully!"
```

**التنفيذ في الكود**:

```python
        # ReAct Loop (can be extended for multiple iterations)
        iteration = 0
        max_iterations = self.max_iterations
        
        while iteration < max_iterations:
            # Check if we have tool calls to execute
            if json_tool_calls:
                # Execute tools (already done above)
                break
            
            # If no tool calls, check if response is complete
            if "complete" in response.lower() or "done" in response.lower():
                break
            
            iteration += 1
```

---

## نظام الأدوات (Tools System)

### 1. الأدوات الأساسية (22 أداة)

**الملف**: `src/tools/tools.py`

**الفئات**:

- **ملفات**: read_file, write_file, list_directory, search_files, delete_file
- **أوامر**: run_command
- **ويب**: search_web, scrape_webpage, fetch_api
- **نظام**: get_system_info, monitor_resources, check_service
- **Docker**: docker_command
- **أمان**: scan_ports, check_ssl

### 2. الأدوات المتخصصة (45+ أداة)

**الملف**: `src/tools/expert_tools.py`

**الفئات**:

- **برمجة**: create_python_project, generate_code, analyze_code
- **مواقع**: create_html_template, generate_css, create_react_component
- **سيرفرات**: check_server_health, manage_nginx, setup_ssl
- **Docker**: create_dockerfile, docker_compose_generate, docker_build
- **PostgreSQL**: postgres_query, postgres_backup, postgres_create_table
- **n8n**: create_n8n_workflow, n8n_api_call, export_n8n_workflow
- **تعلم**: search_documentation, learn_new_technology, save_code_snippet

### 3. آلية تنفيذ الأداة

كل أداة هي دالة Python عادية:

```python
def write_file(self, filepath: str, content: str) -> str:
    """Write content to a file"""
    try:
        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding='utf-8')
        return f"File written successfully: {filepath}"
    except Exception as e:
        return f"Error: {str(e)}"
```

**كيف يتم استدعاؤها**:

```python
# من الموديل:
{"tool": "write_file", "args": ["test.py", "print('hello')"]}

# في الكود:
tool_func = getattr(self.tools, "write_file")
result = tool_func(filepath="test.py", content="print('hello')")
```

---

## نظام الذاكرة (Memory System)

**الملف**: `src/core/memory.py`

### 1. التخزين

```python
def save_solution(self, task: str, solution: str, rating: int = 5):
    """Save a solution to memory"""
    try:
        self.conn.execute(
            "INSERT INTO memory (task, solution, rating, timestamp) VALUES (?, ?, ?, ?)",
            (task, solution, rating, datetime.now().isoformat())
        )
        self.conn.commit()
    except Exception as e:
        print(f"Error saving to memory: {e}")
```

**ما يحدث**:
- يستخدم SQLite database (`data/agent_memory.db`)
- يحفظ:
  - المهمة (task)
  - الحل (solution)
  - التقييم (rating)
  - التاريخ (timestamp)

### 2. الاسترجاع

```python
def search_similar(self, query: str, limit: int = 5) -> List[Tuple[str, int]]:
    """Search for similar past solutions"""
    try:
        cursor = self.conn.execute(
            "SELECT solution, rating FROM memory WHERE task LIKE ? ORDER BY rating DESC, timestamp DESC LIMIT ?",
            (f"%{query}%", limit)
        )
        return [(row[0], row[1]) for row in cursor.fetchall()]
    except Exception as e:
        print(f"Error searching memory: {e}")
        return []
```

**ما يحدث**:
- عند طلب جديد، يبحث في الذاكرة عن حلول مشابهة
- يستخدم semantic search (البحث الدلالي)
- يعرض الحل السابق للمستخدم للاستخدام

---

## نظام التعلم التلقائي (Auto Learning)

**الملف**: `src/tools/auto_learner.py`

### 1. آلية التعلم

#### 1.1 قراءة قائمة الأدوات

```python
def load_tools_list(self) -> Dict[str, List[str]]:
    """Load the master list of tools to learn"""
    if not self.tools_file.exists():
        return {}
    
    try:
        content = self.tools_file.read_text(encoding='utf-8')
        content = content.lstrip('\ufeff').strip()
        return json.loads(content)
    except json.JSONDecodeError as e:
        return {}
```

**ما يحدث**:
- يقرأ `data/essential_tools.json`
- يحتوي على قائمة بجميع التقنيات المراد تعلمها

#### 1.2 التعلم لكل تقنية

```python
def learn_all(self):
    """Learn EVERYTHING in the list automatically"""
    categories = self.load_tools_list()
    learned = self.load_progress()
    
    for category, tools in categories.items():
        for tool in tools:
            if tool in learned:
                continue
            
            # 1. Fast Learn
            try:
                topics = ["overview", "key-features", "installation", "best-practices"]
                
                # Custom topics based on category
                if category == "data_analysis":
                    topics.extend(["data-structures", "visualization", "analysis-examples"])
                elif category == "databases":
                    topics.extend(["crud-operations", "connection-setup", "query-examples"])
                # ... more categories
                
                # Execute learning
                results = self.fast_learner.learn_fast(tool, topics)
                
                # 2. Save to Knowledge Base
                self.fast_learner.save_to_knowledge_base(results)
                
                # 3. Mark as done
                self.save_progress(tool)
                
            except Exception as e:
                print(f"❌ Failed to learn {tool}: {e}")
                continue
```

**ما يحدث**:
- يستخدم `FastLearning` لتعلم كل تقنية
- يبحث في الإنترنت عن معلومات
- يحفظ في `data/knowledge_base/`

#### 1.3 حفظ التقدم

```python
def save_progress(self, learned_tool: str):
    """Mark a tool as learned"""
    progress = self.load_progress()
    if learned_tool not in progress:
        progress.append(learned_tool)
        try:
            self.progress_file.write_text(
                json.dumps(progress, indent=2, ensure_ascii=False),
                encoding='utf-8'
            )
        except Exception as e:
            print(f"WARNING: Failed to save progress: {e}")
```

**ما يحدث**:
- يحفظ في `data/learning_progress.json`
- يتخطى التقنيات التي تم تعلمها مسبقاً

### 2. استخدام المعرفة

```python
def read_knowledge_base(self, technology: str) -> str:
    """Read knowledge from knowledge base"""
    kb_dir = get_knowledge_base_dir()
    tech_dir = kb_dir / technology.lower().replace(' ', '_')
    
    if not tech_dir.exists():
        return f"Knowledge base not found for {technology}"
    
    # Read all markdown files
    content = ""
    for md_file in tech_dir.glob("*.md"):
        content += md_file.read_text(encoding='utf-8') + "\n\n"
    
    return content if content else f"No knowledge found for {technology}"
```

**ما يحدث**:
- عند الحاجة، يقرأ من `knowledge_base/`
- يستخدم المعلومات المحفوظة بدلاً من البحث الأونلاين

---

## مثال كامل: إنشاء Math Calculator

عندما يطلب المستخدم: "Create math calculator using Python"

### الخطوات التفصيلية:

#### 1. Task Detection

```python
task_description = "Create math calculator using Python"
task_lower = task_description.lower()
# الكلمات: "create", "calculator", "python"
# النوع: 'coding' (لأن "python" في قائمة coding keywords)
```

#### 2. Model Selection

```python
scores = {
    "deepseek-r1:8b": 130,  # 100 (coding) + 30 (size > 4GB)
    "mistral:latest": 75,
    "qwen2.5:3b": 50
}
# المختار: "deepseek-r1:8b"
```

#### 3. Prompt Building

```python
prompt = """You are an Expert AI Agent with access to powerful tools.

Available Tools:
- create_directory(dirpath): Create a directory
- write_file(filepath, content): Write content to a file
- create_python_project(project_name, options): Create Python project
...

Task: Create math calculator using Python

Instructions:
1. Analyze the task
2. Plan your approach
3. Use appropriate tools
4. Provide final answer

Start by thinking about the task, then use tools as needed.
"""
```

#### 4. Model Call

```python
response = requests.post(
    "http://localhost:11434/api/generate",
    json={
        "model": "deepseek-r1:8b",
        "prompt": prompt,
        "stream": True
    }
)
# يستقبل رد متدفق
```

#### 5. Tool Calls Extraction

الموديل يرد بـ:

```json
{
  "tool": "create_directory",
  "args": ["math_calculator"]
}
```

ثم:

```json
{
  "tool": "write_file",
  "args": [
    "math_calculator/calculator.py",
    "def add(a, b):\n    return a + b\n\ndef subtract(a, b):\n    return a - b\n..."
  ]
}
```

#### 6. Tool Execution

```python
# تنفيذ create_directory
result1 = self.tools.create_directory("math_calculator")
# Output: "Directory created: math_calculator"

# تنفيذ write_file
result2 = self.tools.write_file(
    "math_calculator/calculator.py",
    "def add(a, b):\n    return a + b\n..."
)
# Output: "File written successfully: math_calculator/calculator.py"

# تنفيذ write_file للـ README
result3 = self.tools.write_file(
    "math_calculator/README.md",
    "# Math Calculator\n\nA simple calculator..."
)
# Output: "File written successfully: math_calculator/README.md"
```

#### 7. Response

```python
final_response = """
✅ Calculator project created successfully!

Created files:
- math_calculator/calculator.py (main calculator code)
- math_calculator/README.md (documentation)

To run:
cd math_calculator
python calculator.py
"""
```

---

## الملفات الرئيسية والمسؤوليات

| الملف | المسؤولية |
|-------|-----------|
| `src/agents/expert_agent.py` | الـ Agent الرئيسي، ReAct loop، اختيار الموديل |
| `src/tools/tools.py` | 22 أداة أساسية (ملفات، أوامر، ويب) |
| `src/tools/expert_tools.py` | 45+ أداة متخصصة (برمجة، Docker، PostgreSQL) |
| `src/core/memory.py` | نظام الذاكرة SQLite |
| `src/tools/auto_learner.py` | التعلم التلقائي للتقنيات |
| `src/tools/fast_learning.py` | البحث والتعلم من الإنترنت |
| `config.py` | إعدادات المشروع والمسارات |

---

## الخلاصة

النظام يعمل كالتالي:

1. **يستقبل الطلب** من المستخدم
2. **يكشف نوع المهمة** تلقائياً
3. **يختار أفضل موديل** بناءً على نوع المهمة
4. **يبني prompt** يحتوي على الأدوات والسياق
5. **يستدعي الموديل** عبر Ollama API
6. **يستخرج Tool Calls** من رد الموديل
7. **ينفذ الأدوات** بالترتيب
8. **يعرض النتيجة** ويحفظ في الذاكرة

النظام مصمم ليكون:

- **ذكي**: يختار الموديل المناسب تلقائياً
- **مرن**: 67+ أداة لمهام مختلفة
- **قابل للتعلم**: يحفظ الحلول ويستخدمها لاحقاً
- **محلي**: يعمل بدون API keys، كل شيء على السيرفر المحلي

---

## ملاحظات إضافية

### لماذا النظام بطيء أحياناً؟

1. **الموديلات الكبيرة**: الموديلات الكبيرة (مثل deepseek-r1:8b) تحتاج وقت أطول للتفكير
2. **Streaming**: النظام يستقبل الرد token بعد token، مما يزيد الوقت
3. **Tool Execution**: تنفيذ الأدوات قد يستغرق وقتاً (مثل البحث في الإنترنت)

### كيف تحسن الأداء؟

1. **استخدم موديلات أصغر**: للمهام البسيطة، استخدم qwen2.5:3b
2. **حدد نوع المهمة**: إذا حددت `task_type` يدوياً، يوفر وقت الكشف
3. **استخدم الذاكرة**: النظام يحفظ الحلول، استخدمها لتجنب إعادة الحساب

### نصائح للاستخدام

1. **كن محدداً**: كلما كان الطلب أوضح، كلما كان الحل أفضل
2. **استخدم الكلمات المفتاحية**: استخدم كلمات مثل "python", "docker", "database" لتوجيه النظام
3. **راجع النتائج**: دائماً راجع الملفات المنشأة قبل الاستخدام

---

**تم إنشاء هذا الدليل بواسطة**: AI Agent System Documentation  
**التاريخ**: 2025-01-27  
**الإصدار**: 1.0.0

