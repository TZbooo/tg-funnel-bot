django := venv/bin/python tg_funnel_bot/manage.py

all:
	sh -c "$(django) $(cmd)"