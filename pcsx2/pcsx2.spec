%global commit 33571dda4239a91e52bf988d2e02be1d92a97750
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20190818
%global with_snapshot 1

%global sanitize 0

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

Name:           pcsx2
Version:        1.5.0
Release:        103%{?gver}%{?dist}
Summary:        A Sony Playstation2 emulator

License:        GPLv3
URL:            https://github.com/PCSX2/pcsx2

%if 0%{sanitize}
%if 0%{?with_snapshot}
Source0:        %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz
%endif #{?with_snapshot}
%else
%if 0%{?with_snapshot}
Source0:        %{name}-%{shortcommit}.tar.xz
%else
Source0:        %{name}-%{version}.tar.xz
%endif
%endif
Source1:        Makefile

# PCSX2 does not support running as a 64 bit application.
# http://code.google.com/p/pcsx2/wiki/ChrootAnd64bStatusLinux
ExclusiveArch:  i686

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  desktop-file-utils
BuildRequires:  cmake
BuildRequires:  pkgconfig(alsa)
BuildRequires:  pkgconfig(bzip2)
BuildRequires:  pkgconfig(freetype2)
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(glesv2)
BuildRequires:  pkgconfig(glew)
BuildRequires:  pkgconfig(glu)
BuildRequires:  pkgconfig(gtk+-2.0)
BuildRequires:  pkgconfig(ice)
BuildRequires:  pkgconfig(liblzma)
BuildRequires:  pkgconfig(libsparsehash)
BuildRequires:  pkgconfig(libudev)
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(harfbuzz)
BuildRequires:  pkgconfig(portaudio-2.0)
BuildRequires:  pkgconfig(sdl2)
BuildRequires:  pkgconfig(soundtouch)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xrandr)
BuildRequires:  pkgconfig(zlib)
# use SDL that depends wxGTK
BuildRequires:  compat-wxGTK3-gtk2-devel
BuildRequires:  gettext
BuildRequires:  libaio-devel
BuildRequires:  libpcap-devel
BuildRequires:  perl-interpreter

Requires:       joystick
Requires:       hicolor-icon-theme


%description
A Playstation 2 emulator. Requires a dump of a real PS2 BIOS (not included)
WARNING: It requires a CPU with SSE2 instructions. If your CPU does not
support this instruction set, it does not have enough horsepower to run
this emulator anyway.

%prep
%if 0%{?with_snapshot}
%autosetup -n %{name}-%{commit} -p1
%else
%autosetup -p1
%endif

%if 0%{sanitize}
  rm -rf 3rdparty
  rm -rf fps2bios
  rm -rf tools
  for plugin in \
    CDVDiso CDVDisoEFP CDVDlinuz CDVDolio CDVDpeops dev9ghzdrk PeopsSPU2 \
    SSSPSXPAD USBqemu xpad zerogs zerospu2
  do
    rm -rf plugins/$plugin
  done
  rm -rf unfree
  rm -rf plugins/GSdx/baseclasses
  rm -f  plugins/zzogl-pg/opengl/Win32/aviUtil.h
  rm -f common/src/Utilities/x86/MemcpyFast.cpp
  rm -rf .git
%endif

# To remove executable bits from man, doc and icon files
chmod -x pcsx2/Docs/GPL.txt pcsx2/Docs/License.txt pcsx2/Docs/readme-Docs.txt pcsx2/Docs/PCSX2_FAQ.doc pcsx2/Docs/PCSX2_Readme.doc bin/docs/PCSX2.1 linux_various/PCSX2.xpm

# Remove DOS encoding errors in txt files
sed -i 's/\r//' pcsx2/Docs/GPL.txt
sed -i 's/\r//' pcsx2/Docs/License.txt

#Remove fedora incompatible values
sed -i 's/@PCSX2_MENU_CATEGORIES@/Game;Emulator;GTK;/g' linux_various/PCSX2.desktop.in

%if 0%{?with_snapshot}
sed -i \
  -e '/PCSX2_GIT_REV/s| ""| "%{shortcommit}"|g' \
  cmake/Pcsx2Utils.cmake
%endif


%build

# pcsx2 contains cflags that override Fedora cflags, however
# a conservative approach has been taken because to quote upsteam "PCSX2 is not
# an ordinary sofware. Most of the code executed are self-generated by PCSX2
# itself (aka dynamic recompiler/virtual machine). That means 1/ gcc flags
# have no much impact on speed 2/ some gcc flags (used to) crash PCSX2"
# Extensive testing will is therefore needed. See rpmfusion bug #2455      

%cmake . \
  -DCMAKE_VERBOSE_MAKEFILE:BOOL=ON \
  -DDISABLE_BUILD_DATE=TRUE \
  -DPACKAGE_MODE=TRUE \
  -DBUILD_REPLAY_LOADERS=FALSE \
  -DXDG_STD=TRUE \
  -DGLSL_API=TRUE \
  -DPLUGIN_DIR=%{_libdir}/pcsx2 \
  -DGAMEINDEX_DIR=%{_datadir}/pcsx2 \
  -DCMAKE_BUILD_STRIP=FALSE \
  -DGTK3_API=FALSE \
  -DWX28_API=FALSE \
  -DSDL2_API=TRUE \
  -DEXTRA_PLUGINS=FALSE \
  -DDISABLE_ADVANCE_SIMD=TRUE \
  -DOpenGL_GL_PREFERENCE=GLVND \
  -DCMAKE_BUILD_TYPE=Release \
%{nil}

%make_build


%install
%make_install

# strip extra copies of pdf files, which are now in /doc/pcsx2
rm -rf %{buildroot}/usr/share/doc/PCSX2

# Install icon
mkdir -p %{buildroot}/%{_datadir}/icons/hicolor/128x128/apps/
install -pm 0644 linux_various/PCSX2.xpm %{buildroot}/%{_datadir}/icons/hicolor/128x128/apps/

# Install Desktop file
mv linux_various/PCSX2.desktop.in -f linux_various/PCSX2.desktop
desktop-file-install \
  --dir=%{buildroot}/%{_datadir}/applications \
  linux_various/PCSX2.desktop

#strip extra copy of icon file, Wrong place for fedora
rm -rf %{buildroot}/usr/share/pixmaps

# Install man page
mkdir -p %{buildroot}/%{_mandir}/man1
install -p -D -m 644 bin/docs/PCSX2.1 %{buildroot}/%{_mandir}/man1

%find_lang pcsx2_Iconized
%find_lang pcsx2_Main


%files -f pcsx2_Iconized.lang -f pcsx2_Main.lang
%doc bin/docs/PCSX2_Readme.pdf bin/docs/PCSX2_FAQ.pdf
%{_bindir}/PCSX2
%{_bindir}/PCSX2-linux.sh
%{_libdir}/pcsx2/
%{_datadir}/applications/PCSX2.desktop
%{_datadir}/icons/hicolor/128x128/apps/*.xpm
%{_mandir}/man1/PCSX2.*
%{_datadir}/pcsx2/


%changelog
* Sun Aug 18 2019 Phantom X <megaphantomx at bol dot com dot br> - 1.5.0-103.20190818git33571dd
- New snapshot

* Wed May 22 2019 Phantom X <megaphantomx at bol dot com dot br> - 1.5.0-102.20190517gitc6fcf0a
- New snapshot

* Fri May 03 2019 Phantom X <megaphantomx at bol dot com dot br> - 1.5.0-101.20190502git079baae
- New snapshot

* Sat Apr 13 2019 Phantom X <megaphantomx at bol dot com dot br> - 1.5.0-100.20190411git163fd2b
- chinforpms
- New snapshot
- Make build on Fedora > 30
- Makefile to sanitize

* Tue Mar 05 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.4-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Aug 19 2018 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.4-11
- Rebuilt for Fedora 29 Mass Rebuild binutils issue

* Sat Jul 28 2018 Sérgio Basto <sergio@serjux.com> - 1.4-10
- Try fix rfbz #4962
- Use the same SDL that wxGTK depends on (F27 SDL, F28 SDL2)

* Fri Jul 27 2018 RPM Fusion Release Engineering <sergio@serjux.com> - 1.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun May 20 2018 Sérgio Basto <sergio@serjux.com> - 1.4-8
- Try fix f27 (#4775) use compat-wxGTK3-gtk2-devel
- Add BR xz-devel to dectect LibLZMA
- Remove manually-specified variables were not used by the project
- Add DISABLE_ADVANCE_SIMD=TRUE, recomended by upstream
- OpenGL_GL_PREFERENCE=GLVND to not use legacy OpenGL

* Fri Mar 02 2018 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 1.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan 30 2018 Sérgio Basto <sergio@serjux.com> - 1.4-6
- Rebuilt to fix core dump with wxWindow

* Sun Oct 08 2017 Sérgio Basto <sergio@serjux.com> - 1.4-5
- Rebuild for soundtouch 2.0.0
- Just enable compat-wxGTK3-gtk2, pcsx2 fails to detect wxGTK3
  therefore SDL2 also is disabled, intructions on
  https://github.com/PCSX2/pcsx2/wiki/Installing-on-Linux
- Enable GLSL_API and AVX
- Fix Perl builroot changes.

* Thu Aug 31 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 1.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Mar 26 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 1.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jul 14 2016 Sérgio Basto <sergio@serjux.com> - 1.4-2
- Add gcc6 patch

* Thu Feb 11 2016 Giles Birchley <gbirchley@blueyonder.co.uk> -1.4-1
- Build for new release 1.4
- Drop patch pcsx2-1.3.1_fedora_cflags_opts.diff - cflag options now streamlined upstream
- Add dependency for lzma-devel
- Add dependency for libICE-devel
- Remove dependency for Cg
- Remove dependency for libjpeg-turbo-devel
- Remove dependency for package glew-devel
- Add build option to retain WxWidget 2.8 -DWX28_API=TRUE
- Add build option -DGTK3_API=FALSE
- Add build option -DSDL2_API=FALSE
- Add build option -DDISABLE_ADVANCE_SIMD=TRUE
- For now, avoided specifying crosscompile (-DCMAKE_TOOLCHAIN_FILE=cmake/linux-compiler-i386-multilib.cmake) as not sure of rpmfusion guideline on this
- Binary name has been altered to PCSX2 upstream; renamed PCSX2.desktop.in, PCSX2.xpm and PCSX2.1
- Added new launcher script PCSX2-linux.sh

* Tue Feb 04 2014 Giles Birchley <gbirchey@blueyonder.co.uk> -1.2.1-1
- Updated source to 1.2.1
- Updated patch1 permissions
- Source required modification to remove copyrighted files - added Source1

* Tue Feb 04 2014 Giles Birchley <gbirchey@blueyonder.co.uk> -1.2.0-1
- Updated source to 1.2
- Updated patch1
- Source required modification to remove copyrighted files - added Source1

* Sat Jul 27 2013 Giles Birchley <gbirchey@blueyonder.co.uk> - 1.1.0-5
- made overlooked change suggested in rpmfusion review (#2455)
- changed requires from libGL-devel/libGLU-devel instead of mesa-libGL-devel

* Sun Jun 30 2013 Giles Birchley <gbirchey@blueyonder.co.uk> - 1.1.0-4
- made some minor changes suggested in rpmfusion review (#2455)
- removed backslash in cmake command
- removed pcsx2-1.1.0-fedora_cflags.diff
- replaced patch with pcsx2-1.1.0-fedora_cflags_opts.diff

* Tue Jun 25 2013 Giles Birchley <gbirchey@blueyonder.co.uk> - 1.1.0-3
- made some minor changes suggested in rpmfusion review (#2455)
- fix URL

* Tue Jun 25 2013 Giles Birchley <gbirchey@blueyonder.co.uk> - 1.1.0-2
- made some minor changes suggested in rpmfusion review (#2455):
- changed icon install permissions
- changed URL
- changed description line length
- reintroduced %%{version} macro to source0
- removed extra backslash from %%cmake
- changed line indentations so all are single space
- removed -DDOC_DIR from %%cmake
- removed extraneous remove lines

* Sun Jun 09 2013 Giles Birchley <gbirchey@blueyonder.co.uk> - 1.1.0-1
- changes following rpmfusion review (#2455).
- removed Group tag.
- updated source to v1.1 (linux fixes) 
- removed pcsx2-1.0.0_helpfile.diff (no longer needed).
- removed pcsx2-1.0.0_fedora_cmake.diff (Fedora<16 is no longer supported).
- removed pcsx2-1.1.0_fedora_gcc.diff as this patch is now applied in 1.1.0 source
- added Requires: hicolor-icon-theme (icons in %%{_datadir}/icons/hicolor/).
- added BuildRequires: libaio-devel (needed for 1.1.0).
- added warning about SSE2 to %%description.
- comment about 64 bit status shortened.
- version from names of docs removed (unversioned in 1.1.0).
- fixed omissions in pcsx2.xpm shebang (fix rpmlint error)
- Use %%{_docdir} instead of %%{_defaultdocdir}.
- removed some docs that were either misplaced or should not be packaged.
- removed specification of CMAKE_INSTALL_PREFIX and CMAKE_VERBOSE_MAKEFILE (%%cmake macro already sets them).
- moved %%find_lang macro to end of %%install.
- moved shell invocation to line following %%post %%postun (fix rpmlint error)

* Mon May 27 2013 Giles Birchley <gbirchey@blueyonder.co.uk> - 1.0.0-2
- further changes to comply with rpmfusion review (#2455):
- libGL-devel/libGLU-devel instead of mesa-libGL-devel
- Remove BuildRequires: libCg (redundant with Cg)
- Use %%{_prefix} instead of /usr for CMAKE install prefix
- add Gregory Hainaut's patch to fix issue with gcc 4.8, for Fedora 19 build
- Changed cmake option of DBUILD_REPLAY_LOADERS to false and changed %%files accrdingly

* Tue Mar 05 2013 Giles Birchley <gbirchey@blueyonder.co.uk>
- bleeding edge build, altered package name
- added pcsx2 as a conflict

* Mon Oct 15 2012 Giles Birchley <gbirchey@blueyonder.co.uk> - 1.0.0-1
- Build of official 1.0.0 Release
- Significant modifications to script to comply with Fedora/RPMFusion packaging requirements
- Removed redundant BuildRequires
- Added upstream source
- Added Patch to make CFLAGS compliant
- Changed DCMAKE_BUILD_STRIP to FALSE to allow rpm debug package to be created
- Changed document destination in cmake by specifying DDOC_DIR=
- Changed language detection
- Changed icon and desktop file installation

* Tue Aug 09 2011 Danger Boy <Danger[dot] Boy [at]necac.tv.idl> - 0.9.8.4851-1
- initial build
