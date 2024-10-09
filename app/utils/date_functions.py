import datetime

def get_current_season():
    current_date = datetime.date.today()
    current_year = current_date.year
    current_month = current_date.month

    if current_month >= 8:  # Season starts in August
        return f"{str(current_year)}-{str(current_year + 1)}"
    else:
        return f"{str(current_year - 1)}-{str(current_year)}"
    
def get_current_date():
	return datetime.date.today().strftime('%Y-%m-%d')