#!/bin/bash
# Script para construir el paquete .deb de blugon-lite

set -e

PACKAGE_NAME="blugon-lite"
VERSION="1.0.0-lite"
ARCH="amd64"

echo "=== Construyendo $PACKAGE_NAME $VERSION ==="

# Limpiar
rm -rf debian/tmp
rm -f ${PACKAGE_NAME}_${VERSION}-${ARCH}.deb

# Crear directorio temporal
mkdir -p debian/tmp

# Instalar en directorio temporal
make install DESTDIR=$(pwd)/debian/tmp PREFIX=/usr

# Copiar archivos DEBIAN
cp -r debian/DEBIAN debian/tmp/DEBIAN

# Ajustar permisos
chmod 755 debian/tmp/DEBIAN/postinst debian/tmp/DEBIAN/prerm debian/tmp/DEBIAN/postrm debian/tmp/DEBIAN/init.d

# Construir paquete
dpkg-deb --build debian/tmp ${PACKAGE_NAME}_${VERSION}-${ARCH}.deb

# Limpiar
rm -rf debian/tmp

echo ""
echo "=== Paquete construido: ${PACKAGE_NAME}_${VERSION}-${ARCH}.deb ==="
ls -lh ${PACKAGE_NAME}_${VERSION}-${ARCH}.deb
