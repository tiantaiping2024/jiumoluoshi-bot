"""
鸠摩罗什Bot 工具模块
"""
from .search import search_web
from .weather import get_weather, get_buddhist_calendar
from .calendar import get_calendar, list_buddhist_holidays
from .mcp import get_mcp_loader, load_mcp_tools

__all__ = [
    "search_web",
    "get_weather",
    "get_buddhist_calendar",
    "get_calendar",
    "list_buddhist_holidays",
    "get_mcp_loader",
    "load_mcp_tools",
]
