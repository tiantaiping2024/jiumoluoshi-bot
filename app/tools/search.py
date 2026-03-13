"""
搜索工具
"""
import os
import requests


TAVILY_API_KEY = os.getenv("TAVILY_API_KEY", "")


def search_web(query: str) -> str:
    """搜索互联网获取最新信息"""
    if not TAVILY_API_KEY:
        return "搜索功能未配置 API Key"
    
    try:
        resp = requests.post(
            "https://api.tavily.com/search",
            json={"api_key": TAVILY_API_KEY, "query": query, "max_results": 3},
            timeout=10
        )
        data = resp.json()
        
        results = data.get("results", [])
        if not results:
            return "未找到相关信息"
        
        answer = f"搜索结果：\n\n"
        for r in results:
            answer += f"• {r.get('title', '')}\n"
            answer += f"  {r.get('content', '')[:200]}...\n\n"
        
        return answer
    except Exception as e:
        return f"搜索出错：{str(e)}"
