# Copyright 1999-2018 Gentoo Authors
# Distributed under the terms of the GNU General Public License v2

EAPI=7

PYTHON_COMPAT=(python3_{6,7,8})

inherit distutils-r1 systemd

DESCRIPTION="Automatically reposit, organize, rename, and process large collections of files."
HOMEPAGE="https://github.com/TheChymera/repositorg"
SRC_URI=""

LICENSE="GPLv3"
SLOT="0"
KEYWORDS=""
IUSE=""

DEPEND="
	>=dev-python/argh-0.26.2[${PYTHON_USEDEP}]
	media-libs/mutagen
	dev-python/regex[${PYTHON_USEDEP}]
"
RDEPEND="${DEPEND}"

src_unpack() {
	cp -r -L "$DOTGENTOO_PACKAGE_ROOT" "$S"
}

python_install() {
	distutils-r1_python_install
	systemd_newunit "${FILESDIR}/${PN}_uuid.service" "${PN}_uuid@.service"
	dobin repositorg_uuid
}

src_test() {
	cd test_scripts/
	for i in *.sh; do
		./"$i" || die "Test $i failed"
	done
}
