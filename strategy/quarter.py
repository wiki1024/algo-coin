from datetime import datetime


def calculate_expire_date(now=None):
	season_month = [3, 6, 9, 12]
	if now is None:
		now = datetime.utcnow()
	for i in range(len(season_month)):
		start_date = now.replace(month=season_month[i], hour=8, day=28, minute=0, second=0, microsecond=0)
		if now < start_date:
			return start_date
		if i + 1 == len(season_month):
			return now.replace(year=now.year + 1, month=season_month[0], hour=8, day=28, minute=0, second=0, microsecond=0)
