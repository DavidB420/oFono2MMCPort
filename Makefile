PREFIX ?= /usr
LIBDIR ?= $(PREFIX)/lib
BINDIR ?= $(PREFIX)/bin
SYSTEMD_DIR = /usr/lib/systemd/system
POLKIT_DIR = /etc/polkit-1/localauthority/10-vendor.d

MAIN = main.c
MAINOUTPUT = main
OFONO2MM_DIR = ofono2mm
DBUS_XML = dbus.xml
OFONO_XML_FILES = ofono.xml ofono_modem.xml ofono_operator.xml ofono_context.xml
SYSTEMD_CONF = systemd/10-ofono2mm.conf
POLKIT_PKLA = extra/ofono2mm-radio.pkla

.PHONY: all install uninstall

all:
	@echo "Run 'make install' to install the files."

build:
	gcc $(MAIN) -o $(MAINOUTPUT) 

install:
	install -d $(LIBDIR)/ofono2mm

	install -m 755 $(MAIN) $(LIBDIR)/ofono2mm/
	ln -sf $(LIBDIR)/ofono2mm/$(MAIN) $(BINDIR)/ofono2mm

	cp -r $(OFONO2MM_DIR) $(LIBDIR)/ofono2mm/

	install -m 644 $(DBUS_XML) $(LIBDIR)/ofono2mm/
	install -m 644 $(OFONO_XML_FILES) $(LIBDIR)/ofono2mm/

ifeq ($(shell test -d $(SYSTEMD_DIR) && echo 1),1)
	install -d $(SYSTEMD_DIR)/ModemManager.service.d
	install -m 644 $(SYSTEMD_CONF) $(SYSTEMD_DIR)/ModemManager.service.d/
endif

ifeq ($(shell test -d $(POLKIT_DIR) && echo 1),1)
	install -d $(POLKIT_DIR)
	install -m 644 $(POLKIT_PKLA) $(POLKIT_DIR)/
endif

uninstall:
	rm -rf $(LIBDIR)/ofono2mm/
	rm -f $(BINDIR)/ofono2mm
	rm -f $(SYSDIR)/ModemManager.service.d/10-ofono2mm.conf
	rm -f $(POLKIT_DIR)/ofono2mm-radio.pkla
