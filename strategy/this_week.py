from datetime import datetime, timedelta


def calculate_expire_date():
	today = datetime.now()
	weekday_now = today.weekday()

	if weekday_now == 4:
		if today.hour < 16:
			return today.replace(hour=16,
			                     minute=0,
			                     second=0,
			                     microsecond=0)
		else:
			return (today + timedelta(7)).replace(hour=16,
			                                      minute=0,
			                                      second=0,
			                                      microsecond=0)
	else:
		cur = today
		while cur.weekday() != 4:
			cur = cur + timedelta(1)
		return cur.replace(hour=16,
		                   minute=0,
		                   second=0,
		                   microsecond=0)
