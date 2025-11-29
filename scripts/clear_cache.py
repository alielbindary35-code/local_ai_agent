"""
Script to clear old cache entries containing Chinese results
"""
import json
from pathlib import Path

def clear_chinese_cache():
    """Clear cache entries that contain Chinese results"""
    cache_dir = Path("data/knowledge_base")
    index_file = cache_dir / "cache_index.json"
    
    if not index_file.exists():
        print("No cache index found.")
        return
    
    # Load index
    with open(index_file, 'r', encoding='utf-8') as f:
        index = json.load(f)
    
    chinese_domains = ['baidu.com', 'zhidao.baidu', 'zhihu.com', 'sina.com', 'qq.com', '163.com', 'sohu.com']
    removed_count = 0
    
    # Check each cache entry
    keys_to_remove = []
    for key, entry in index.items():
        filepath = cache_dir / entry.get('file', '')
        if filepath.exists():
            try:
                content = filepath.read_text(encoding='utf-8')
                # Check if contains Chinese domains or high percentage of Chinese chars
                if any(domain in content.lower() for domain in chinese_domains):
                    chinese_chars = sum(1 for char in content if '\u4e00' <= char <= '\u9fff')
                    total_chars = len(content)
                    if total_chars > 0 and (chinese_chars / total_chars) > 0.2:
                        keys_to_remove.append(key)
                        filepath.unlink()  # Delete file
                        removed_count += 1
                        print(f"Removed: {key} ({entry.get('file')})")
            except Exception as e:
                print(f"Error processing {key}: {e}")
    
    # Update index
    for key in keys_to_remove:
        del index[key]
    
    # Save updated index
    with open(index_file, 'w', encoding='utf-8') as f:
        json.dump(index, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Removed {removed_count} cache entries with Chinese content.")

if __name__ == "__main__":
    print("🧹 Clearing cache entries with Chinese content...\n")
    clear_chinese_cache()

