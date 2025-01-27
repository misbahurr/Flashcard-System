from datetime import datetime, timedelta

def calculate_next_review(performance, current_interval):
    """SuperMemo-2 Algorithm"""
    if performance < 3:
        return datetime.now() + timedelta(minutes=10)  # Reset
    
    ease_factor = 1.3 + (0.1 * (5 - performance))
    new_interval = current_interval * ease_factor
    return datetime.now() + timedelta(days=new_interval)