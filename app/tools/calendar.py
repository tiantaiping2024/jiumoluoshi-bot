"""
日历工具 - 支持公历和佛历
"""
from datetime import datetime, timedelta
from langchain_core.tools import tool


# 2026年佛教节日 (佛历2569-2570年)
BUDDHIST_HOLIDAYS_2026 = {
    "2026-01-01": {"name": "弥勒菩萨圣诞", "type": "节日"},
    "2026-02-17": {"name": "农历正月初一", "type": "春节"},
    "2026-02-26": {"name": "观世音菩萨圣诞", "type": "节日", "note": "农历二月十九"},
    "2026-04-03": {"name": "文殊菩萨圣诞", "type": "节日", "note": "农历三月四"},
    "2026-05-03": {"name": "佛祖释迦牟尼圣诞(浴佛节)", "type": "节日", "note": "农历四月初八"},
    "2026-06-21": {"name": "夏至", "type": "节气"},
    "2026-07-15": {"name": "盂兰盆节", "type": "节日", "note": "农历七月十五"},
    "2026-09-07": {"name": "观世音菩萨成道日", "type": "节日", "note": "农历六月十九"},
    "2026-09-23": {"name": "秋分", "type": "节气"},
    "2026-10-06": {"name": "观世音菩萨出家日", "type": "节日", "note": "农历九月十九"},
    "2026-12-21": {"name": "佛祖释迦牟尼成道日", "type": "节日", "note": "农历十一月初八"},
    "2026-12-22": {"name": "冬至", "type": "节气"},
}

# 2026年佛历2569年主要节日
BUDDHIST_YEAR_2569 = [
    ("2569-01-01", "公历2025年11月30日", "吠舍佉节(卫塞节)"),
    ("2569-04-15", "公历2026年5月3日", "佛诞节(浴佛节)"),
    ("2569-07-15", "公历2026年7月15日", "盂兰盆节"),
    ("2569-09-22", "公历2026年10月6日", "观世音菩萨出家日"),
]


@tool
def get_calendar(date: str = None, location: str = None) -> str:
    """
    查询日历信息，支持公历和佛历。
    
    参数:
        date: 可选，日期格式 YYYY-MM-DD，默认今天
        location: 可选，地点(用于节日安排)
    
    返回:
        日历信息，包括公历、农历、佛历
    """
    if date:
        try:
            dt = datetime.strptime(date, "%Y-%m-%d")
        except:
            return "日期格式错误，请使用 YYYY-MM-DD"
    else:
        dt = datetime.now()
    
    return _format_calendar(dt)


def _format_calendar(dt: datetime) -> str:
    """格式化日历信息"""
    # 公历
    weekdays = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
    weekday = weekdays[dt.weekday()]
    
    # 佛历
    buddhist_year = dt.year + 543
    
    # 农历 (简化计算)
    lunar_months = ["正月", "二月", "三月", "四月", "五月", "六月", 
                   "七月", "八月", "九月", "十月", "冬月", "腊月"]
    lunar_days = ["初一", "初二", "初三", "初四", "初五", "初六", "初七", "初八", 
                  "初九", "初十", "十一", "十二", "十三", "十四", "十五", 
                  "十六", "十七", "十八", "十九", "二十", "廿一", "廿二", 
                  "廿三", "廿四", "廿五", "廿六", "廿七", "廿八", "廿九", "三十"]
    
    # 简化：使用固定日期映射
    year_day = dt.timetuple().tm_yday
    lunar_month = (year_day % 30) + 1
    lunar_day = (year_day % 30) + 1
    
    lunar_info = f"农历{get_lunar_month(year_day)}{get_lunar_day(year_day)}"
    
    # 佛历节日
    date_key = dt.strftime("%Y-%m-%d")
    holiday_info = BUDDHIST_HOLIDAYS_2026.get(date_key, None)
    
    result = f"""
📅 **日历信息**

📆 公历: {dt.year}年{dt.month}月{dt.day}日 {weekday}
🪔 佛历: {buddhist_year}年
🌙 {lunar_info}
    """
    
    if holiday_info:
        result += f"\n🎊 今日: **{holiday_info['name']}**"
        if holiday_info.get('note'):
            result += f" ({holiday_info['note']})"
    
    return result.strip()


def get_lunar_month(day_of_year: int) -> str:
    """简化农历月计算"""
    lunar_months = ["正月", "二月", "三月", "四月", "五月", "六月", 
                   "七月", "八月", "九月", "十月", "冬月", "腊月"]
    month_idx = (day_of_year // 30) % 12
    return lunar_months[month_idx]


def get_lunar_day(day_of_year: int) -> str:
    """简化农历日计算"""
    lunar_days = ["初一", "初二", "初三", "初四", "初五", "初六", "初七", "初八", 
                  "初九", "初十", "十一", "十二", "十三", "十四", "十五", 
                  "十六", "十七", "十八", "十九", "二十", "廿一", "廿二", 
                  "廿三", "廿四", "廿五", "廿六", "廿七", "廿八", "廿九", "三十"]
    return lunar_days[(day_of_year - 1) % 30]


@tool
def list_buddhist_holidays(year: int = None) -> str:
    """
    列出2026年佛教重要节日。
    
    参数:
        year: 年份，默认2026
    """
    if year is None:
        year = 2026
    
    result = "🪔 **2026年佛教节日日历**\n\n"
    
    holidays = sorted(BUDDHIST_HOLIDAYS_2026.items(), key=lambda x: x[0])
    
    for date_str, info in holidays:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        result += f"• {dt.month}月{dt.day}日: {info['name']}\n"
    
    result += "\n*更多节日请查询佛历日历*"
    
    return result.strip()
