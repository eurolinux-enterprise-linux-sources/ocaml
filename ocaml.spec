# OCaml has a bytecode backend that works on anything with a C
# compiler, and a native code backend available on a subset of
# architectures.  A further subset of architectures support native
# dynamic linking.

%ifarch %{ocaml_native_compiler}
%global native_compiler 1
%else
%global native_compiler 0
%endif

%ifarch %{ocaml_natdynlink}
%global natdynlink 1
%else
%global natdynlink 0
%endif

# These are all the architectures that the tests run on.  The tests
# take a long time to run, so don't run them on slow machines.
# - ppc64: tests hang under Koji with:
#     Thread 1 killed on uncaught exception Unix.Unix_error(25, "accept", "")
#   Unable to reproduce this failure locally.
%global test_arches          aarch64 ppc64le x86_64
# These are the architectures for which the tests must pass otherwise
# the build will fail.
%global test_arches_required aarch64 ppc64le x86_64

# Architectures where parallel builds fail.
#%global no_parallel_build_arches aarch64

Name:           ocaml
Version:        4.05.0
Release:        6%{?dist}

Summary:        OCaml compiler and programming environment

License:        QPL and (LGPLv2+ with exceptions)

URL:            http://www.ocaml.org

Source0:        http://caml.inria.fr/pub/distrib/ocaml-4.05/ocaml-%{version}.tar.xz

Source1:        http://caml.inria.fr/pub/distrib/ocaml-4.05/ocaml-4.05-refman-html.tar.gz
Source2:        http://caml.inria.fr/pub/distrib/ocaml-4.05/ocaml-4.05-refman.pdf
Source3:        http://caml.inria.fr/pub/distrib/ocaml-4.05/ocaml-4.05-refman.info.tar.gz

# IMPORTANT NOTE:
#
# These patches are generated from unpacked sources stored in a
# pagure.io git repository.  If you change the patches here, they will
# be OVERWRITTEN by the next update.  Instead, request commit access
# to the pagure project:
#
# https://pagure.io/fedora-ocaml
#
# Current branch: rhel-7.5-4.05.0
#
# ALTERNATIVELY add a patch to the end of the list (leaving the
# existing patches unchanged) adding a comment to note that it should
# be incorporated into the git repo at a later time.
#

# Upstream patches after 4.05.
Patch0001:      0001-Changes-clarify-compatibility-breaking-change-items.patch
Patch0002:      0002-MPR-7591-frametable-not-8-aligned-on-x86-64-port.patch
Patch0003:      0003-Fixes-for-out-of-range-Ialloc.patch

# Fedora-specific downstream patches.
Patch0004:      0004-Don-t-add-rpaths-to-libraries.patch
Patch0005:      0005-ocamlbyteinfo-ocamlplugininfo-Useful-utilities-from-.patch
Patch0006:      0006-configure-Allow-user-defined-C-compiler-flags.patch

# Out of tree patches for RISC-V support.
# https://github.com/nojb/riscv-ocaml
Patch0007:      0007-Adapt-config.guess-for-RISC-V.patch
Patch0008:      0008-Add-RISC-V-backend-runtime.patch
Patch0009:      0009-Try-fix-for-andi-ori-xori-immediates-1.patch
Patch0010:      0010-Fix-immediates-range-when-adjusting-indexing-sp.patch
Patch0011:      0011-Another-immediate-range-fix.patch

# Fix for some aarch64 linker problems.
# https://caml.inria.fr/mantis/view.php?id=7585
Patch0012:      0012-AArch64-GOT-fixed.patch

BuildRequires:  ocaml-srpm-macros
BuildRequires:  binutils-devel
BuildRequires:  ncurses-devel
BuildRequires:  gdbm-devel
%ifnarch riscv64
BuildRequires:  emacs
%endif
BuildRequires:  gawk
BuildRequires:  perl
BuildRequires:  util-linux
BuildRequires:  libICE-devel
BuildRequires:  libSM-devel
BuildRequires:  libX11-devel
BuildRequires:  libXaw-devel
BuildRequires:  libXext-devel
BuildRequires:  libXft-devel
BuildRequires:  libXmu-devel
BuildRequires:  libXrender-devel
BuildRequires:  libXt-devel
BuildRequires:  mesa-libGL-devel
BuildRequires:  mesa-libGLU-devel
BuildRequires:  chrpath

Requires:       ocaml-srpm-macros
Requires:       gcc

# Because we pass -c flag to ocaml-find-requires (to avoid circular
# dependencies) we also have to explicitly depend on the right version
# of ocaml-runtime.
Requires:       ocaml-runtime = %{version}-%{release}

# Bundles an MD5 implementation in byterun/md5.{c,h}
Provides:       bundled(md5-plumb)

Provides:       ocaml(compiler) = %{version}

# These subpackages were removed in RHEL 7.5.  It is intended that
# they will be replaced by new packages in EPEL.
Obsoletes:      ocaml-labltk <= %{version}-%{release}
Obsoletes:      ocaml-labltk-devel <= %{version}-%{release}

%global __ocaml_requires_opts -c -f '%{buildroot}%{_bindir}/ocamlrun %{buildroot}%{_bindir}/ocamlobjinfo.byte'
%global __ocaml_provides_opts -f '%{buildroot}%{_bindir}/ocamlrun %{buildroot}%{_bindir}/ocamlobjinfo.byte'


%description
OCaml is a high-level, strongly-typed, functional and object-oriented
programming language from the ML family of languages.

This package comprises two batch compilers (a fast bytecode compiler
and an optimizing native-code compiler), an interactive toplevel system,
parsing tools (Lex,Yacc), a replay debugger, a documentation generator,
and a comprehensive library.


%package runtime
Summary:        OCaml runtime environment
Requires:       util-linux
Provides:       ocaml(runtime) = %{version}

%description runtime
OCaml is a high-level, strongly-typed, functional and object-oriented
programming language from the ML family of languages.

This package contains the runtime environment needed to run OCaml
bytecode.


%package source
Summary:        Source code for OCaml libraries
Requires:       ocaml = %{version}-%{release}

%description source
Source code for OCaml libraries.


%package x11
Summary:        X11 support for OCaml
Requires:       ocaml-runtime = %{version}-%{release}
Requires:       libX11-devel

%description x11
X11 support for OCaml.


%package ocamldoc
Summary:        Documentation generator for OCaml
Requires:       ocaml = %{version}-%{release}
Provides:	ocamldoc

%description ocamldoc
Documentation generator for OCaml.


%ifnarch riscv64
%package emacs
Summary:        Emacs mode for OCaml
Requires:       ocaml = %{version}-%{release}
Requires:       emacs(bin)

%description emacs
Emacs mode for OCaml.
%endif


%package docs
Summary:        Documentation for OCaml
Requires:       ocaml = %{version}-%{release}
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info


%description docs
OCaml is a high-level, strongly-typed, functional and object-oriented
programming language from the ML family of languages.

This package contains documentation in PDF and HTML format as well as
man pages and info files.


%package compiler-libs
Summary:        Compiler libraries for OCaml
Requires:       ocaml = %{version}-%{release}


%description compiler-libs
OCaml is a high-level, strongly-typed, functional and object-oriented
programming language from the ML family of languages.

This package contains some modules used internally by the OCaml
compilers, useful for the development of some OCaml applications.
Note that this exposes internal details of the OCaml compiler which
may not be portable between versions.


%prep
%setup -q -T -b 0 -n %{name}-%{version}
%setup -q -T -D -a 1 -n %{name}-%{version}
%setup -q -T -D -a 3 -n %{name}-%{version}
cp %{SOURCE2} refman.pdf
%autopatch -p1


%build
# Parallel builds are broken in 4.05.0, see
# https://caml.inria.fr/mantis/view.php?id=7587
#%ifnarch %{no_parallel_build_arches}
#make="make %{?_smp_mflags}"
#%else
unset MAKEFLAGS
make=make
#%endif

CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing" \
./configure \
    -bindir %{_bindir} \
    -libdir %{_libdir}/ocaml \
    -x11lib %{_libdir} \
    -x11include %{_includedir} \
    -mandir %{_mandir}/man1 \
    -no-curses
$make world
%if %{native_compiler}
$make opt
$make opt.opt
%endif
%ifnarch riscv64
make -C emacs ocamltags
%endif

# Currently these tools are supplied by Debian, but are expected
# to go upstream at some point.
includes="-nostdlib -I stdlib -I utils -I parsing -I typing -I bytecomp -I asmcomp -I driver -I otherlibs/unix -I otherlibs/str -I otherlibs/dynlink"
boot/ocamlrun ./ocamlc $includes dynlinkaux.cmo ocamlbyteinfo.ml -o ocamlbyteinfo
# ocamlplugininfo doesn't compile because it needs 'dynheader' (type
# decl) and I have no idea where that comes from
#cp otherlibs/dynlink/natdynlink.ml .
#boot/ocamlrun ./ocamlopt $includes unix.cmxa str.cmxa natdynlink.ml ocamlplugininfo.ml -o ocamlplugininfo


%check
%ifarch %{test_arches}
cd testsuite

%ifarch %{test_arches_required}
make -j1 all
%else
make -j1 all ||:
%endif
%endif


%install
make install \
     BINDIR=$RPM_BUILD_ROOT%{_bindir} \
     LIBDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml \
     MANDIR=$RPM_BUILD_ROOT%{_mandir}
perl -pi -e "s|^$RPM_BUILD_ROOT||" $RPM_BUILD_ROOT%{_libdir}/ocaml/ld.conf

%ifnarch riscv64
(
    # install emacs files
    cd emacs;
    make install \
         BINDIR=$RPM_BUILD_ROOT%{_bindir} \
         EMACSDIR=$RPM_BUILD_ROOT%{_datadir}/emacs/site-lisp
    make install-ocamltags BINDIR=$RPM_BUILD_ROOT%{_bindir}
)
%endif

(
    # install info files
    mkdir -p $RPM_BUILD_ROOT%{_infodir};
    cd infoman; cp ocaml*.gz $RPM_BUILD_ROOT%{_infodir}
)

echo %{version} > $RPM_BUILD_ROOT%{_libdir}/ocaml/fedora-ocaml-release

# Remove rpaths from stublibs .so files.
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/ocaml/stublibs/*.so

install -m 0755 ocamlbyteinfo $RPM_BUILD_ROOT%{_bindir}
#install -m 0755 ocamlplugininfo $RPM_BUILD_ROOT%{_bindir}

find $RPM_BUILD_ROOT -name .ignore -delete

# Remove .cmt and .cmti files, for now.  We could package them later.
# See also: http://www.ocamlpro.com/blog/2012/08/20/ocamlpro-and-4.00.0.html
find $RPM_BUILD_ROOT \( -name '*.cmt' -o -name '*.cmti' \) -a -delete


%post docs
/sbin/install-info \
    --entry="* ocaml: (ocaml).   The OCaml compiler and programming environment" \
    --section="Programming Languages" \
    %{_infodir}/%{name}.info \
    %{_infodir}/dir 2>/dev/null || :


%preun docs
if [ $1 -eq 0 ]; then
  /sbin/install-info --delete %{_infodir}/%{name}.info %{_infodir}/dir 2>/dev/null || :
fi


%files
%doc LICENSE
%{_bindir}/ocaml

%{_bindir}/ocamlbyteinfo
%{_bindir}/ocamldebug
#%{_bindir}/ocamlplugininfo
%{_bindir}/ocamlyacc

# symlink to either .byte or .opt version
%{_bindir}/ocamlc
%{_bindir}/ocamlcp
%{_bindir}/ocamldep
%{_bindir}/ocamllex
%{_bindir}/ocamlmklib
%{_bindir}/ocamlmktop
%{_bindir}/ocamlobjinfo
%{_bindir}/ocamloptp
%{_bindir}/ocamlprof

# bytecode versions
%{_bindir}/ocamlc.byte
%{_bindir}/ocamlcp.byte
%{_bindir}/ocamldep.byte
%{_bindir}/ocamllex.byte
%{_bindir}/ocamlmklib.byte
%{_bindir}/ocamlmktop.byte
%{_bindir}/ocamlobjinfo.byte
%{_bindir}/ocamloptp.byte
%{_bindir}/ocamlprof.byte

%if %{native_compiler}
# native code versions
%{_bindir}/ocamlc.opt
%{_bindir}/ocamlcp.opt
%{_bindir}/ocamldep.opt
%{_bindir}/ocamllex.opt
%{_bindir}/ocamlmklib.opt
%{_bindir}/ocamlmktop.opt
%{_bindir}/ocamlobjinfo.opt
%{_bindir}/ocamloptp.opt
%{_bindir}/ocamlprof.opt
%endif

%if %{native_compiler}
%{_bindir}/ocamlopt
%{_bindir}/ocamlopt.byte
%{_bindir}/ocamlopt.opt
%endif

#%{_libdir}/ocaml/addlabels
#%{_libdir}/ocaml/scrapelabels
%{_libdir}/ocaml/camlheader
%{_libdir}/ocaml/camlheader_ur
%{_libdir}/ocaml/expunge
%{_libdir}/ocaml/extract_crc
%{_libdir}/ocaml/ld.conf
%{_libdir}/ocaml/Makefile.config
%{_libdir}/ocaml/*.a
%if %{natdynlink}
%{_libdir}/ocaml/*.cmxs
%endif
%if %{native_compiler}
%{_libdir}/ocaml/*.cmxa
%{_libdir}/ocaml/*.cmx
%{_libdir}/ocaml/*.o
%{_libdir}/ocaml/libasmrun_shared.so
%endif
%{_libdir}/ocaml/*.mli
%{_libdir}/ocaml/libcamlrun_shared.so
%{_libdir}/ocaml/objinfo_helper
%{_libdir}/ocaml/vmthreads/*.mli
%{_libdir}/ocaml/vmthreads/*.a
%if %{native_compiler}
%{_libdir}/ocaml/threads/*.a
%{_libdir}/ocaml/threads/*.cmxa
%{_libdir}/ocaml/threads/*.cmx
%endif
%{_libdir}/ocaml/caml
%exclude %{_libdir}/ocaml/graphicsX11.mli


%files runtime
%doc README.adoc LICENSE Changes
%{_bindir}/ocamlrun
%dir %{_libdir}/ocaml
%{_libdir}/ocaml/VERSION
%{_libdir}/ocaml/*.cmo
%{_libdir}/ocaml/*.cmi
%{_libdir}/ocaml/*.cma
%{_libdir}/ocaml/stublibs
%dir %{_libdir}/ocaml/vmthreads
%{_libdir}/ocaml/vmthreads/*.cmi
%{_libdir}/ocaml/vmthreads/*.cma
%dir %{_libdir}/ocaml/threads
%{_libdir}/ocaml/threads/*.cmi
%{_libdir}/ocaml/threads/*.cma
%{_libdir}/ocaml/fedora-ocaml-release
%exclude %{_libdir}/ocaml/graphicsX11.cmi


%files source
%doc LICENSE
%{_libdir}/ocaml/*.ml


%files x11
%doc LICENSE
%{_libdir}/ocaml/graphicsX11.cmi
%{_libdir}/ocaml/graphicsX11.mli


%files ocamldoc
%doc LICENSE
%doc ocamldoc/Changes.txt
%{_bindir}/ocamldoc*
%{_libdir}/ocaml/ocamldoc


%files docs
%doc refman.pdf htmlman
%{_infodir}/*
%{_mandir}/man1/*
%{_mandir}/man3/*


%ifnarch riscv64
%files emacs
%doc emacs/README
%{_datadir}/emacs/site-lisp/*
%{_bindir}/ocamltags
%endif


%files compiler-libs
%doc LICENSE
%dir %{_libdir}/ocaml/compiler-libs
%{_libdir}/ocaml/compiler-libs/*.mli
%{_libdir}/ocaml/compiler-libs/*.cmi
%{_libdir}/ocaml/compiler-libs/*.cmo
%{_libdir}/ocaml/compiler-libs/*.cma
%if %{native_compiler}
%{_libdir}/ocaml/compiler-libs/*.a
%{_libdir}/ocaml/compiler-libs/*.cmxa
%{_libdir}/ocaml/compiler-libs/*.cmx
%{_libdir}/ocaml/compiler-libs/*.o
%endif


%changelog
* Mon Sep 25 2017 Richard W.M. Jones <rjones@redhat.com> - 4.05.0-6
- Obsolete only ocaml-labltk (not ocaml-camlp4)
  related: rhbz#1447988

* Fri Sep 22 2017 Richard W.M. Jones <rjones@redhat.com> - 4.05.0-5
- Obsolete ocaml-camlp4 and ocaml-labltk, removed in RHEL 7.5.

* Fri Sep 15 2017 Richard W.M. Jones <rjones@redhat.com> - 4.05.0-4
- Rebase to 4.05.0 (same as Fedora Rawhide).
- Adds support for POWER, z/VM.
- Improves support for aarch64.
  resolves: rhbz#1447988

* Tue Jun 07 2016 Richard W.M. Jones <rjones@redhat.com> - 4.01.0-22.7
- Fix buffer overflow and information leak CVE-2015-8869
  resolves: rhbz#1343081

* Tue Jul 07 2015 Richard W.M. Jones <rjones@redhat.com> - 4.01.0-22.6
- ppc64le: Fix behaviour of Int64.max_int ÷ -1
  resolves: rhbz#1236615

* Thu May 28 2015 Richard W.M. Jones <rjones@redhat.com> - 4.01.0-22.5
- ppc64le: Fix calling convention of external functions with > 8 params
  resolves: rhbz#1225995

* Mon Feb 16 2015 Richard W.M. Jones <rjones@redhat.com> - 4.01.0-22.4
- Fix ppc, ppc64, ppc64le stack non-executable (1214777).

* Mon Feb 16 2015 Richard W.M. Jones <rjones@redhat.com> - 4.01.0-22.3
- Fix caml_callback2 crashes (upstream PR#6489, RHBZ#1197240).

* Thu Sep 11 2014 Richard W.M. Jones <rjones@redhat.com> - 4.01.0-22.2
- Use -fno-strict-aliasing when building the compiler
- ppc, ppc64, ppc64le: Mark stack as non-executable.
  resolves: rhbz#990521
- Provides ocaml(runtime) 4.01.1.
  related: rhbz#1098459

* Thu Sep 11 2014 Richard W.M. Jones <rjones@redhat.com> - 4.01.0-22
- Update to last 4.01 version from OCaml git.
- Fix bug in argument parsing
  resolves: rhbz#1139803

* Thu Jun 26 2014 Richard W.M. Jones <rjones@redhat.com> - 4.01.0-20
- BR binutils-devel so ocamlobjinfo supports *.cmxs files (RHBZ#1113735).

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.01.0-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 21 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 4.01.0-18
- Rebuilt for https://fedoraproject.org/wiki/Changes/f21tcl86

* Sat May 10 2014 Richard W.M. Jones <rjones@redhat.com> - 4.01.0-17
- Mark stack as non-executable on ARM (32 bit) and Aarch64.

* Tue Apr 22 2014 Richard W.M. Jones <rjones@redhat.com> - 4.01.0-16
- Remove ocaml-srpm-macros subpackage.
  This is now a separate package, see RHBZ#1087893.

* Tue Apr 15 2014 Richard W.M. Jones <rjones@redhat.com> - 4.01.0-15
- Fix s390x builds (no native compiler).

* Tue Apr 15 2014 Richard W.M. Jones <rjones@redhat.com> - 4.01.0-14
- Remove ExclusiveArch.
- Add ocaml-srpm-macros subpackage containing arch macros.
- See: RHBZ#1087794

* Mon Apr 14 2014 Richard W.M. Jones <rjones@redhat.com> - 4.01.0-13
- Fix aarch64 relocation problems again.
  Earlier patch was dropped accidentally.

* Wed Apr  9 2014 Richard W.M. Jones <rjones@redhat.com> - 4.01.0-12
- Add ppc64le support (thanks: Michel Normand) (RHBZ#1077767).

* Tue Apr  1 2014 Richard W.M. Jones <rjones@redhat.com> - 4.01.0-11
- Fix --flag=arg patch (thanks: Anton Lavrik, Ignas Vyšniauskas).

* Mon Mar 24 2014 Richard W.M. Jones <rjones@redhat.com> - 4.01.0-10
- Include a fix for aarch64 relocation problems
  http://caml.inria.fr/mantis/view.php?id=6283

* Wed Jan  8 2014 Richard W.M. Jones <rjones@redhat.com> - 4.01.0-8
- Don't use ifarch around Patch lines, as it means the patch files
  don't get included in the spec file.

* Mon Jan  6 2014 Richard W.M. Jones <rjones@redhat.com> - 4.01.0-7
- Work around gcc stack alignment issues, see
  http://caml.inria.fr/mantis/view.php?id=5700

* Tue Dec 31 2013 Richard W.M. Jones <rjones@redhat.com> - 4.01.0-6
- Add aarch64 (arm64) code generator.

* Thu Nov 21 2013 Richard W.M. Jones <rjones@redhat.com> - 4.01.0-4
- Add bundled(md5-plumb) (thanks: Tomas Mraz).
- Add NON-upstream (but being sent upstream) patch to allow --flag=arg
  as an alternative to --flag arg (RHBZ#1028650).

* Sat Sep 14 2013 Richard W.M. Jones <rjones@redhat.com> - 4.01.0-3
- Disable -lcurses.  This is not actually used, just linked with unnecessarily.

* Sat Sep 14 2013 Richard W.M. Jones <rjones@redhat.com> - 4.01.0-2
- Fix the build on ppc64.

* Fri Sep 13 2013 Richard W.M. Jones <rjones@redhat.com> - 4.01.0-1
- Update to new major version OCaml 4.01.0.
- Rebase patches.
- Remove bogus Requires 'ncurses-devel'.  The base ocaml package already
  pulls in the library implicitly.
- Remove bogus Requires 'gdbm-devel'.  Nothing in the source mentions gdbm.
- Use mkstemp instead of mktemp in ocamlyacc.
- Add LICENSE as doc to some subpackages to keep rpmlint happy.
- Remove .ignore file from some packages.
- Remove period from end of Summary.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.00.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.00.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Oct 16 2012 Richard W.M. Jones <rjones@redhat.com> - 4.00.1-1
- Update to upstream version 4.00.1.
- Clean up the spec file further.

* Thu Aug 16 2012 Richard W.M. Jones <rjones@redhat.com> - 4.00.0-2
- ppc supports natdynlink.

* Sat Jul 28 2012 Richard W.M. Jones <rjones@redhat.com> - 4.00.0-1
- Upgrade to OCaml 4.00.0 official release.
- Remove one patch (add -lpthread) which went upstream.

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.00.0-0.6.beta2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jun 10 2012 Richard W.M. Jones <rjones@redhat.com> - 4.00.0-0.5.beta2
- No change, just fix up changelog.

* Thu Jun  7 2012 Richard W.M. Jones <rjones@redhat.com> 4.00.0-0.3.beta2
- Upgrade to OCaml 4.00.0 beta 2.
- The language is now officially called OCaml (not Objective Caml, O'Caml etc)
- Rebase patches on top:
  . New ARM backend patch no longer required, since upstream.
  . Replacement config.guess, config.sub no longer required, since upstream
    versions are newer.
- PPC64 backend rebased and fixed.
  . Increase the default size of the stack when compiling.
- New tool: ocamloptp (ocamlopt profiler).
- New VERSION file in ocaml-runtime package.
- New ocaml-compiler-libs subpackage.
- Rearrange ExclusiveArch alphanumerically.
- alpha, ia64 native backends have been removed upstream, so they are
  no longer supported as native compiler targets.
- Remove defattr.
- Make OCaml dependency generator self-contained so it doesn't need
  previous version of OCaml around.

* Wed Jun  6 2012 Richard W.M. Jones <rjones@redhat.com> 3.12.1-12
- ppc64: Include fix for minor heap corruption because of unaligned
  minor heap register (RHBZ#826649).
- Unset MAKEFLAGS before running build.

* Wed Jun  6 2012 Richard W.M. Jones <rjones@redhat.com> 3.12.1-11
- ppc64: Fix position of stack arguments to external C functions
  when there are more than 8 parameters.

* Tue Jun  5 2012 Richard W.M. Jones <rjones@redhat.com> 3.12.1-10
- Include patch to link dllthreads.so with -lpthread explicitly, to
  fix problem with 'pthread_atfork' symbol missing (statically linked)
  on ppc64.

* Sun Jun  3 2012 Richard W.M. Jones <rjones@redhat.com> 3.12.1-9
- Include svn rev 12548 to fix invalid generation of Thumb-2 branch
  instruction TBH (upstream PR#5623, RHBZ#821153).

* Wed May 30 2012 Richard W.M. Jones <rjones@redhat.com> 3.12.1-8
- Modify the ppc64 patch to reduce the delta between power64 and
  upstream power backends.
- Clean up the spec file and bring it up to modern standards.
  * Remove patch fuzz directive.
  * Remove buildroot directive.
  * Rearrange source unpacking.
  * Remove chmod of GNU config.* files, since git does it.
  * Don't need to remove buildroot in install section.
  * Remove clean section.
  * git am </dev/null to avoid hang (thanks Adam Jackson).
- Note there is no functional change in the above.

* Tue May 29 2012 Richard W.M. Jones <rjones@redhat.com> 3.12.1-6
- Move patches to external git repo:
  http://git.fedorahosted.org/git/?p=fedora-ocaml.git
  There should be no change introduced here.

* Tue May 15 2012 Karsten Hopp <karsten@redhat.com> 3.12.1-4
- ppc64 got broken by the new ARM backend, add a minor patch

* Sat Apr 28 2012 Richard W.M. Jones <rjones@redhat.com> 3.12.1-3
- New ARM backend by Benedikt Meurer, backported to OCaml 3.12.1.
  This has several advantages, including enabling natdynlink on ARM.
- Provide updated config.guess and config.sub (from OCaml upstream tree).

* Thu Jan 12 2012 Richard W.M. Jones <rjones@redhat.com> 3.12.1-2
- add back ocaml-ppc64.patch for ppc secondary arch, drop .cmxs files
  from file list on ppc (cherry picked from F16 - this should have
  gone into Rawhide originally then been cherry picked back to F16)

* Fri Jan  6 2012 Richard W.M. Jones <rjones@redhat.com> - 3.12.1-1
- New upstream version 3.12.1.  This is a bugfix update.

* Thu Dec  8 2011 Richard W.M. Jones <rjones@redhat.com> - 3.12.0-7
- Allow this package to be compiled on platforms without native
  support and/or natdynlink, specifically ppc64.  This updates (and
  hopefully does not break) DJ's previous *.cmxs change for arm.

* Fri Sep 23 2011 DJ Delorie <dj@redhat.com> - 3.12.0-6
- Add arm type directive patch.
- Allow more arm arches.
- Don't package *.cmxs on arm.

* Wed Mar 30 2011 Richard W.M. Jones <rjones@redhat.com> - 3.12.0-5
- Fix for invalid assembler generation (RHBZ#691896).

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.12.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan  5 2011 Richard W.M. Jones <rjones@redhat.com> - 3.12.0-3
- Rebuild with self.

* Tue Jan  4 2011 Richard W.M. Jones <rjones@redhat.com> - 3.12.0-2
- Try depending on OCaml BR to fix:
  /usr/lib/rpm/ocaml-find-provides.sh: /builddir/build/BUILDROOT/ocaml-3.12.0-1.fc15.i386/usr/bin/ocamlobjinfo: /usr/bin/ocamlrun: bad interpreter: No such file or directory

* Tue Jan  4 2011 Richard W.M. Jones <rjones@redhat.com> - 3.12.0-1
- New upstream version 3.12.0.
  http://fedoraproject.org/wiki/Features/OCaml3.12
- Remove ppc64 support patch.
- Rebase rpath removal patch.
- ocamlobjinfo is now an official tool, so no need to compile it by hand.
  Add objinfo_helper.
- Disable ocamlplugininfo.
- Remove addlabels, scrapelabels.
- Remove ocaml/stublibs/dlltkanim.so.

* Fri Jan 29 2010 Richard W.M. Jones <rjones@redhat.com> - 3.11.2-2
- Update reference manual to latest version from website.

* Wed Jan 20 2010 Richard W.M. Jones <rjones@redhat.com> - 3.11.2-1
- Update to 3.11.2 official release.

* Tue Jan  5 2010 Richard W.M. Jones <rjones@redhat.com> - 3.11.2-0.rc1.2
- ocaml-labltk-devel should require tcl-devel and tk-devel.

* Tue Dec 29 2009 Richard W.M. Jones <rjones@redhat.com> - 3.11.2-0.rc1.1
- Update to (release candidate) 3.11.2+rc1.

* Wed Dec 16 2009 Richard W.M. Jones <rjones@redhat.com> - 3.11.1-8
- Use __ocaml_requires_opts / __ocaml_provides_opts.

* Wed Dec 16 2009 Richard W.M. Jones <rjones@redhat.com> - 3.11.1-7
- Remove ocaml-find-{requires,provides}.sh from this package.  These are
  now in upstream RPM 4.8 (RHBZ#545116).
- define -> global in a few places.

* Thu Nov 05 2009 Dennis Gilmore <dennis@ausil.us> - 3.11.1-6
- include sparcv9 in the arch list

* Tue Oct 27 2009 Richard W.M. Jones <rjones@redhat.com> - 3.11.1-5
- Install ocaml.info files correctly (RHBZ#531204).

* Fri Oct 16 2009 Richard W.M. Jones <rjones@redhat.com> - 3.11.1-4
- Set includes so building the *info programs works without
  having OCaml already installed.

* Fri Oct 16 2009 Richard W.M. Jones <rjones@redhat.com> - 3.11.1-3
- Add ocamlbyteinfo and ocamlplugininfo programs from Debian.

* Sun Oct  4 2009 Richard W.M. Jones <rjones@redhat.com> - 3.11.1-2
- ocaml-find-requires.sh: Calculate runtime version using ocamlrun
  -version instead of fedora-ocaml-release file.

* Wed Sep 30 2009 Richard W.M. Jones <rjones@redhat.com> - 3.11.1-1
- OCaml 3.11.1 (this is virtually the same as the release candidate
  that we were using for Fedora 12).

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.11.1-0.rc1.2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jun  3 2009 Richard W.M. Jones <rjones@redhat.com> - 3.11.1-0.rc1.2
- Remember to upload the source this time.

* Wed Jun  3 2009 Richard W.M. Jones <rjones@redhat.com> - 3.11.1-0.rc1.1
- New upstream release candidate 3.11.1+rc1.
- Remove ocamlbuild -where patch (now upstream).

* Tue Jun  2 2009 Richard W.M. Jones <rjones@redhat.com> - 3.11.1-0.rc0.3
- Move dllgraphics.so into runtime package (RHBZ#468506).

* Tue May 26 2009 Richard W.M. Jones <rjones@redhat.com> - 3.11.1-0.rc0.2
- Backport ocamlbuild -where fix.

* Fri May 22 2009 Richard W.M. Jones <rjones@redhat.com> - 3.11.1-0.rc0.1
- 3.11.1 release candidate 0.

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.11.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Dec  4 2008 Richard W.M. Jones <rjones@redhat.com> - 3.11.0-1
- Official release of 3.11.0.

* Thu Dec  4 2008 Richard W.M. Jones <rjones@redhat.com> - 3.11.0-0.6.rc1
- Fixed sources file.

* Thu Dec  4 2008 Richard W.M. Jones <rjones@redhat.com> - 3.11.0-0.5.rc1
- New upstream version 3.11.0+rc1.

* Mon Nov 24 2008 Richard W.M. Jones <rjones@redhat.com> - 3.11.0-0.4.beta1
- Rebuild.

* Thu Nov 20 2008 Rex Dieter <rdieter@fedoraproject.org> - 3.11.0-0.3.beta1
- fix NVR to match packaging guidelines

* Thu Nov 20 2008 Richard W.M. Jones <rjones@redhat.com> - 3.11.0+beta1-2
- Fix Invalid_argument("String.index_from") with patch from upstream.

* Tue Nov 18 2008 Richard W.M. Jones <rjones@redhat.com> - 3.11.0+beta1-1
- Rebuild for major new upstream release of 3.11.0 for Fedora 11.

* Fri Aug 29 2008 Richard W.M. Jones <rjones@redhat.com> - 3.10.2-5
- Rebuild with patch fuzz.

* Mon Jun  9 2008 Richard W.M. Jones <rjones@redhat.com> - 3.10.2-4
- Add ocaml-3.11-dev12-no-executable-stack.patch (bz #450551).

* Wed Jun  4 2008 Richard W.M. Jones <rjones@redhat.com> - 3.10.2-3
- ocaml-ocamldoc provides ocamldoc (bz #449931).
- REMOVED provides of labltk, camlp4.  Those are libraries and all
  packages should now depend on ocaml-labltk / ocaml-camlp4 / -devel
  as appropriate.

* Thu May  8 2008 Richard W.M. Jones <rjones@redhat.com> - 3.10.2-2
- Pass MAP_32BIT to mmap (bz #445545).

* Mon Apr 21 2008 Richard W.M. Jones <rjones@redhat.com> - 3.10.2-1
- New upstream version 3.10.2 for Fedora 10.
- Cleaned up several rpmlint errors & warnings.

* Fri Feb 29 2008 David Woodhouse <dwmw2@infradead.org> - 3.10.1-2
- ppc64 port

* Tue Feb 12 2008 Richard W.M. Jones <rjones@redhat.com> - 3.10.1-1
- new upstream version 3.10.1

* Fri Jan  4 2008 Gerard Milmeister <gemi@bluewin.ch> - 3.10.0-8
- patch for building with tcl/tk 8.5

* Thu Sep  6 2007 Richard W.M. Jones <rjones@redhat.com> - 3.10.0-7
- Run chrpath to delete rpaths used on some of the stublibs.
- Ignore Parsetree module in dependency calculation.
- Fixed ocaml-find-{requires,provides}.sh regexp calculation so it doesn't
  over-match module names.

* Mon Sep  3 2007 Richard W.M. Jones <rjones@redhat.com> - 3.10.0-6
- ocaml-runtime provides ocaml(runtime) = 3.10.0, and
  ocaml-find-requires.sh modified so that it adds this requires
  to other packages.  Now can upgrade base ocaml packages without
  needing to rebuild everything else.

* Mon Sep  3 2007 Richard W.M. Jones <rjones@redhat.com> - 3.10.0-5
- Don't include the release number in fedora-ocaml-release file, so
  that packages built against this won't depend on the Fedora release.

* Wed Aug 29 2007 Gerard Milmeister <gemi@bluewin.ch> - 3.10.0-4
- added BR util-linux-ng

* Wed Aug 29 2007 Gerard Milmeister <gemi@bluewin.ch> - 3.10.0-3
- added BR gawk

* Tue Aug 28 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 3.10.0-2
- Rebuild for selinux ppc32 issue.

* Sat Jun  2 2007 Gerard Milmeister <gemi@bluewin.ch> - 3.10.0-1
- new version 3.10.0
- split off devel packages
- rename subpackages to use ocaml- prefix

* Thu May 24 2007 Gerard Milmeister <gemi@bluewin.ch> - 3.09.3-2
- added ocamlobjinfo

* Sat Dec  2 2006 Gerard Milmeister <gemi@bluewin.ch> - 3.09.3-1
- new version 3.09.3

* Mon Aug 28 2006 Gerard Milmeister <gemi@bluewin.ch> - 3.09.2-2
- Rebuild for FE6

* Sun Apr 30 2006 Gerard Milmeister <gemi@bluewin.ch> - 3.09.2-1
- new version 3.09.2

* Fri Feb 17 2006 Gerard Milmeister <gemi@bluewin.ch> - 3.09.1-2
- Rebuild for Fedora Extras 5

* Thu Jan  5 2006 Gerard Milmeister <gemi@bluewin.ch> - 3.09.1-1
- new version 3.09.1

* Sun Jan  1 2006 Gerard Milmeister <gemi@bluewin.ch> - 3.09.0-1
- new version 3.09.0

* Sun Sep 11 2005 Gerard Milmeister <gemi@bluewin.ch> - 3.08.4-1
- New Version 3.08.4

* Wed May 25 2005 Toshio Kuratomi <toshio-tiki-lounge.com> - 3.08.3-5
- Bump and re-release as last build failed due to rawhide syncing.

* Sun May 22 2005 Toshio Kuratomi <toshio-tiki-lounge.com> - 3.08.3-4
- Fix for gcc4 and the 32 bit assembly in otherlibs/num.
- Fix to allow compilation with RPM_OPT_FLAG defined -O level.

* Sun May 22 2005 Jeremy Katz <katzj@redhat.com> - 3.08.3-3
- rebuild on all arches

* Fri Apr  8 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Sat Mar 26 2005 Gerard Milmeister <gemi@bluewin.ch> - 3.08.3-1
- New Version 3.08.3

* Sat Feb 12 2005 Gerard Milmeister <gemi@bluewin.ch> - 0:3.08.2-2
- Added patch for removing rpath from shared libs

* Sat Feb 12 2005 Gerard Milmeister <gemi@bluewin.ch> - 0:3.08.2-1
- New Version 3.08.2

* Thu Dec 30 2004 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 0:3.07-6
- add -x11lib _prefix/X11R6/_lib to configure; fixes labltk build
  on x86_64

* Tue Dec  2 2003 Gerard Milmeister <gemi@bluewin.ch> - 0:3.07-0.fdr.5
- ocamldoc -> ocaml-ocamldoc
- ocaml-doc -> ocaml-docs

* Fri Nov 28 2003 Gerard Milmeister <gemi@bluewin.ch> - 0:3.07-0.fdr.4
- Make separate packages for labltk, camlp4, ocamldoc, emacs and documentation

* Thu Nov 27 2003 Gerard Milmeister <gemi@bluewin.ch> - 0:3.07-0.fdr.2
- Changed license tag
- Register info files
- Honor RPM_OPT_FLAGS
- New Patch

* Fri Oct 31 2003 Gerard Milmeister <gemi@bluewin.ch> - 0:3.07-0.fdr.1
- First Fedora release

* Mon Oct 13 2003 Axel Thimm <Axel.Thimm@physik.fu-berlin.de>
- Updated to 3.07.

* Wed Apr  9 2003 Axel Thimm <Axel.Thimm@physik.fu-berlin.de>
- Rebuilt for Red Hat 9.

* Tue Nov 26 2002 Axel Thimm <Axel.Thimm@physik.fu-berlin.de>
- Added _mandir/mano/* entry
