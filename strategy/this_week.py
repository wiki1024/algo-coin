from datetime import datetime, timedelta


def calculate_expire_date(today=None):
	if today is None:
		today = datetime.utcnow()

	weekday_now = today.weekday()

	if weekday_now == 4:
		if today.hour < 8:
			return today.replace(hour=8,
			                     minute=0,
			                     second=0,
			                     microsecond=0)
		else:
			return (today + timedelta(7)).replace(hour=8,
			                                      minute=0,
			                                      second=0,
			                                      microsecond=0)
	else:
		cur = today
		while cur.weekday() != 4:
			cur = cur + timedelta(1)
		return cur.replace(hour=8,
		                   minute=0,
		                   second=0,
		                   microsecond=0)
