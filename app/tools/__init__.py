"""
鸠摩罗什Bot 工具模块
"""
# 延迟导入，避免启动失败
def get_search():
    from .search import search_web
    return search_web

try:
    from .search import search_web
except ImportError:
    search_web = None

from .weather import get_weather, get_buddhist_calendar
from .calendar import get_calendar, list_buddhist_holidays

# MCP 延迟导入
def get_mcp_loader():
    from .mcp import get_mcp_loader as _get_mcp_loader
    return _get_mcp_loader()

def load_mcp_tools():
    from .mcp import load_mcp_tools as _load_mcp_tools
    return _load_mcp_tools()

__all__ = [
    "search_web",
    "get_weather",
    "get_buddhist_calendar",
    "get_calendar",
    "list_buddhist_holidays",
    "get_mcp_loader",
    "load_mcp_tools",
]
