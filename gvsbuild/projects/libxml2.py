#  Copyright (C) 2016 The Gvsbuild Authors
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, see <http://www.gnu.org/licenses/>.

from gvsbuild.utils.base_builders import Meson
from gvsbuild.utils.base_expanders import Tarball
from gvsbuild.utils.base_project import Project, project_add


@project_add
class Libxml2(Tarball, Meson):
    def __init__(self):
        Project.__init__(
            self,
            "libxml2",
            version="2.12.3",
            lastversion_even=True,
            repository="https://gitlab.gnome.org/GNOME/libxml2",
            archive_url="https://download.gnome.org/sources/libxml2/{major}.{minor}/libxml2-{version}.tar.xz",
            hash="8c8f1092340a89ff32bc44ad5c9693aff9bc8a7a3e161bb239666e5d15ac9aaa",
            dependencies=["win-iconv", "meson", "ninja"],
            patches=[],
        )

    def build(self):
        Meson.build(self)
        self.install_pc_files()
        self.install(r".\COPYING share\doc\libxml2")
