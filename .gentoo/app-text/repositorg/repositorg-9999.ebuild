# Copyright 1999-2017 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2

EAPI=6

DESCRIPTION=" Automatically reposit, organize, rename, and process large collections of files."
HOMEPAGE="https://github.com/TheChymera/repositorg"
SRC_URI=""

LICENSE="GPLv3"
SLOT="0"
KEYWORDS=""
IUSE=""

DEPEND="
	>=dev-python/argh-0.26.2
	media-libs/mutagen
"
RDEPEND="${DEPEND}"


PYTHON_COMPAT=(python3_{4,5,6})
inherit distutils-r1

src_unpack() {
	cp -r -L "$DOTGENTOO_PACKAGE_ROOT" "$S"
}
