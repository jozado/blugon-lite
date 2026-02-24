DESTDIR :=
PREFIX := /usr

build:
	sed "s|MAKE_INSTALL_PREFIX = '.*'|MAKE_INSTALL_PREFIX = '$(PREFIX)'|g" blugon-lite.py > blugon-lite
	gzip --best --force --keep blugon-lite.1
	cd backends/scg && make build

install:
	install -D -m755 blugon-lite $(DESTDIR)$(PREFIX)/bin/blugon-lite
	install -D -m644 blugon-lite.1.gz $(DESTDIR)$(PREFIX)/share/man/man1/blugon-lite.1.gz
	install -D -m644 bash-completion/blugon-lite $(DESTDIR)$(PREFIX)/share/bash-completion/completions/blugon-lite
	install -D -m755 backends/scg/scg $(DESTDIR)$(PREFIX)/lib/blugon-lite/scg
	install -D -m644 configs/evening/gamma $(DESTDIR)$(PREFIX)/share/blugon-lite/configs/evening/gamma
	install -D -m644 configs/office/gamma $(DESTDIR)$(PREFIX)/share/blugon-lite/configs/office/gamma
	install -D -m644 configs/student/gamma $(DESTDIR)$(PREFIX)/share/blugon-lite/configs/student/gamma
	install -D -m644 configs/night-owl/gamma $(DESTDIR)$(PREFIX)/share/blugon-lite/configs/night-owl/gamma
	install -D -m644 configs/minimal/gamma $(DESTDIR)$(PREFIX)/share/blugon-lite/configs/minimal/gamma

uninstall:
	rm -f $(DESTDIR)$(PREFIX)/bin/blugon-lite
	rm -f $(DESTDIR)$(PREFIX)/share/man/man1/blugon-lite.1.gz
	rm -f $(DESTDIR)$(PREFIX)/share/bash-completion/completions/blugon-lite
	rm -rf $(DESTDIR)$(PREFIX)/lib/blugon-lite
	rm -rf $(DESTDIR)$(PREFIX)/share/blugon-lite

clean:
	rm -f blugon-lite
	rm -f blugon-lite.1.gz
	cd backends/scg && make clean

.PHONY: build install uninstall clean
