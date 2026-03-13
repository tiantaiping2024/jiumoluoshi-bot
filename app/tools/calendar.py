"""
日历工具 - 支持公历和佛历
"""
from datetime import datetime


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


def get_calendar(date: str = None, location: str = None) -> str:
    """查询日历信息"""
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
    weekdays = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
    weekday = weekdays[dt.weekday()]
    buddhist_year = dt.year + 543
    
    # 简化农历
    lunar_months = ["正月", "二月", "三月", "四月", "五月", "六月", 
                   "七月", "八月", "九月", "十月", "冬月", "腊月"]
    year_day = dt.timetuple().tm_yday
    lunar_month = lunar_months[(year_day // 30) % 12]
    
    date_key = dt.strftime("%Y-%m-%d")
    holiday_info = BUDDHIST_HOLIDAYS_2026.get(date_key, None)
    
    result = f"""
📅 日历信息

📆 公历: {dt.year}年{dt.month}月{dt.day}日 {weekday}
🪔 佛历: {buddhist_year}年
🌙 农历{get_lunar_day(year_day)}
    """
    
    if holiday_info:
        result += f"\n🎊 今日: **{holiday_info['name']}**"
        if holiday_info.get('note'):
            result += f" ({holiday_info['note']})"
    
    return result.strip()


def get_lunar_day(day_of_year: int) -> str:
    """简化农历日计算"""
    lunar_days = ["初一", "初二", "初三", "初四", "初五", "初六", "初七", "初八", 
                  "初九", "初十", "十一", "十二", "十三", "十四", "十五", 
                  "十六", "十七", "十八", "十九", "二十", "廿一", "廿二", 
                  "廿三", "廿四", "廿五", "廿六", "廿七", "廿八", "廿九", "三十"]
    return lunar_days[(day_of_year - 1) % 30]


def list_buddhist_holidays(year: int = None) -> str:
    """列出佛教重要节日"""
    if year is None:
        year = 2026
    
    result = "🪔 2026年佛教节日日历\n\n"
    
    holidays = sorted(BUDDHIST_HOLIDAYS_2026.items(), key=lambda x: x[0])
    
    for date_str, info in holidays:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        result += f"• {dt.month}月{dt.day}日: {info['name']}\n"
    
    return result.strip()
