# utils/helpers.py
"""
Helper utility functions
"""


def get_chart_title_with_dates(time_interval, start_date, end_date):
    """Get chart title based on interval and date range"""
    days_count = (end_date - start_date).days + 1
    
    interval_info = {
        "1 Hour": f"Hourly ({days_count} day(s))",
        "3 Hours": f"Every 3 Hours - 8 points/day ({days_count} day(s))",
        "6 Hours": f"Every 6 Hours - 4 points/day ({days_count} day(s))",
        "12 Hours": f"Every 12 Hours - 2 points/day ({days_count} day(s))",
        "24 Hours": f"Daily - 1 point/day ({days_count} day(s))"
    }
    
    return interval_info.get(time_interval, f"({days_count} day(s))")