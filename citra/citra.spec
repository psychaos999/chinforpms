%undefine _cmake_shared_libs

%global commit 8e3c7674d82df8db66e9cdf6a5d8b0e678a7f720
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20210306
%global with_snapshot 1

# Enable system boost
%bcond_with boost
# Enable ffmpeg support
%bcond_with ffmpeg
# Disable Qt build
%bcond_without qt

%global commit1 15cf3caaceb21172ea42a24e595a2eb58c3ec960
%global shortcommit1 %(c=%{commit1}; echo ${c:0:7})
%global srcname1 Catch

%global commit2 f320e7d92a33ee80ae42deef79da78cfc30868af
%global shortcommit2 %(c=%{commit2}; echo ${c:0:7})
%global srcname2 cryptopp

%global commit3 f9d84871fb6dd41c47945d649dc9017aa3762125
%global shortcommit3 %(c=%{commit3}; echo ${c:0:7})
%global srcname3 dynarmic

%global commit4 cc09f1a6798c085c325569ef466bcdcffdc266d4
%global shortcommit4 %(c=%{commit4}; echo ${c:0:7})
%global srcname4 fmt

%global commit5 1e80a47dffbda813604f0913e2ad68c7054c14e4
%global shortcommit5 %(c=%{commit5}; echo ${c:0:7})
%global srcname5 inih

%global commit6 fd69de1a1b960ec296cc67d32257b0f9e2d89ac6
%global shortcommit6 %(c=%{commit6}; echo ${c:0:7})
%global srcname6 nihstro

%global commit7 060181eaf273180d3a7e87349895bd0cb6ccbf4a
%global shortcommit7 %(c=%{commit7}; echo ${c:0:7})
%global srcname7 ext-soundtouch

%global commit8 3e032a73d7e97eb434a053391d95029eebd7e189
%global shortcommit8 %(c=%{commit8}; echo ${c:0:7})
%global srcname8 teakra

%global commit9 c306b8e5786eeeb87b8925a8af5c3bf057ff5a90
%global shortcommit9 %(c=%{commit9}; echo ${c:0:7})
%global srcname9 xbyak

%global commit10 31d9704fdcca0b68fb9656d4764fa0fb60e460c2
%global shortcommit10 %(c=%{commit9}; echo ${c:0:7})
%global srcname10 lodepng

%global commit11 36603a1e665e849d29b1735a12c0a51284a10dd0
%global shortcommit11 %(c=%{commit11}; echo ${c:0:7})
%global srcname11 ext-boost

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

%undefine _hardened_build

%global vc_url  https://github.com/citra-emu

Name:           citra
Version:        0
Release:        15%{?gver}%{?dist}
Summary:        A Nintendo 3DS Emulator

License:        GPLv2
URL:            https://citra-emu.org

%if 0%{?with_snapshot}
Source0:        %{vc_url}/%{name}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        %{vc_url}/%{name}/archive/v%{version}/%{name}-%{version}.tar.gz
%endif
Source1:        https://github.com/philsquared/%{srcname1}/archive/%{commit1}/%{srcname1}-%{shortcommit1}.tar.gz
Source2:        https://github.com/weidai11/%{srcname2}/archive/%{commit2}/%{srcname2}-%{shortcommit2}.tar.gz
Source3:        https://github.com/MerryMage/%{srcname3}/archive/%{commit3}/%{srcname3}-%{shortcommit3}.tar.gz
Source4:        https://github.com/fmtlib/%{srcname4}/archive/%{commit4}/%{srcname4}-%{shortcommit4}.tar.gz
Source5:        https://github.com/benhoyt/%{srcname5}/archive/%{commit5}/%{srcname5}-%{shortcommit5}.tar.gz
Source6:        https://github.com/neobrain/%{srcname6}/archive/%{commit6}/%{srcname6}-%{shortcommit6}.tar.gz
Source7:        %{vc_url}/%{srcname7}/archive/%{commit7}/%{srcname7}-%{shortcommit7}.tar.gz
Source8:        https://github.com/wwylele/%{srcname8}/archive/%{commit8}/%{srcname8}-%{shortcommit8}.tar.gz
Source9:        https://github.com/herumi/%{srcname9}/archive/%{commit9}/%{srcname9}-%{shortcommit9}.tar.gz
Source10:       https://github.com/lvandeve/%{srcname10}/archive/%{commit10}/%{srcname10}-%{shortcommit10}.tar.gz
%if !%{with boost}
Source11:       %{vc_url}/%{srcname11}/archive/%{commit11}/%{srcname11}-%{shortcommit11}.tar.gz
%endif

Source20:       https://api.citra-emu.org/gamedb#/compatibility_list.json

Patch0:         0001-Use-system-libraries.patch
Patch1:         0001-Disable-telemetry-initial-dialog.patch
Patch10:        %{vc_url}/%{name}/pull/5711.patch#/%{name}-gh-pr5711.patch

BuildRequires:  cmake
BuildRequires:  make
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  desktop-file-utils
%if %{with boost}
BuildRequires:  boost-devel >= 1.71.0
%else
Provides:       bundled(boost) = 0~git%{shortcommit11}
%endif
BuildRequires:  cmake(cubeb)
%if %{with ffmpeg}
BuildRequires:  pkgconfig(libavcodec)
%endif
BuildRequires:  pkgconfig(libenet)
BuildRequires:  pkgconfig(libzstd)
BuildRequires:  pkgconfig(nlohmann_json) >= 3.9.0
BuildRequires:  pkgconfig(sdl2)
%if %{with qt}
BuildRequires:  cmake(Qt5Core)
BuildRequires:  cmake(Qt5Gui)
BuildRequires:  cmake(Qt5LinguistTools)
BuildRequires:  cmake(Qt5Multimedia)
BuildRequires:  cmake(Qt5Widgets)
%endif

BuildRequires:  hicolor-icon-theme
BuildRequires:  shared-mime-info

Provides:       bundled(catch2) = 0~git%{shortcommit1}
Provides:       bundled(cryptopp) = 0~git%{shortcommit2}
Provides:       bundled(dynarmic) = 0~git%{shortcommit3}
Provides:       bundled(fmt) = 0~git%{shortcommit4}
Provides:       bundled(inih) = 0~git%{shortcommit5}
Provides:       bundled(nihstro) = 0~git%{shortcommit6}
Provides:       bundled(soundtouch) = 0~git%{shortcommit7}
Provides:       bundled(teakra) = 0~git%{shortcommit8}
Provides:       bundled(xbyak) = 0~git%{shortcommit9}
Provides:       bundled(lodepng) = 0~git%{shortcommit10}


%description
Citra is an experimental open-source Nintendo 3DS emulator/debugger
written in C++.


%package qt
Summary:        A Nintendo 3DS Emulator (Qt frontend)
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       hicolor-icon-theme

%description qt
Citra is an experimental open-source Nintendo 3DS emulator/debugger
written in C++.

This is the Qt frontend.


%prep
%if 0%{?with_snapshot}
%autosetup -n %{name}-%{commit} -p1
%else
%autosetup -n %{name}-%{version} -p1
%endif

tar -xf %{S:1} -C externals/catch --strip-components 1
tar -xf %{S:2} -C externals/cryptopp/cryptopp --strip-components 1
tar -xf %{S:3} -C externals/dynarmic --strip-components 1
tar -xf %{S:4} -C externals/fmt --strip-components 1
tar -xf %{S:5} -C externals/inih/inih --strip-components 1
tar -xf %{S:6} -C externals/nihstro --strip-components 1
tar -xf %{S:7} -C externals/soundtouch --strip-components 1
tar -xf %{S:8} -C externals/teakra --strip-components 1
tar -xf %{S:9} -C externals/xbyak --strip-components 1
tar -xf %{S:10} -C externals/lodepng/lodepng --strip-components 1
%if !%{with boost}
tar -xf %{S:11} -C externals/boost --strip-components 1
%endif

rm -f externals/json/json.hpp
ln -sf %{_includedir}/nlohmann/json.hpp \
  externals/json/json.hpp

sed -e '/ENABLE_WEB_SERVICE/s|ON|OFF|g' -i CMakeLists.txt

sed -e 's|-pedantic-errors||g' -i externals/fmt/CMakeLists.txt

sed \
  -e 's/-Wfatal-errors\b//g' \
  -e '/-pedantic-errors/d' \
  -i externals/teakra/CMakeLists.txt externals/dynarmic/CMakeLists.txt

sed -e '/^#include <exception>/a#include <system_error>' \
  -i externals/teakra/src/interpreter.h

%if 0%{?with_snapshot}
  sed \
    -e 's|@GIT_REV@|%{commit}|g' \
    -e 's|@GIT_BRANCH@|HEAD|g' \
    -e 's|@GIT_DESC@|%{shortcommit}|g' \
    -e 's|@BUILD_FULLNAME@|chinforpms %{version}-%{release}|g' \
    -i src/common/scm_rev.cpp.in
%endif

%build
# Disable LTO. Crash.
%global _lto_cflags %{nil}

%global optflags %(echo "%{optflags}" | sed -e 's/-Wp,-D_GLIBCXX_ASSERTIONS//')
export LDFLAGS="%{build_ldflags} -Wl,-z,relro -Wl,-z,now"

mkdir -p dist/compatibility_list/
cp %{S:20} dist/compatibility_list/

%if 0%{?with_snapshot}
export CI=true
export TRAVIS=true
export TRAVIS_REPO_SLUG=%{name}/%{name}-nightly
export TRAVIS_TAG="%{version}-%{release}"
%endif

%cmake \
%if %{with qt}
  -DENABLE_QT_TRANSLATION:BOOL=ON \
%else
  ENABLE_QT:BOOL=OFF \
%endif
%if %{with boost}
  -DUSE_SYSTEM_BOOST:BOOL=ON \
%endif
%if %{with ffmpeg}
  -DENABLE_FFMPEG:BOOL=ON \
%endif
  -DENABLE_WEB_SERVICE:BOOL=OFF \
  -DENABLE_COMPATIBILITY_LIST_DOWNLOAD:BOOL=ON \
%{nil}

%cmake_build


%install
%cmake_install

desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop


%files
%license license.txt
%doc README.md
%{_bindir}/%{name}
%{_bindir}/%{name}-room
%{_mandir}/man6/%{name}.6*


%if %{with qt}
%files qt
%{_bindir}/%{name}-qt
%license license.txt
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/*
%{_datadir}/mime/packages/%{name}.xml
%{_mandir}/man6/%{name}-qt.6*
%endif


%changelog
* Wed Mar 17 2021 Phantom X <megaphantomx at hotmail dot com> - 0-15.20210306git8e3c767
- Last snapshot

* Fri Feb 12 2021 Phantom X <megaphantomx at hotmail dot com> - 0-14.20210212gite6c479f
- Update

* Sun Jan 17 2021 Phantom X <megaphantomx at hotmail dot com> - 0-13.20210109git7c6d790
- Update

* Fri Oct 02 2020 Phantom X <megaphantomx at hotmail dot com> - 0-12.20201001gitaced133
- Bump

* Sun Sep 06 2020 Phantom X <megaphantomx at hotmail dot com> - 0-11.20200905git316a649
- New snapshot

* Sun Jul 19 2020 Phantom X <megaphantomx at hotmail dot com> - 0-10.20200714gitd88d220
- Bump

* Sun Jun 21 2020 Phantom X <megaphantomx at hotmail dot com> - 0-9.20200620git372c653
- New snapshot

* Sun May 10 2020 Phantom X <megaphantomx at bol dot com dot br> - 0-8.20200509git8d27b07
- Bump
- ext-boost

* Sat Mar 21 2020 Phantom X <megaphantomx at bol dot com dot br> - 0-7.20200321git8722b97
- New snapshot

* Sun Mar 15 2020 Phantom X <megaphantomx at bol dot com dot br> - 0-6.20200312gitad3c464
- Bump

* Thu Feb 06 2020 Phantom X <megaphantomx at bol dot com dot br> - 0-5.20200204git821a35b
- New snapshot
- libzstd

* Sun Jan 05 2020 Phantom X <megaphantomx at bol dot com dot br> - 0-4.20200101git01686f7
- New snapshot
- lodepng

* Sat Sep 21 2019 Phantom X <megaphantomx at bol dot com dot br> - 0-3.20190921git223bfc9
- New snapshot

* Wed Apr 24 2019 Phantom X <megaphantomx at bol dot com dot br> - 0-2.20190423gitb9e51f0
- Disable telemetry initial dialog
- Update version strings

* Tue Apr 23 2019 Phantom X <megaphantomx at bol dot com dot br> - 0-1.20190423gitb9e51f0
- Initial spec
