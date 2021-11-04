logfile := $(shell date +%Y-%m-%d).log

submit:
	python3 -B scripts/submit.py > logs/$(logfile)