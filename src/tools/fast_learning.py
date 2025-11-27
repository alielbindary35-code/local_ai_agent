"""
Fast Learning Module - Accelerated Knowledge Acquisition
=========================================================

This module provides enhanced online learning capabilities by integrating
multiple knowledge sources:
- 🔍 Web search (DuckDuckGo)
- 📚 Official documentation
- 💻 GitHub repositories
- 📖 Wikipedia (optional)
- 💬 Stack Overflow (optional)

Usage:
    fast_learner = FastLearning()
    knowledge = fast_learner.learn_fast("Docker", ["containers", "images"])
"""

import requests
from typing import List, Dict, Any
from pathlib import Path
import json


class FastLearning:
    """Fast Learning with Multiple Online Sources"""
    
    def __init__(self):
        self.sources = {
            "search": True,      # DuckDuckGo search
            "docs": True,        # Official documentation
            "github": True,      # GitHub repositories
            "wikipedia": False,  # Wikipedia (optional)
            "stackoverflow": False  # Stack Overflow (optional)
        }
    
    def learn_fast(self, technology: str, topics: List[str] = None) -> Dict[str, Any]:
        """
        Fast learning from multiple online sources
        
        Args:
            technology: Technology to learn (e.g., "Docker")
            topics: Specific topics to focus on (e.g., ["containers", "images"])
        
        Returns:
            Dictionary with aggregated knowledge from all sources
        """
        if topics is None:
            topics = ["overview", "getting-started", "best-practices"]
        
        results = {
            "technology": technology,
            "topics": topics,
            "sources": {},
            "summary": ""
        }
        
        for topic in topics:
            print(f"🔍 Learning about {technology} - {topic}...")
            
            # 1. Search web for documentation
            if self.sources["search"]:
                search_results = self._search_web(technology, topic)
                if "search" not in results["sources"]:
                    results["sources"]["search"] = []
                results["sources"]["search"].extend(search_results)
            
            # 2. Find official documentation
            if self.sources["docs"]:
                doc_urls = self._get_official_docs(technology, topic)
                if "docs" not in results["sources"]:
                    results["sources"]["docs"] = []
                results["sources"]["docs"].extend(doc_urls)
            
            # 3. Search GitHub for examples
            if self.sources["github"]:
                github_repos = self._search_github(technology, topic)
                if "github" not in results["sources"]:
                    results["sources"]["github"] = []
                results["sources"]["github"].extend(github_repos)
        
        # Generate summary
        results["summary"] = self._generate_summary(results)
        
        return results
    
    def _search_web(self, technology: str, topic: str) -> List[Dict[str, str]]:
        """Search web using DuckDuckGo"""
        try:
            from src.tools.tools import Tools
            tools = Tools()
            
            query = f"{technology} {topic} tutorial documentation"
            search_results = tools.search_web(query, max_results=3)
            
            if isinstance(search_results, list):
                return search_results
            return []
        except Exception as e:
            print(f"⚠️ Web search failed: {e}")
            return []
    
    def _get_official_docs(self, technology: str, topic: str) -> List[Dict[str, str]]:
        """Get official documentation URLs"""
        doc_urls = {
            # Existing
            "docker": "https://docs.docker.com",
            "postgres": "https://www.postgresql.org/docs/",
            "postgresql": "https://www.postgresql.org/docs/",
            "n8n": "https://docs.n8n.io",
            "python": "https://docs.python.org/3/",
            "javascript": "https://developer.mozilla.org",
            "react": "https://react.dev",
            "vue": "https://vuejs.org/guide/",
            "nodejs": "https://nodejs.org/docs/",
            "express": "https://expressjs.com",
            "fastapi": "https://fastapi.tiangolo.com",
            "django": "https://docs.djangoproject.com",
            "flask": "https://flask.palletsprojects.com",
            # Cloud Platforms
            "aws": "https://docs.aws.amazon.com",
            "azure": "https://docs.microsoft.com/azure",
            "gcp": "https://cloud.google.com/docs",
            "vercel": "https://vercel.com/docs",
            "netlify": "https://docs.netlify.com",
            # Mobile
            "react native": "https://reactnative.dev/docs",
            "flutter": "https://docs.flutter.dev",
            "swift": "https://docs.swift.org",
            "kotlin": "https://kotlinlang.org/docs",
            # Testing
            "jest": "https://jestjs.io/docs",
            "pytest": "https://docs.pytest.org",
            "selenium": "https://www.selenium.dev/documentation",
            "cypress": "https://docs.cypress.io",
            "playwright": "https://playwright.dev/docs",
            # Security
            "owasp": "https://owasp.org",
            # API Tools
            "postman": "https://learning.postman.com/docs",
            "graphql": "https://graphql.org/learn",
            "swagger": "https://swagger.io/docs",
            # Version Control
            "git": "https://git-scm.com/doc",
            "github actions": "https://docs.github.com/actions",
            # Build Tools
            "webpack": "https://webpack.js.org",
            "vite": "https://vitejs.dev/guide",
            "rollup": "https://rollupjs.org/guide",
        }
        
        base_url = doc_urls.get(technology.lower())
        if base_url:
            return [{
                "title": f"{technology} Official Documentation - {topic}",
                "url": f"{base_url}/search?q={topic}",
                "type": "official_docs"
            }]
        return []
    
    def _search_github(self, technology: str, topic: str) -> List[Dict[str, str]]:
        """Search GitHub for repositories and examples"""
        try:
            # GitHub search API (no auth needed for basic search)
            query = f"{technology} {topic}"
            url = f"https://api.github.com/search/repositories?q={query}&sort=stars&order=desc&per_page=3"
            
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                repos = []
                for item in data.get("items", [])[:3]:
                    repos.append({
                        "title": item["name"],
                        "description": item.get("description", ""),
                        "url": item["html_url"],
                        "stars": item["stargazers_count"],
                        "type": "github_repo"
                    })
                return repos
            return []
        except Exception as e:
            print(f"⚠️ GitHub search failed: {e}")
            return []
    
    def _generate_summary(self, results: Dict[str, Any]) -> str:
        """Generate a summary of learned content"""
        technology = results["technology"]
        topics = results["topics"]
        sources = results["sources"]
        
        summary = f"# Fast Learning Summary: {technology}\n\n"
        summary += f"**Topics Covered**: {', '.join(topics)}\n\n"
        
        # Count sources
        total_sources = sum(len(items) for items in sources.values())
        summary += f"**Total Sources**: {total_sources}\n\n"
        
        # Add source breakdown
        for source_type, items in sources.items():
            if items:
                summary += f"### {source_type.upper()} ({len(items)} items)\n"
                for item in items[:3]:  # Show top 3
                    title = item.get("title", item.get("name", "Unknown"))
                    url = item.get("url", item.get("href", ""))
                    summary += f"- [{title}]({url})\n"
                summary += "\n"
        
        return summary
    
    def save_to_knowledge_base(self, results: Dict[str, Any], kb_path: str = None) -> str:
        """Save learned content to knowledge base"""
        try:
            from src.tools.expert_tools import ExpertTools
            expert_tools = ExpertTools()
            
            technology = results["technology"]
            summary = results["summary"]
            
            # First, create the knowledge base if it doesn't exist
            # expert_tools.learn_new_technology(technology, results["topics"])  # Removed to avoid recursion
            pass
            
            # Then update with the fast learning results
            filename = "fast_learning_results.md"
            expert_tools.update_knowledge_base(
                technology=technology,
                content=summary,
                filename=filename,
                append=False
            )
            
            return f"✅ Saved fast learning results to knowledge base: {technology}/{filename}"
        except Exception as e:
            return f"❌ Error saving to knowledge base: {e}"


def main():
    """Test the fast learning module"""
    print("🚀 Fast Learning Module - Test")
    print("=" * 60)
    
    fast_learner = FastLearning()
    
    # Test with Docker
    print("\n📚 Learning Docker (containers, images)...")
    results = fast_learner.learn_fast("Docker", ["containers", "images"])
    
    print("\n" + "=" * 60)
    print("📊 Results:")
    print(f"Technology: {results['technology']}")
    print(f"Topics: {results['topics']}")
    print(f"Sources found: {sum(len(items) for items in results['sources'].values())}")
    
    print("\n" + "=" * 60)
    print("📝 Summary:")
    print(results['summary'])
    
    # Save to knowledge base
    print("\n" + "=" * 60)
    save_result = fast_learner.save_to_knowledge_base(results)
    print(save_result)


if __name__ == "__main__":
    main()
