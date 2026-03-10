"""
MCP 搜索工具 - 使用 Exa MCP
"""
import os
import subprocess
import json
from langchain_core.tools import tool


# 设置工作目录
WORK_DIR = os.path.expanduser("~/.openclaw/workspace")


@tool
def search_web(query: str) -> str:
    """
    搜索互联网获取最新信息。
    
    当用户询问以下问题时使用此工具:
    - 佛教节日、佛历相关问题
    - 佛教资讯、佛事活动
    - 天气查询
    - 新闻资讯
    - 其他需要最新信息的问题
    
    参数:
        query: 搜索关键词
    """
    if not query or len(query.strip()) < 2:
        return "搜索关键词太短"
    
    try:
        # 调用 MCP Exa 搜索
        result = _mcporter_search(query)
        if result:
            return result
    except Exception as e:
        print(f"MCP search error: {e}")
    
    # 备用：返回本地知识库
    return _local_knowledge(query)


def _mcporter_search(query: str, num_results: int = 5) -> str:
    """通过 mcporter 调用 Exa MCP 搜索"""
    try:
        cmd = [
            "mcporter", "call", 
            f"exa.web_search_exa(query: \"{query}\", numResults: {num_results})"
        ]
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30,
            cwd=WORK_DIR  # 设置正确的工作目录
        )
        
        if result.returncode != 0:
            print(f"mcporter error: {result.stderr}")
            return None
        
        output = result.stdout.strip()
        
        if not output:
            return None
        
        # 解析 JSON 输出
        try:
            data = json.loads(output)
            results = data.get("results", [])
            
            if not results:
                return None
            
            # 格式化输出
            formatted = f"🔍 搜索结果: 「{query}」\n\n"
            
            for i, r in enumerate(results[:5], 1):
                title = r.get("title", "无标题")
                url = r.get("url", "")
                text = r.get("text", "")[:200]
                
                formatted += f"**{i}. {title}**\n"
                if text:
                    formatted += f"   {text}...\n"
                if url:
                    formatted += f"   🔗 {url}\n\n"
            
            return formatted.strip()
            
        except json.JSONDecodeError:
            # 输出不是 JSON，直接返回
            if output:
                return output[:2000]
        
    except subprocess.TimeoutExpired:
        return "搜索超时，请稍后重试"
    except Exception as e:
        print(f"mcporter exception: {e}")
    
    return None


def _local_knowledge(query: str) -> str:
    """本地知识库备用"""
    local_kb = {
        "佛教节日": """
2026年佛教重要节日:
• 1月1日 - 弥勒菩萨圣诞
• 2月17日 - 农历新年
• 2月26日 - 观世音菩萨圣诞(农历二月十九)
• 4月3日 - 文殊菩萨圣诞(农历三月四)
• 5月3日 - 佛祖释迦牟尼圣诞/浴佛节(农历四月初八)
• 7月15日 - 盂兰盆节
• 9月7日 - 观世音菩萨成道日(农历六月十九)
• 10月6日 - 观世音菩萨出家日(农历九月十九)
• 12月8日 - 佛祖释迦牟尼成道日(农历十一月初八)
""",
    }
    
    query_lower = query.lower()
    for key, content in local_kb.items():
        if any(kw in query_lower for kw in ["节日", "佛历", "佛诞", "浴佛", "盂兰"]):
            return f"📚 本地知识库: \n\n{content}"
    
    return "抱歉，暂时无法完成搜索。"


# 测试
if __name__ == "__main__":
    print(search_web.invoke("2026年佛教节日有哪些"))
