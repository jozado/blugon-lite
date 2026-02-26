DESTDIR :=
PREFIX := /usr

build:
	sed "s|MAKE_INSTALL_PREFIX = '.*'|MAKE_INSTALL_PREFIX = '$(PREFIX)'|g" blugon-lite.py > blugon-lite
	gzip --best --force --keep blugon-lite.1
	cd backends/scg && make build
	# Copiar archivos adicionales para el paquete .deb (solo si no existen)
	cp -n blugon-lite.desktop blugon-lite.svg INSTALL.md . 2>/dev/null || true

install:
	install -D -m755 blugon-lite $(DESTDIR)$(PREFIX)/bin/blugon-lite
	install -D -m755 blugon-lite-tui $(DESTDIR)$(PREFIX)/bin/blugon-lite-tui
	install -D -m755 blugon-lite-monitor $(DESTDIR)$(PREFIX)/bin/blugon-lite-monitor
	install -D -m755 blugon-lite-autostart.sh $(DESTDIR)$(PREFIX)/bin/blugon-lite-autostart.sh
	install -D -m755 blugon-lite-tui.py $(DESTDIR)$(PREFIX)/lib/blugon-lite/blugon-lite-tui.py
	install -D -m644 tui/__init__.py $(DESTDIR)$(PREFIX)/lib/blugon-lite/tui/__init__.py
	install -D -m644 tui/app.py $(DESTDIR)$(PREFIX)/lib/blugon-lite/tui/app.py
	install -D -m644 tui/config.py $(DESTDIR)$(PREFIX)/lib/blugon-lite/tui/config.py
	install -D -m644 tui/utils.py $(DESTDIR)$(PREFIX)/lib/blugon-lite/tui/utils.py
	install -D -m644 tui/themes.py $(DESTDIR)$(PREFIX)/lib/blugon-lite/tui/themes.py
	install -D -m644 tui/widgets/__init__.py $(DESTDIR)$(PREFIX)/lib/blugon-lite/tui/widgets/__init__.py
	install -D -m644 tui/input_handler.py $(DESTDIR)$(PREFIX)/lib/blugon-lite/tui/input_handler.py
	install -D -m644 tui/modals/__init__.py $(DESTDIR)$(PREFIX)/lib/blugon-lite/tui/modals/__init__.py
	install -D -m644 tui/modals/base.py $(DESTDIR)$(PREFIX)/lib/blugon-lite/tui/modals/base.py
	install -D -m644 tui/modals/edit_modal.py $(DESTDIR)$(PREFIX)/lib/blugon-lite/tui/modals/edit_modal.py
	install -D -m644 tui/modals/add_modal.py $(DESTDIR)$(PREFIX)/lib/blugon-lite/tui/modals/add_modal.py
	install -D -m644 tui/modals/delete_modal.py $(DESTDIR)$(PREFIX)/lib/blugon-lite/tui/modals/delete_modal.py
	install -D -m644 tui/modals/theme_modal.py $(DESTDIR)$(PREFIX)/lib/blugon-lite/tui/modals/theme_modal.py
	install -D -m644 blugon-lite.1.gz $(DESTDIR)$(PREFIX)/share/man/man1/blugon-lite.1.gz
	install -D -m644 blugon-lite.1.gz $(DESTDIR)$(PREFIX)/share/man/man1/blugon-lite-tui.1.gz
	install -D -m644 bash-completion/blugon-lite $(DESTDIR)$(PREFIX)/share/bash-completion/completions/blugon-lite
	install -D -m755 backends/scg/scg $(DESTDIR)$(PREFIX)/lib/blugon-lite/scg
	install -D -m644 configs/evening/gamma $(DESTDIR)$(PREFIX)/share/blugon-lite/configs/evening/gamma
	install -D -m644 configs/office/gamma $(DESTDIR)$(PREFIX)/share/blugon-lite/configs/office/gamma
	install -D -m644 configs/student/gamma $(DESTDIR)$(PREFIX)/share/blugon-lite/configs/student/gamma
	install -D -m644 configs/night-owl/gamma $(DESTDIR)$(PREFIX)/share/blugon-lite/configs/night-owl/gamma
	install -D -m644 configs/minimal/gamma $(DESTDIR)$(PREFIX)/share/blugon-lite/configs/minimal/gamma
	install -D -m644 blugon-lite.desktop $(DESTDIR)$(PREFIX)/share/applications/blugon-lite.desktop
	install -D -m644 blugon-lite-autostart.desktop $(DESTDIR)$(PREFIX)/share/applications/blugon-lite-autostart.desktop
	install -D -m644 blugon-lite.svg $(DESTDIR)$(PREFIX)/share/icons/hicolor/scalable/apps/blugon-lite.svg
	install -D -m644 README.md $(DESTDIR)$(PREFIX)/share/doc/blugon-lite/README.md
	install -D -m644 INSTALL.md $(DESTDIR)$(PREFIX)/share/doc/blugon-lite/INSTALL.md
	# Systemd service
	install -D -m644 debian/blugon-lite.service $(DESTDIR)$(PREFIX)/lib/systemd/system/blugon-lite.service
	# SysV init script
	install -D -m755 debian/init.d $(DESTDIR)$(PREFIX)/etc/init.d/blugon-lite

uninstall:
	rm -f $(DESTDIR)$(PREFIX)/bin/blugon-lite
	rm -f $(DESTDIR)$(PREFIX)/bin/blugon-lite-tui
	rm -rf $(DESTDIR)$(PREFIX)/lib/blugon-lite
	rm -f $(DESTDIR)$(PREFIX)/share/man/man1/blugon-lite.1.gz
	rm -f $(DESTDIR)$(PREFIX)/share/man/man1/blugon-lite-tui.1.gz
	rm -f $(DESTDIR)$(PREFIX)/share/bash-completion/completions/blugon-lite
	rm -rf $(DESTDIR)$(PREFIX)/share/blugon-lite
	rm -f $(DESTDIR)$(PREFIX)/share/applications/blugon-lite.desktop
	rm -f $(DESTDIR)$(PREFIX)/share/applications/blugon-lite-autostart.desktop
	rm -f $(DESTDIR)$(PREFIX)/share/icons/hicolor/scalable/apps/blugon-lite.svg
	rm -rf $(DESTDIR)$(PREFIX)/share/doc/blugon-lite
	rm -f $(DESTDIR)$(PREFIX)/lib/systemd/system/blugon-lite.service
	rm -f $(DESTDIR)$(PREFIX)/etc/init.d/blugon-lite

clean:
	rm -f blugon-lite
	rm -f blugon-lite.1.gz
	rm -f blugon-lite.svg
	rm -f INSTALL.md
	cd backends/scg && make clean

# Target para construir paquete .deb
deb: clean build
	# Asegurar que todo esté compilado
	dpkg-deb --build debian blugon-lite_1.0.0-lite_amd64.deb
	@echo ""
	@echo "Paquete .deb construido: blugon-lite_1.0.0-lite_amd64.deb"

.PHONY: build install uninstall clean deb
