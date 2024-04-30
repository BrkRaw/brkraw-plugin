clean:
	rm -rf tests/sordino

sordino: tests/sordino
	brk-tonifti sordino -i sordino_test.zip