"""
Cache Manager Utility
Manages caching of online search results for offline use
"""

import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
from rich.console import Console

console = Console()


class CacheManager:
    """
    Manages knowledge base cache for hybrid online/offline mode
    """
    
    def __init__(self, cache_dir: str = "data/knowledge_base"):
        """
        Initialize cache manager
        
        Args:
            cache_dir: Directory to store cached knowledge
        """
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        self.index_file = self.cache_dir / "cache_index.json"
        self.index = self._load_index()
        
        # In-memory cache for API responses (key -> {value, expires_at})
        self.memory_cache: Dict[str, Dict[str, Any]] = {}
    
    def _load_index(self) -> Dict[str, Any]:
        """Load cache index from disk"""
        if self.index_file.exists():
            try:
                with open(self.index_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def _save_index(self):
        """Save cache index to disk"""
        try:
            with open(self.index_file, 'w', encoding='utf-8') as f:
                json.dump(self.index, f, indent=2, ensure_ascii=False)
        except Exception as e:
            console.print(f"[yellow]⚠️ Warning: Could not save cache index: {e}[/yellow]")
    
    def save(self, technology: str, topic: str, content: str, source: str = "web_search") -> bool:
        """
        Save content to cache
        
        Args:
            technology: Technology name (e.g., "python", "docker")
            topic: Topic name (e.g., "calculator", "basics")
            content: Content to cache
            source: Source of the content
            
        Returns:
            True if saved successfully
        """
        try:
            # Create technology directory
            tech_dir = self.cache_dir / technology.lower()
            tech_dir.mkdir(exist_ok=True)
            
            # Save content
            filename = f"{topic.lower().replace(' ', '_')}.md"
            filepath = tech_dir / filename
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # Update index
            key = f"{technology}_{topic}".lower()
            self.index[key] = {
                "file": str(filepath.relative_to(self.cache_dir)),
                "last_updated": datetime.now().isoformat(),
                "source": source,
                "technology": technology,
                "topic": topic
            }
            self._save_index()
            
            console.print(f"[green]💾 Cached: {technology}/{topic}[/green]")
            return True
            
        except Exception as e:
            console.print(f"[red]❌ Cache save failed: {e}[/red]")
            return False
    
    def load(self, technology: str, topic: Optional[str] = None) -> Optional[str]:
        """
        Load content from cache
        
        Args:
            technology: Technology name
            topic: Optional topic name. If None, loads all for technology
            
        Returns:
            Cached content or None if not found
        """
        try:
            if topic:
                # Load specific topic
                key = f"{technology}_{topic}".lower()
                if key in self.index:
                    filepath = self.cache_dir / self.index[key]["file"]
                    if filepath.exists():
                        with open(filepath, 'r', encoding='utf-8') as f:
                            content = f.read()
                        console.print(f"[green]📂 Loaded from cache: {technology}/{topic}[/green]")
                        return content
            else:
                # Load all topics for technology
                tech_dir = self.cache_dir / technology.lower()
                if tech_dir.exists():
                    all_content = []
                    for file in tech_dir.glob("*.md"):
                        with open(file, 'r', encoding='utf-8') as f:
                            all_content.append(f.read())
                    if all_content:
                        console.print(f"[green]📂 Loaded {len(all_content)} files from cache: {technology}[/green]")
                        return "\n\n---\n\n".join(all_content)
            
            return None
            
        except Exception as e:
            console.print(f"[yellow]⚠️ Cache load failed: {e}[/yellow]")
            return None
    
    def exists(self, technology: str, topic: Optional[str] = None) -> bool:
        """
        Check if content exists in cache
        
        Args:
            technology: Technology name
            topic: Optional topic name
            
        Returns:
            True if exists in cache
        """
        if topic:
            key = f"{technology}_{topic}".lower()
            return key in self.index
        else:
            tech_dir = self.cache_dir / technology.lower()
            return tech_dir.exists() and any(tech_dir.glob("*.md"))
    
    def list_cached(self, technology: Optional[str] = None) -> List[Dict[str, str]]:
        """
        List all cached items
        
        Args:
            technology: Optional technology filter
            
        Returns:
            List of cached items
        """
        if technology:
            return [
                item for key, item in self.index.items()
                if item["technology"].lower() == technology.lower()
            ]
        else:
            return list(self.index.values())
    
    def clear(self, technology: Optional[str] = None):
        """
        Clear cache
        
        Args:
            technology: Optional technology to clear. If None, clears all
        """
        if technology:
            tech_dir = self.cache_dir / technology.lower()
            if tech_dir.exists():
                import shutil
                shutil.rmtree(tech_dir)
                # Remove from index
                self.index = {
                    k: v for k, v in self.index.items()
                    if v["technology"].lower() != technology.lower()
                }
                self._save_index()
                console.print(f"[yellow]🗑️ Cleared cache for: {technology}[/yellow]")
        else:
            import shutil
            if self.cache_dir.exists():
                shutil.rmtree(self.cache_dir)
                self.cache_dir.mkdir(parents=True, exist_ok=True)
            self.index = {}
            self._save_index()
            console.print("[yellow]🗑️ Cleared all cache[/yellow]")
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get cache statistics
        
        Returns:
            Dictionary with cache stats
        """
        technologies = set(item["technology"] for item in self.index.values())
        total_size = sum(
            (self.cache_dir / item["file"]).stat().st_size
            for item in self.index.values()
            if (self.cache_dir / item["file"]).exists()
        )
        
        return {
            "total_items": len(self.index),
            "technologies": len(technologies),
            "total_size_bytes": total_size,
            "total_size_mb": round(total_size / (1024 * 1024), 2)
        }
    
    def get(self, key: str) -> Optional[Any]:
        """
        Get value from in-memory cache (for API responses).
        
        Args:
            key: Cache key
        
        Returns:
            Cached value or None if not found or expired
        """
        if key in self.memory_cache:
            entry = self.memory_cache[key]
            if datetime.now() < entry['expires_at']:
                return entry['value']
            else:
                # Expired, remove it
                del self.memory_cache[key]
        return None
    
    def set(self, key: str, value: Any, ttl: int = 3600):
        """
        Set value in in-memory cache with TTL.
        
        Args:
            key: Cache key
            value: Value to cache
            ttl: Time-to-live in seconds (default: 1 hour)
        """
        expires_at = datetime.now() + timedelta(seconds=ttl)
        self.memory_cache[key] = {
            'value': value,
            'expires_at': expires_at
        }
        
        # Clean up expired entries periodically (simple cleanup)
        if len(self.memory_cache) > 1000:
            self._cleanup_expired()
    
    def _cleanup_expired(self):
        """Remove expired entries from memory cache."""
        now = datetime.now()
        expired_keys = [
            key for key, entry in self.memory_cache.items()
            if now >= entry['expires_at']
        ]
        for key in expired_keys:
            del self.memory_cache[key]
