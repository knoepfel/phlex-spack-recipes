# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.cmake import CMakePackage
from spack_repo.fnal_art.packages.fnal_github_package.package import *

from spack.package import *


class Phlex(CMakePackage, FnalGithubPackage):
    """Parallel, hierarchical, and layered execution of data-processing algorithms"""

    git = "https://github.com/framework-r-d/phlex"
    version_patterns = ["v0.1.0"]

    maintainers("knoepfel")

    license("Apache-2.0")

    # Development version
    version("develop", branch="main", get_full_repo=True)

    # Released versions
    version("0.3.2", sha256="0b10cd4ab6c43019fb2c216014f4666bc643647a06a464815a2a5c6f1536ce89")
    version("0.3.1", sha256="1689fced4229b82be54269b2e785ad75f65869dbbbe0275194620294bc9b9095")
    version("0.3.0", sha256="2219a7f504873563b8befd85afd5ddc2a8a3b1ffe8e61caf219cdc4609271408")
    version("0.2.0", sha256="37833e1b976ec534d8da5b9ec412f297426e2e534ae8e471124f6a1859fe9841")
    version("0.1.0", sha256="b525540e7526f9cefe8537b06640917ece70f771af3270e6bb0aa2722d23d915")

    variant(
        "cxxstd",
        default="23",
        values=(conditional("20", when="@0.1.0"), conditional("23", when="@0.2.0:")),
        multi=False,
        description="Use the specified C++ standard when building.",
    )

    variant("form", default=True, description="Build with experimental FORM integration")

    depends_on("cmake@3.31:", type="build")
    depends_on("cxx", type="build")

    depends_on("boost@1.88.0: +json+program_options")
    depends_on("cppgsl@4:", when="@0.4:")
    depends_on("fmt@11.2:")
    depends_on("jsonnet")
    depends_on("spdlog")
    depends_on("tbb", when="@:0.3")
    depends_on("tbb@2023", when="@0.4:")
    depends_on("catch2", type=("build", "test"))

    # Python dependencies
    depends_on("python@3.12:")
    depends_on("py-numpy@2:")
    depends_on("py-packaging", type="build")  # Used to check (e.g.) numpy versions in CMake
    depends_on("py-pytest", type="build")
    depends_on("py-pyyaml", type="build")  # Used in scripts testing
    with when("@0.3:"):
        depends_on("pkgconf", type="build")
        depends_on("py-numba")
        depends_on("libffi")  # Used in combination with numba

    with when("+form"):
        for std in (20, 23):
            depends_on(f"root +root7 cxxstd={std}", when=f"cxxstd={std}")

    @cmake_preset
    def cmake_args(self):
        return [
            self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd"),
            self.define_from_variant("PHLEX_USE_FORM", "form"),
        ]

    def setup_run_environment(self, env):
        env.prepend_path("PHLEX_PLUGIN_PATH", self.prefix.lib)
