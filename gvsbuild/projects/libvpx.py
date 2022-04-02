#  Copyright (C) 2016 - Yevgen Muntyan
#  Copyright (C) 2016 - Ignacio Casal Quinteiro
#  Copyright (C) 2016 - Arnavion
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

import os

from gvsbuild.utils.base_expanders import Tarball
from gvsbuild.utils.base_project import Project, project_add
from gvsbuild.utils.utils import convert_to_msys


@project_add
class Libvpx(Tarball, Project):
    def __init__(self):
        Project.__init__(
            self,
            "libvpx",
            archive_url="https://github.com/webmproject/libvpx/archive/v1.10.0.tar.gz",
            hash="85803ccbdbdd7a3b03d930187cb055f1353596969c1f92ebec2db839fa4f834a",
            dependencies=["yasm", "msys2", "libyuv", "perl"],
            patches=[
                "0006-gen_msvs_vcxproj.sh-Select-current-Windows-SDK-if-av.patch",
                "0001-Always-generate-pc-file.patch",
            ],
        )

    def build(self):
        configure_options = (
            "--enable-pic --as=yasm --disable-unit-tests --size-limit=16384x16384 "
            "--enable-postproc --enable-multi-res-encoding --enable-temporal-denoising "
            "--enable-vp9-temporal-denoising --enable-vp9-postproc --disable-tools "
            "--disable-examples --disable-docs "
        )
        if self.builder.opts.configuration == "debug":
            configure_options += "--enable-debug_libs"

        if self.builder.x86:
            target = "x86-win32-vs"
        else:
            target = "x86_64-win64-vs"

        target += self.builder.opts.vs_ver

        msys_path = Project.get_tool_path("msys2")

        self.exec_vs(
            r"%s\bash ./configure --target=%s --prefix=%s %s"
            % (
                msys_path,
                target,
                convert_to_msys(self.builder.gtk_dir),
                configure_options,
            ),
            add_path=msys_path,
        )
        self.exec_vs(r"make", add_path=msys_path)
        self.exec_vs(r"make install", add_path=msys_path)

        self.install(r".\LICENSE share\doc\libvpx")

    def post_install(self):
        # LibVPX generates a static library named 'vpxmd.lib' or 'vpxmdd.lib'
        # in an unusual directory which is not the same as expected by the vpx.pc file
        if self.builder.opts.configuration == "debug":
            lib_name = "vpxmdd.lib"
        else:
            lib_name = "vpxmd.lib"
        lib_path = f"Win32/{lib_name}" if self.builder.x86 else f"x64/{lib_name}"
        self.builder.exec_msys(
            ["mv", lib_path, "./vpx.lib"],
            working_dir=os.path.join(self.builder.gtk_dir, "lib"),
        )