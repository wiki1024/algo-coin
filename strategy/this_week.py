from datetime import datetime, timedelta, timezone


def calculate_expire_date():
	utc_now = datetime.utcnow().replace(tzinfo=timezone.utc)
	today = utc_now.astimezone(timezone(timedelta(hours=8)))
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
