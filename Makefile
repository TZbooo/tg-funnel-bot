django := venv/bin/python3.11 tg_funnel_bot/manage.py

all:
	sh -c "$(django) $(cmd)"