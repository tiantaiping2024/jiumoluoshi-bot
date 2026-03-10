"""
天气查询工具
"""
import os
import requests
from typing import Optional
from langchain_core.tools import tool


# OpenWeatherMap API (免费额度)
WEATHER_API_KEY = os.getenv("OPENWEATHERMAP_API_KEY", "")
WEATHER_API_BASE = "https://api.openweathermap.org/data/2.5/weather"


@tool
def get_weather(city: str = "北京", unit: str = "celsius") -> str:
    """
    查询指定城市的天气情况。
    
    参数:
        city: 城市名称，默认北京
        unit: 温度单位，celsius(摄氏度) 或 fahrenheit(华氏度)
    
    返回:
        天气信息描述
    """
    if not WEATHER_API_KEY:
        # 如果没有API Key，返回提示
        return "天气服务暂未配置。如需启用，请设置 OPENWEATHERMAP_API_KEY 环境变量。"
    
    try:
        params = {
            "q": city,
            "appid": WEATHER_API_KEY,
            "units": "metric" if unit == "celsius" else "imperial"
        }
        resp = requests.get(WEATHER_API_BASE, params=params, timeout=10)
        data = resp.json()
        
        if resp.status_code != 200:
            return f"查询失败: {data.get('message', '未知错误')}"
        
        weather = data.get("weather", [{}])[0]
        main = data.get("main", {})
        
        result = f"""
🌤️ **{city}天气预报**

天气状况: {weather.get('description', '未知')}
温度: {main.get('temp', '?')}°{'C' if unit == 'celsius' else 'F'}
体感温度: {main.get('feels_like', '?')}°{'C' if unit == 'celsius' else 'F'}
湿度: {main.get('humidity', '?')}%
风速: {data.get('wind', {}).get('speed', '?')} m/s

数据来源: OpenWeatherMap
"""
        return result.strip()
        
    except Exception as e:
        return f"查询天气出错: {str(e)}"


@tool
def get_buddhist_calendar(date: str = None) -> str:
    """
    查询佛历日期信息。
    
    参数:
        date: 可选，日期格式 YYYY-MM-DD，默认今天
    
    返回:
        佛历信息
    """
    from datetime import datetime, timedelta
    import random
    
    if date:
        try:
            dt = datetime.strptime(date, "%Y-%m-%d")
        except:
            return "日期格式错误，请使用 YYYY-MM-DD"
    else:
        dt = datetime.now()
    
    # 佛历计算 (佛历 = 公元 + 543)
    buddhist_year = dt.year + 543
    
    # 简单黄历吉日判断
    day = dt.day
    zodiac_animals = ["鼠", "牛", "虎", "兔", "龙", "蛇", "马", "羊", "猴", "鸡", "狗", "猪"]
    zodiac = zodiac_animals[dt.year % 12]
    
    # 佛教节日 (农历)
    buddhist_holidays = {
        "01-01": "弥勒菩萨圣诞",
        "02-19": "观世音菩萨圣诞",
        "04-04": "文殊菩萨圣诞",
        "04-08": "佛祖释迦牟尼圣诞(浴佛节)",
        "06-19": "观世音菩萨成道日",
        "07-13": "大势至菩萨圣诞",
        "07-15": "盂兰盆节",
        "09-19": "观世音菩萨出家日",
        "09-30": "药师佛圣诞",
        "12-08": "佛祖释迦牟尼成道日",
    }
    
    # 简化：检查公历日期对应的佛教节日
    holiday_today = buddhist_holidays.get(f"{dt.month:02d}-{dt.day:02d}", "")
    
    result = f"""
📅 **佛历信息**

公元: {dt.year}年{dt.month}月{dt.day}日
佛历: {buddhist_year}年
生肖: {zodiac}
星期: {['一', '二', '三', '四', '五', '六', '日'][dt.weekday()]}
    """
    
    if holiday_today:
        result += f"\n🎉 今日佛教节日: **{holiday_today}**"
    else:
        result += "\n今日非特定佛教节日"
    
    return result.strip()
