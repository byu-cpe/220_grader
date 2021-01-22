all:
	python3 -m pip install pandas
	git submodule init
	git submodule update

sample:
	python3 run_passoff.py Lab9

clean:
	rm -rf *_passoff
	git co -- Labs.csv Lab9.zip

