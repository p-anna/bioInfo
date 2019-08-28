.PHONY: clean

clean:
	rm *~ *#
	rm *csv

rmFolders:
	rm -r abyss velvet spades
	rm -r statistics gam-ngs
	rm -r quast
