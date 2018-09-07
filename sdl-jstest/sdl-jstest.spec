%global gitcommitid aafbdb1ed3e687583037ba55ae88b1210d6ce98b
%global shortcommit %(c=%{gitcommitid}; echo ${c:0:7})
%global date 20180715
%global with_snapshot 1

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

Name:           sdl-jstest
Version:        0.2.1
Release:        0.1%{?gver}%{?dist}
Summary:        Simple SDL joystick test application for the console

License:        GPLv3
URL:            https://gitlab.com/sdl-jstest/sdl-jstest

%if 0%{?with_snapshot}
Source0:        %{url}/-/archive/%{gitcommitid}/%{name}-%{gitcommitid}.tar.bz2#/%{name}-%{shortcommit}.tar.bz2
%else
Source0:        %{url}/-/archive/%{name}-%{version}.tar.gz#/%{name}-%{version}.tar.bz2
%endif

Patch0:         %{name}-system-sdl_db.patch

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  pkgconfig(ncurses)
BuildRequires:  pkgconfig(sdl2)
Requires:       sdl_gamecontrollerdb


%description
sdl2-jstest is a simple program that lets you find out how many
joysticks SDL2 detected on your system, how many axes, buttons,
hats and balls they have each. They also lets you test the joysticks
by displaying the events they send or by displaying their current
button, axis, hat or ball state. sdl-jstest is especially useful if
you want to test your SDL_LINUX_JOYSTICK configuration.


%prep
%if 0%{?with_snapshot}
%autosetup -n %{name}-%{gitcommitid} -p1
%else
%autosetup -n %{name}-%{version} -p1
%endif

%if 0%{?with_snapshot}
sed -i \
  -e '/Git REQUIRED/d' \
  -e "/COMMAND/s|\${GIT_EXECUTABLE} describe.*$|echo \"%{version}-%{release}\"|g" \
  -e "/COMMAND/s|\${GIT_EXECUTABLE} log.*$|echo \"%{date}\"|g" \
  CMakeLists.txt
%endif

sed \
  -e '/AddMappingsFromFile/s|"gamecontrollerdb.txt"|"%{_datadir}/SDL_GameControllerDB/gamecontrollerdb.txt"|g' \
  -i sdl2-jstest.c


%build

mkdir -p build
pushd build

%cmake .. \
  -DBUILD_SDL_JSTEST:BOOL=OFF \
  -DCMAKE_VERBOSE_MAKEFILE:BOOL=ON

%make_build

popd

%install
%make_install -C build


%files
%license LICENSE.txt
%doc README.md
%{_bindir}/sdl*-jstest
%{_mandir}/man1/sdl*-jstest.1*
%{_metainfodir}/sdl*-jstest.appdata.xml


%changelog
* Thu Sep 06 2018 Phantom X <megaphantomx at bol dot com dot br> - 0.2.1-0.1.20180715gitaafbdb1
- Initial spec
