"""
天气查询工具
"""
import os
import requests
from typing import Optional


# OpenWeatherMap API (免费额度)
WEATHER_API_KEY = os.getenv("OPENWEATHERMAP_API_KEY", "")
WEATHER_API_BASE = "https://api.openweathermap.org/data/2.5/weather"


def get_weather(city: str = "北京", unit: str = "celsius") -> str:
    """
    查询指定城市的天气情况。
    """
    if not WEATHER_API_KEY:
        return "天气查询功能未配置 API Key"
    
    try:
        params = {
            "q": city,
            "appid": WEATHER_API_KEY,
            "units": "metric" if unit == "celsius" else "imperial"
        }
        resp = requests.get(WEATHER_API_BASE, params=params, timeout=10)
        data = resp.json()
        
        if data.get("cod") == 200:
            weather = data["weather"][0]["description"]
            temp = data["main"]["temp"]
            humidity = data["main"]["humidity"]
            return f"{city}天气：{weather}，温度：{temp}°C，湿度：{humidity}%"
        else:
            return f"查询失败：{data.get('message', '未知错误')}"
    except Exception as e:
        return f"查询出错：{str(e)}"


def get_buddhist_calendar() -> str:
    """获取佛历日期"""
    import datetime
    now = datetime.datetime.now()
    # 简单佛历计算（仅供参考）
    buddhist_year = now.year + 543
    return f"佛历{buddhist_year}年 {now.strftime('%Y年%m月%d日')}"
