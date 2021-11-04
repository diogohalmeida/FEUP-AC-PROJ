SHELL := bash

logfile := $(shell date +%Y-%m-%d).log

submit:
	python3 -B scripts/submit.py >> logs/$(logfile)

load_merge:
	python3 -B scripts/load_merge.py >> logs/$(logfile)