SHELL := bash

logfile := $(shell date +%Y-%m-%d).log

default: submit

submit: apply-model
	python3 -B scripts/submit.py >> logs/$(logfile)

apply-model: process
	python3 -B scripts/apply_model.py >> logs/$(logfile)

process: merge
	python3 -B scripts/process.py >> logs/$(logfile)

merge: clean-data
	python3 -B scripts/merge.py >> logs/$(logfile)

clean-data: load
	python3 -B scripts/clean.py >> logs/$(logifle)

load:
	python3 -B scripts/load.py >> logs/$(logfile)

clean:
	rm -rf dev/*