import sys
from typing import Union
import sysconfig

import pybind11
import pybind11_extensions
from setuptools import setup, Extension
from distutils import ccompiler
import versioneer

define_macros: list[tuple[str, Union[str, None]]] = [("PYBIND11_DETAILED_ERROR_MESSAGES", None)]
extra_compile_args: list[str] = []
extra_link_args: list[str] = []
libraries: list[str] = []
extra_objects: list[str] = []
extra_sources: list[str] = []

if sys.platform == "win32":
    define_macros.append(("WIN32", None))
    define_macros.append(("_WIN32_WINNT", "0x0601"))
    define_macros.append(("LEVELDB_PLATFORM_WINDOWS", None))
    define_macros.append(("DLLX", "__declspec(dllexport)"))

    extra_sources.append("./submodules/leveldb-mcpe/port/port_win.cc")
    extra_sources.append("./submodules/leveldb-mcpe/util/env_win.cc")
    extra_sources.append("./submodules/leveldb-mcpe/util/win_logger.cc")

    if sys.maxsize > 2**32:  # 64 bit python
        extra_objects.append("bin/zlib/win64/zlibstatic.lib")
    else:  # 32 bit python
        extra_objects.append("bin/zlib/win32/zlibstatic.lib")

elif sys.platform in ["linux", "darwin"]:
    define_macros.append(("LEVELDB_PLATFORM_POSIX", None))
    define_macros.append(("DLLX", ""))
    extra_sources.append("./submodules/leveldb-mcpe/port/port_posix.cc")
    extra_sources.append("./submodules/leveldb-mcpe/util/env_posix.cc")
    libraries.append("z")

    if sys.platform == "darwin":
        define_macros.append(("OS_MACOSX", None))
        # shared_mutex needs MacOS 10.12+
        extra_compile_args.append("-mmacosx-version-min=10.12")
        extra_compile_args.append("-Werror=partial-availability")
        extra_link_args.append("-Wl,-no_weak_imports")
else:
    raise Exception("Unsupported platform")

compiler = sysconfig.get_config_var("CXX") or ccompiler.get_default_compiler()
if compiler.split()[0] == "msvc":
    extra_compile_args.append("/std:c++20")
else:
    extra_compile_args.append("-std=c++20")


setup(
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    ext_modules=[
        Extension(
            name="leveldb.__init__",
            sources=[
                "./src/leveldb/__init__leveldb.py.cpp",
                "./submodules/leveldb-mcpe/db/builder.cc",
                "./submodules/leveldb-mcpe/db/c.cc",
                "./submodules/leveldb-mcpe/db/db_impl.cc",
                "./submodules/leveldb-mcpe/db/db_iter.cc",
                "./submodules/leveldb-mcpe/db/dbformat.cc",
                "./submodules/leveldb-mcpe/db/filename.cc",
                "./submodules/leveldb-mcpe/db/log_reader.cc",
                "./submodules/leveldb-mcpe/db/log_writer.cc",
                "./submodules/leveldb-mcpe/db/memtable.cc",
                "./submodules/leveldb-mcpe/db/repair.cc",
                "./submodules/leveldb-mcpe/db/table_cache.cc",
                "./submodules/leveldb-mcpe/db/version_edit.cc",
                "./submodules/leveldb-mcpe/db/version_set.cc",
                "./submodules/leveldb-mcpe/db/write_batch.cc",
                "./submodules/leveldb-mcpe/table/block.cc",
                "./submodules/leveldb-mcpe/table/block_builder.cc",
                "./submodules/leveldb-mcpe/table/filter_block.cc",
                "./submodules/leveldb-mcpe/table/format.cc",
                "./submodules/leveldb-mcpe/table/iterator.cc",
                "./submodules/leveldb-mcpe/table/merger.cc",
                "./submodules/leveldb-mcpe/table/table.cc",
                "./submodules/leveldb-mcpe/table/table_builder.cc",
                "./submodules/leveldb-mcpe/table/two_level_iterator.cc",
                "./submodules/leveldb-mcpe/util/arena.cc",
                "./submodules/leveldb-mcpe/util/bloom.cc",
                "./submodules/leveldb-mcpe/util/cache.cc",
                "./submodules/leveldb-mcpe/util/coding.cc",
                "./submodules/leveldb-mcpe/util/comparator.cc",
                "./submodules/leveldb-mcpe/util/crc32c.cc",
                "./submodules/leveldb-mcpe/util/env.cc",
                "./submodules/leveldb-mcpe/util/filter_policy.cc",
                "./submodules/leveldb-mcpe/util/hash.cc",
                "./submodules/leveldb-mcpe/util/histogram.cc",
                "./submodules/leveldb-mcpe/util/logging.cc",
                "./submodules/leveldb-mcpe/util/options.cc",
                "./submodules/leveldb-mcpe/util/status.cc",
                "./submodules/leveldb-mcpe/db/zlib_compressor.cc",
                "./submodules/leveldb-mcpe/db/zstd_compressor.cc",
                "./submodules/leveldb-mcpe/port/port_posix_sse.cc",
                *extra_sources,
            ],
            include_dirs=[
                "submodules/zlib",
                "submodules/leveldb-mcpe",
                "submodules/leveldb-mcpe/include",
                pybind11_extensions.get_include(),
                pybind11.get_include()
            ],
            extra_compile_args=extra_compile_args,
            extra_link_args=extra_link_args,
            extra_objects=extra_objects,
            libraries=libraries,
            define_macros=define_macros,
        ),
    ],
)
