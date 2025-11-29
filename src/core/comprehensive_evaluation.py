"""
Comprehensive Agent Evaluation System
Tests agent capabilities across all domains with detailed logging and evaluation
"""

import sys
import time
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn

# Add project root to path
def find_project_root():
    """Find the project root directory"""
    current = Path(__file__).resolve()
    while current != current.parent:
        if (current / "config.py").exists() and (current / "src").exists():
            return current
        current = current.parent
    return Path(__file__).parent.parent.parent

project_root = find_project_root()
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.agents.expert_agent import ExpertAgent
from src.core.knowledge_base import KnowledgeBase
from src.utils.connection_checker import ConnectionChecker

console = Console()

# Comprehensive Test Questions by Domain
EVALUATION_TESTS = {
    "System Detection": {
        "description": "Test if agent understands the operating system",
        "tests": [
            {
                "question": "What operating system am I using?",
                "expected_keywords": ["Windows", "Linux", "Mac", "macOS", "system"],
                "expected_tool": "get_system_info",
                "offline": True,
                "weight": 10
            },
            {
                "question": "What is my current CPU and RAM usage?",
                "expected_keywords": ["CPU", "RAM", "usage", "percent"],
                "expected_tool": "monitor_resources",
                "offline": True,
                "weight": 10
            },
            {
                "question": "What version of Windows/Linux am I running?",
                "expected_keywords": ["version", "Windows", "Linux", "release"],
                "expected_tool": "get_system_info",
                "offline": True,
                "weight": 10
            }
        ]
    },
    "Docker": {
        "description": "Test Docker knowledge and operations",
        "tests": [
            {
                "question": "What is Docker and how does containerization work?",
                "expected_keywords": ["Docker", "container", "containerization", "image"],
                "expected_tool": "read_knowledge_base",
                "offline": True,
                "weight": 10
            },
            {
                "question": "How do I create a Dockerfile for a Python application?",
                "expected_keywords": ["Dockerfile", "FROM", "python", "WORKDIR"],
                "expected_tool": "create_dockerfile",
                "offline": True,
                "weight": 15
            },
            {
                "question": "How to use Docker Compose for multi-container applications?",
                "expected_keywords": ["docker-compose", "services", "volumes", "networks"],
                "expected_tool": "read_knowledge_base",
                "offline": True,
                "weight": 10
            },
            {
                "question": "Check if Docker is installed and running on my system",
                "expected_keywords": ["Docker", "installed", "running", "version"],
                "expected_tool": "diagnose_system",
                "offline": True,
                "weight": 15
            }
        ]
    },
    "n8n": {
        "description": "Test n8n workflow automation knowledge",
        "tests": [
            {
                "question": "What is n8n and how does workflow automation work?",
                "expected_keywords": ["n8n", "workflow", "automation", "nodes"],
                "expected_tool": "read_knowledge_base",
                "offline": True,
                "weight": 10
            },
            {
                "question": "How to install and set up n8n?",
                "expected_keywords": ["install", "setup", "n8n", "docker", "npm"],
                "expected_tool": "read_knowledge_base",
                "offline": True,
                "weight": 10
            },
            {
                "question": "How to create workflows in n8n?",
                "expected_keywords": ["workflow", "create", "nodes", "connections"],
                "expected_tool": "read_knowledge_base",
                "offline": True,
                "weight": 10
            },
            {
                "question": "What are the best practices for n8n workflows?",
                "expected_keywords": ["best practices", "workflow", "optimization"],
                "expected_tool": "read_knowledge_base",
                "offline": True,
                "weight": 10
            }
        ]
    },
    "PostgreSQL": {
        "description": "Test PostgreSQL database knowledge",
        "tests": [
            {
                "question": "What is PostgreSQL and how does it work?",
                "expected_keywords": ["PostgreSQL", "database", "relational", "SQL"],
                "expected_tool": "read_knowledge_base",
                "offline": True,
                "weight": 10
            },
            {
                "question": "How to install PostgreSQL on Windows/Linux?",
                "expected_keywords": ["install", "PostgreSQL", "Windows", "Linux"],
                "expected_tool": "read_knowledge_base",
                "offline": True,
                "weight": 10
            },
            {
                "question": "How to create a database and tables in PostgreSQL?",
                "expected_keywords": ["CREATE DATABASE", "CREATE TABLE", "SQL"],
                "expected_tool": "read_knowledge_base",
                "offline": True,
                "weight": 10
            },
            {
                "question": "How to backup and restore PostgreSQL databases?",
                "expected_keywords": ["backup", "restore", "pg_dump", "psql"],
                "expected_tool": "read_knowledge_base",
                "offline": True,
                "weight": 10
            },
            {
                "question": "Check if PostgreSQL service is running on my system",
                "expected_keywords": ["PostgreSQL", "service", "running", "status"],
                "expected_tool": "diagnose_system",
                "offline": True,
                "weight": 15
            }
        ]
    },
    "Ollama": {
        "description": "Test Ollama AI model knowledge",
        "tests": [
            {
                "question": "What is Ollama and how does it work?",
                "expected_keywords": ["Ollama", "AI", "model", "LLM"],
                "expected_tool": "search_web",
                "offline": False,
                "weight": 10
            },
            {
                "question": "Check if Ollama service is currently running on my system",
                "expected_keywords": ["Ollama", "running", "service", "status"],
                "expected_tool": "check_service_status",
                "offline": True,
                "weight": 15
            },
            {
                "question": "How to install Ollama on Windows?",
                "expected_keywords": ["install", "Ollama", "Windows"],
                "expected_tool": "search_web",
                "offline": False,
                "weight": 10
            }
        ]
    },
    "Server Management": {
        "description": "Test server administration knowledge",
        "tests": [
            {
                "question": "How to manage Linux servers?",
                "expected_keywords": ["Linux", "server", "management", "SSH"],
                "expected_tool": "read_knowledge_base",
                "offline": True,
                "weight": 10
            },
            {
                "question": "How to configure web servers (Nginx, Apache)?",
                "expected_keywords": ["Nginx", "Apache", "web server", "configuration"],
                "expected_tool": "read_knowledge_base",
                "offline": True,
                "weight": 10
            },
            {
                "question": "How to monitor server performance?",
                "expected_keywords": ["monitor", "performance", "CPU", "RAM", "disk"],
                "expected_tool": "monitor_resources",
                "offline": True,
                "weight": 10
            }
        ]
    },
    "Offline Capability": {
        "description": "Test if agent can work without internet",
        "tests": [
            {
                "question": "What is Docker? (offline test)",
                "expected_keywords": ["Docker", "container"],
                "expected_tool": "read_knowledge_base",
                "offline": True,
                "weight": 20
            },
            {
                "question": "How to use PostgreSQL? (offline test)",
                "expected_keywords": ["PostgreSQL", "database"],
                "expected_tool": "read_knowledge_base",
                "offline": True,
                "weight": 20
            },
            {
                "question": "What is n8n? (offline test)",
                "expected_keywords": ["n8n", "workflow"],
                "expected_tool": "read_knowledge_base",
                "offline": True,
                "weight": 20
            }
        ]
    },
    "Loop Detection": {
        "description": "Test if agent repeats itself",
        "tests": [
            {
                "question": "What is the current CPU usage?",
                "expected_keywords": ["CPU", "usage"],
                "expected_tool": "monitor_resources",
                "offline": True,
                "weight": 15,
                "repeat_test": True  # Ask same question twice
            },
            {
                "question": "List files in current directory",
                "expected_keywords": ["files", "directory"],
                "expected_tool": "list_dir",
                "offline": True,
                "weight": 15,
                "repeat_test": True
            }
        ]
    }
}


class ComprehensiveEvaluator:
    """Comprehensive evaluation system for the AI agent"""
    
    def __init__(self, auto_approve: bool = True):
        self.auto_approve = auto_approve
        self.agent = ExpertAgent(auto_approve=auto_approve)
        self.connection_checker = ConnectionChecker()
        self.online = self.connection_checker.check_internet()
        
        # Create logs directory
        self.logs_dir = project_root / "data" / "evaluation_logs"
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        
        # Log file
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.log_file = self.logs_dir / f"comprehensive_evaluation_{timestamp}.txt"
        
        # Results storage
        self.results = {
            "started_at": datetime.now().isoformat(),
            "online": self.online,
            "system": self.agent.tools.get_os_identifier(),
            "tests": {},
            "summary": {}
        }
        
        # Track for loop detection
        self.question_responses = {}  # question -> [response1, response2, ...]
    
    def log(self, message: str, level: str = "INFO"):
        """Log message to file and console"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{level}] {message}\n"
        
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(log_entry)
        
        if level == "ERROR":
            console.print(f"[red]{message}[/red]")
        elif level == "WARNING":
            console.print(f"[yellow]{message}[/yellow]")
        else:
            console.print(f"[dim]{message}[/dim]")
    
    def evaluate_response(
        self,
        question: str,
        response: str,
        expected_keywords: List[str],
        expected_tool: str,
        offline_required: bool = False
    ) -> Dict[str, Any]:
        """
        Evaluate agent response quality
        
        Returns:
            Evaluation dict with scores and feedback
        """
        evaluation = {
            "question": question,
            "response_length": len(response),
            "has_expected_keywords": False,
            "keyword_matches": [],
            "has_error": False,
            "is_offline_capable": False,
            "tool_used": None,
            "correct_tool_used": False,
            "system_awareness": False,
            "score": 0,
            "feedback": []
        }
        
        # Check for errors
        if "Error:" in response or "error" in response.lower()[:100]:
            evaluation["has_error"] = True
            evaluation["feedback"].append("Response contains error")
            return evaluation
        
        # Check for expected keywords
        response_lower = response.lower()
        matches = []
        for keyword in expected_keywords:
            if keyword.lower() in response_lower:
                matches.append(keyword)
        
        evaluation["keyword_matches"] = matches
        evaluation["has_expected_keywords"] = len(matches) >= len(expected_keywords) * 0.5
        
        # Check system awareness (Windows/Linux/Mac)
        system_info = self.agent.tools.get_os_identifier()
        if "system" in question.lower() or "os" in question.lower() or "windows" in question.lower() or "linux" in question.lower():
            # Check if response mentions the actual system
            if "windows" in system_info.lower() and "windows" in response_lower:
                evaluation["system_awareness"] = True
            elif "linux" in system_info.lower() and "linux" in response_lower:
                evaluation["system_awareness"] = True
            elif "mac" in system_info.lower() and ("mac" in response_lower or "darwin" in response_lower):
                evaluation["system_awareness"] = True
            else:
                evaluation["feedback"].append("System awareness: Response doesn't match actual system")
        
        # Check offline capability
        if offline_required:
            # Check if response uses knowledge base (offline) vs web search (online)
            if "read_knowledge_base" in response or "knowledge base" in response_lower or "local knowledge" in response_lower:
                evaluation["is_offline_capable"] = True
            elif "search_web" in response or "searching" in response_lower or "duckduckgo" in response_lower:
                evaluation["is_offline_capable"] = False
                evaluation["feedback"].append("Used web search instead of offline knowledge")
            else:
                # Check if response has substantial content (likely from knowledge base)
                if len(response) > 200:
                    evaluation["is_offline_capable"] = True
                else:
                    evaluation["is_offline_capable"] = False
                    evaluation["feedback"].append("Response too short, may not have used offline knowledge")
        
        # Try to detect tool used from response patterns
        # This is a heuristic - actual tool usage is logged separately
        tools_mentioned = []
        if "get_system_info" in response or "system info" in response_lower:
            tools_mentioned.append("get_system_info")
        if "monitor_resources" in response or "cpu usage" in response_lower or "ram usage" in response_lower:
            tools_mentioned.append("monitor_resources")
        if "read_knowledge_base" in response or "knowledge base" in response_lower:
            tools_mentioned.append("read_knowledge_base")
        if "search_web" in response or "searching" in response_lower:
            tools_mentioned.append("search_web")
        if "diagnose_system" in response or "diagnostics" in response_lower:
            tools_mentioned.append("diagnose_system")
        if "check_service_status" in response or "service status" in response_lower:
            tools_mentioned.append("check_service_status")
        
        evaluation["tools_mentioned"] = tools_mentioned
        evaluation["correct_tool_used"] = expected_tool in tools_mentioned if tools_mentioned else False
        
        # Calculate score
        score = 0
        if not evaluation["has_error"]:
            score += 25
        if evaluation["has_expected_keywords"]:
            score += 30
        if evaluation["is_offline_capable"] or not offline_required:
            score += 20
        if evaluation["correct_tool_used"]:
            score += 15
        if evaluation["system_awareness"] or "system" not in question.lower():
            score += 10
        
        evaluation["score"] = min(score, 100)  # Cap at 100
        
        return evaluation
    
    def detect_loops(self, question: str, response: str) -> bool:
        """Detect if agent is repeating itself"""
        if question not in self.question_responses:
            self.question_responses[question] = []
        
        self.question_responses[question].append(response)
        
        # If same question asked multiple times
        if len(self.question_responses[question]) > 1:
            previous = self.question_responses[question][-2]
            current = response
            
            # Check for high similarity (simple check)
            if len(current) > 50 and len(previous) > 50:
                # Check if responses are very similar
                words_current = set(current.lower().split()[:20])
                words_previous = set(previous.lower().split()[:20])
                similarity = len(words_current & words_previous) / max(len(words_current), len(words_previous))
                
                if similarity > 0.8:  # 80% similarity
                    return True
        
        return False
    
    def run_evaluation(self, domains: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Run comprehensive evaluation
        
        Args:
            domains: List of domains to test (None = all)
        
        Returns:
            Evaluation results
        """
        console.print("\n" + "="*80)
        console.print(Panel(
            "[bold cyan]Comprehensive Agent Evaluation System[/bold cyan]\n\n"
            f"System: {self.agent.tools.get_os_identifier()}\n"
            f"Online: {'Yes' if self.online else 'No'}\n"
            f"Log File: {self.log_file}",
            title="🎯 Evaluation Started",
            border_style="cyan"
        ))
        console.print("="*80 + "\n")
        
        self.log(f"Starting comprehensive evaluation")
        self.log(f"System: {self.agent.tools.get_os_identifier()}")
        self.log(f"Online: {self.online}")
        
        domains_to_test = domains if domains else list(EVALUATION_TESTS.keys())
        
        total_tests = sum(len(EVALUATION_TESTS[domain]["tests"]) for domain in domains_to_test)
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeElapsedColumn(),
            console=console
        ) as progress:
            
            task = progress.add_task("[cyan]Running evaluation...", total=total_tests)
            
            for domain in domains_to_test:
                if domain not in EVALUATION_TESTS:
                    continue
                
                domain_info = EVALUATION_TESTS[domain]
                self.log(f"\n{'='*80}")
                self.log(f"Testing Domain: {domain}")
                self.log(f"Description: {domain_info['description']}")
                self.log(f"{'='*80}")
                
                domain_results = []
                
                for test_case in domain_info["tests"]:
                    question = test_case["question"]
                    expected_keywords = test_case["expected_keywords"]
                    expected_tool = test_case["expected_tool"]
                    offline_required = test_case.get("offline", False)
                    weight = test_case.get("weight", 10)
                    repeat_test = test_case.get("repeat_test", False)
                    
                    self.log(f"\nQuestion: {question}")
                    self.log(f"Expected Tool: {expected_tool}")
                    self.log(f"Offline Required: {offline_required}")
                    
                    # Run test
                    start_time = time.time()
                    try:
                        # Clear previous response for this question if repeating
                        if repeat_test and question in self.question_responses:
                            self.question_responses[question] = []
                        
                        response = self.agent.run(question, task_type=domain.lower())
                        elapsed = time.time() - start_time
                        
                        self.log(f"Response received ({elapsed:.2f}s)")
                        self.log(f"Response length: {len(response)} characters")
                        self.log(f"Response preview: {response[:200]}...")
                        
                        # Evaluate response
                        evaluation = self.evaluate_response(
                            question, response, expected_keywords,
                            expected_tool, offline_required
                        )
                        evaluation["elapsed_time"] = elapsed
                        evaluation["weight"] = weight
                        evaluation["response"] = response[:500]  # Store first 500 chars
                        
                        # Check for loops
                        is_loop = self.detect_loops(question, response)
                        evaluation["is_loop"] = is_loop
                        
                        if is_loop:
                            self.log("⚠️ LOOP DETECTED: Agent repeated same response", "WARNING")
                            evaluation["score"] = max(0, evaluation["score"] - 20)
                            evaluation["feedback"].append("Loop detected - agent repeated itself")
                        
                        # Check offline capability
                        if offline_required and not evaluation["is_offline_capable"]:
                            self.log("⚠️ OFFLINE TEST FAILED: Used online resources", "WARNING")
                            evaluation["feedback"].append("Failed offline requirement - used online resources")
                        
                        # Check tool usage
                        if not evaluation["correct_tool_used"] and expected_tool:
                            self.log(f"⚠️ Expected tool '{expected_tool}' not clearly used", "WARNING")
                            evaluation["feedback"].append(f"Expected tool '{expected_tool}' not detected")
                        
                        # Check system awareness
                        if "system" in question.lower() and not evaluation["system_awareness"]:
                            self.log("⚠️ System awareness: Response doesn't match actual system", "WARNING")
                        
                        domain_results.append(evaluation)
                        
                        # Log evaluation
                        self.log(f"Score: {evaluation['score']}/100")
                        self.log(f"Keywords matched: {len(evaluation['keyword_matches'])}/{len(expected_keywords)}")
                        self.log(f"Offline capable: {evaluation['is_offline_capable']}")
                        self.log(f"Correct tool used: {evaluation['correct_tool_used']}")
                        if evaluation.get("feedback"):
                            self.log(f"Feedback: {', '.join(evaluation['feedback'])}")
                        
                        # Repeat test if needed (for loop detection)
                        if repeat_test:
                            self.log("Repeating question for loop detection...")
                            time.sleep(2)  # Delay between repeats
                            response2 = self.agent.run(question, task_type=domain.lower())
                            is_loop2 = self.detect_loops(question, response2)
                            if is_loop2:
                                self.log("⚠️ LOOP CONFIRMED on repeat", "WARNING")
                                evaluation["loop_confirmed"] = True
                                evaluation["score"] = max(0, evaluation["score"] - 15)
                            
                            # Compare responses
                            if len(response) > 50 and len(response2) > 50:
                                words1 = set(response.lower().split()[:30])
                                words2 = set(response2.lower().split()[:30])
                                similarity = len(words1 & words2) / max(len(words1), len(words2))
                                evaluation["repeat_similarity"] = similarity
                                if similarity > 0.85:
                                    self.log(f"⚠️ High similarity on repeat: {similarity:.2%}", "WARNING")
                    
                    except Exception as e:
                        self.log(f"ERROR: {str(e)}", "ERROR")
                        evaluation = {
                            "question": question,
                            "has_error": True,
                            "error": str(e),
                            "score": 0,
                            "elapsed_time": time.time() - start_time
                        }
                        domain_results.append(evaluation)
                    
                    progress.update(task, advance=1)
                    time.sleep(0.5)  # Small delay between tests
                
                # Calculate domain score
                if domain_results:
                    total_score = sum(r.get("score", 0) * r.get("weight", 1) for r in domain_results)
                    total_weight = sum(r.get("weight", 1) for r in domain_results)
                    domain_score = (total_score / total_weight) if total_weight > 0 else 0
                    
                    self.results["tests"][domain] = {
                        "score": domain_score,
                        "tests_count": len(domain_results),
                        "passed": sum(1 for r in domain_results if r.get("score", 0) >= 60),
                        "failed": sum(1 for r in domain_results if r.get("score", 0) < 60),
                        "details": domain_results
                    }
                    
                    self.log(f"\nDomain '{domain}' Score: {domain_score:.1f}/100")
        
        # Calculate overall summary
        self._calculate_summary()
        
        # Save results
        self._save_results()
        
        # Display summary
        self._display_summary()
        
        return self.results
    
    def _calculate_summary(self):
        """Calculate overall evaluation summary"""
        total_score = 0
        total_weight = 0
        total_tests = 0
        total_passed = 0
        total_failed = 0
        loop_count = 0
        offline_failures = 0
        
        for domain, domain_data in self.results["tests"].items():
            domain_score = domain_data["score"]
            tests_count = domain_data["tests_count"]
            passed = domain_data["passed"]
            failed = domain_data["failed"]
            
            total_score += domain_score * tests_count
            total_weight += tests_count
            total_tests += tests_count
            total_passed += passed
            total_failed += failed
            
            # Count loops and offline failures
            for detail in domain_data.get("details", []):
                if detail.get("is_loop"):
                    loop_count += 1
                if detail.get("offline_required") and not detail.get("is_offline_capable"):
                    offline_failures += 1
        
        overall_score = (total_score / total_weight) if total_weight > 0 else 0
        
        self.results["summary"] = {
            "overall_score": overall_score,
            "total_tests": total_tests,
            "passed": total_passed,
            "failed": total_failed,
            "pass_rate": (total_passed / total_tests * 100) if total_tests > 0 else 0,
            "loop_detections": loop_count,
            "offline_failures": offline_failures,
            "completed_at": datetime.now().isoformat()
        }
    
    def _save_results(self):
        """Save evaluation results to JSON"""
        results_file = self.log_file.with_suffix(".json")
        with open(results_file, "w", encoding="utf-8") as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        
        self.log(f"Results saved to: {results_file}")
    
    def _display_summary(self):
        """Display evaluation summary table"""
        console.print("\n" + "="*80)
        console.print(Panel(
            "[bold green]Evaluation Complete![/bold green]",
            title="✅ Summary",
            border_style="green"
        ))
        
        summary = self.results["summary"]
        
        # Overall score table
        table = Table(title="Overall Results", show_header=True, header_style="bold cyan")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")
        
        table.add_row("Overall Score", f"{summary['overall_score']:.1f}/100")
        table.add_row("Total Tests", str(summary['total_tests']))
        table.add_row("Passed", f"{summary['passed']} ({summary['pass_rate']:.1f}%)")
        table.add_row("Failed", str(summary['failed']))
        table.add_row("Loop Detections", str(summary['loop_detections']))
        table.add_row("Offline Failures", str(summary['offline_failures']))
        
        console.print(table)
        
        # Domain scores table
        domain_table = Table(title="Domain Scores", show_header=True, header_style="bold cyan")
        domain_table.add_column("Domain", style="cyan")
        domain_table.add_column("Score", style="green")
        domain_table.add_column("Tests", style="yellow")
        domain_table.add_column("Passed", style="green")
        domain_table.add_column("Failed", style="red")
        domain_table.add_column("Loops", style="yellow")
        domain_table.add_column("Offline OK", style="green")
        
        for domain, data in self.results["tests"].items():
            score = data["score"]
            score_color = "green" if score >= 70 else "yellow" if score >= 50 else "red"
            
            # Count loops and offline status
            loops = sum(1 for d in data.get("details", []) if d.get("is_loop"))
            offline_ok = sum(1 for d in data.get("details", []) 
                           if d.get("offline_required", False) and d.get("is_offline_capable", False))
            offline_total = sum(1 for d in data.get("details", []) if d.get("offline_required", False))
            offline_status = f"{offline_ok}/{offline_total}" if offline_total > 0 else "N/A"
            
            domain_table.add_row(
                domain,
                f"[{score_color}]{score:.1f}/100[/{score_color}]",
                str(data["tests_count"]),
                str(data["passed"]),
                str(data["failed"]),
                str(loops),
                offline_status
            )
        
        console.print("\n")
        console.print(domain_table)
        
        # Detailed analysis
        console.print("\n" + "="*80)
        console.print(Panel(
            self._generate_detailed_analysis(),
            title="📊 Detailed Analysis",
            border_style="cyan"
        ))
        
        # Recommendations
        console.print("\n" + "="*80)
        console.print(Panel(
            self._generate_recommendations(),
            title="💡 Recommendations",
            border_style="yellow"
        ))
        
        console.print(f"\n[dim]Full log: {self.log_file}[/dim]")
        console.print(f"[dim]Results JSON: {self.log_file.with_suffix('.json')}[/dim]\n")
    
    def _generate_detailed_analysis(self) -> str:
        """Generate detailed analysis of evaluation results"""
        analysis = []
        summary = self.results["summary"]
        
        # System awareness
        system_tests = self.results["tests"].get("System Detection", {})
        if system_tests:
            system_score = system_tests.get("score", 0)
            if system_score >= 80:
                analysis.append("✅ System Detection: Excellent - Agent understands the OS")
            elif system_score >= 60:
                analysis.append("⚠️ System Detection: Good but could be better")
            else:
                analysis.append("❌ System Detection: Poor - Agent doesn't understand the OS")
        
        # Offline capability
        offline_tests = self.results["tests"].get("Offline Capability", {})
        if offline_tests:
            offline_details = offline_tests.get("details", [])
            offline_passed = sum(1 for d in offline_details if d.get("is_offline_capable", False))
            offline_total = len(offline_details)
            if offline_passed == offline_total:
                analysis.append(f"✅ Offline Capability: Perfect ({offline_passed}/{offline_total})")
            elif offline_passed >= offline_total * 0.7:
                analysis.append(f"⚠️ Offline Capability: Good ({offline_passed}/{offline_total})")
            else:
                analysis.append(f"❌ Offline Capability: Poor ({offline_passed}/{offline_total}) - Needs more offline knowledge")
        
        # Loop detection
        if summary["loop_detections"] == 0:
            analysis.append("✅ Loop Detection: No loops detected - Agent doesn't repeat itself")
        else:
            analysis.append(f"❌ Loop Detection: {summary['loop_detections']} loop(s) detected - Agent repeats itself")
        
        # Domain-specific analysis
        critical_domains = ["Docker", "n8n", "PostgreSQL", "Ollama"]
        for domain in critical_domains:
            if domain in self.results["tests"]:
                domain_data = self.results["tests"][domain]
                score = domain_data["score"]
                if score >= 80:
                    analysis.append(f"✅ {domain}: Excellent ({score:.1f}/100)")
                elif score >= 60:
                    analysis.append(f"⚠️ {domain}: Acceptable ({score:.1f}/100)")
                else:
                    analysis.append(f"❌ {domain}: Needs improvement ({score:.1f}/100)")
        
        return "\n".join(analysis)
    
    def _generate_recommendations(self) -> str:
        """Generate recommendations based on evaluation results"""
        recommendations = []
        summary = self.results["summary"]
        
        if summary["overall_score"] < 50:
            recommendations.append("⚠️ Overall score is low. Agent needs significant improvement.")
        elif summary["overall_score"] < 70:
            recommendations.append("⚠️ Overall score is acceptable but could be better.")
        else:
            recommendations.append("✅ Overall score is good!")
        
        if summary["loop_detections"] > 0:
            recommendations.append(f"⚠️ Found {summary['loop_detections']} loop(s). Agent repeats itself - needs loop detection improvement.")
        
        if summary["offline_failures"] > 0:
            recommendations.append(f"⚠️ {summary['offline_failures']} offline test(s) failed. Agent needs more offline knowledge.")
        
        # Domain-specific recommendations
        for domain, data in self.results["tests"].items():
            if data["score"] < 60:
                recommendations.append(f"⚠️ {domain} domain needs improvement (score: {data['score']:.1f}/100)")
        
        # System awareness
        system_tests = self.results["tests"].get("System Detection", {})
        if system_tests and system_tests.get("score", 0) < 70:
            recommendations.append("⚠️ System Detection needs improvement - Agent should better understand Windows/Linux/Mac")
        
        if not any("⚠️" in r or "❌" in r for r in recommendations):
            recommendations.append("✅ Agent performance is good across all domains!")
        
        return "\n".join(recommendations)


def main():
    """Main entry point"""
    try:
        evaluator = ComprehensiveEvaluator(auto_approve=True)
        
        console.print("\n[bold]Available Test Domains:[/bold]")
        for i, domain in enumerate(EVALUATION_TESTS.keys(), 1):
            console.print(f"  {i}. {domain} - {EVALUATION_TESTS[domain]['description']}")
        
        console.print("\n[cyan]Starting comprehensive evaluation of all domains...[/cyan]\n")
        
        # Run evaluation for all domains
        results = evaluator.run_evaluation()
        
        console.print("\n[bold green]✅ Evaluation completed![/bold green]")
        
    except KeyboardInterrupt:
        console.print("\n[yellow]Evaluation interrupted by user.[/yellow]")
    except Exception as e:
        console.print(f"\n[red]Evaluation failed: {e}[/red]")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

