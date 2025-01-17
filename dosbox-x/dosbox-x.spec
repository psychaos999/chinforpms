%bcond_with ffmpeg

%global perms_dx %caps(cap_net_raw+ep)

%global vc_url https://github.com/joncampbell123/%{name}

Name:           dosbox-x
Version:        0.83.11
Release:        1%{?dist}

Summary:        DOS emulator for running DOS games and applications including Windows 3.x/9x

License:        GPLv2+
URL:            https://dosbox-x.com/

Source0:        %{vc_url}/archive/%{name}-v%{version}.tar.gz

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  make
BuildRequires:  desktop-file-utils
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  libappstream-glib
BuildRequires:  nasm
BuildRequires:  pkgconfig(alsa)
BuildRequires:  pkgconfig(fluidsynth)
BuildRequires:  pkgconfig(freetype2)
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(libpcap)
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(ncurses)
BuildRequires:  pkgconfig(tinfo)
BuildRequires:  pkgconfig(sdl2)
BuildRequires:  pkgconfig(SDL2_net)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xkbfile)
BuildRequires:  pkgconfig(xrandr)
BuildRequires:  pkgconfig(zlib)
%if %{with ffmpeg}
BuildRequires:  pkgconfig(libavcodec)
%endif

Requires:       fluid-soundfont-gm
Requires:       hicolor-icon-theme


%description
DOSBox-X emulates a PC necessary for running many DOS games and applications
that simply cannot be run on modern PCs and operating systems, including
Windows 3.x/9x software.


%prep
%autosetup -n %{name}-%{name}-v%{version} -p1

mv vs2015/sdl/src/cdrom _cdrom
rm -rf vs2015/{extlib,freetype,libpdcurses,libpng,pcap,sdl,sdl2,sdlnet,zlib/*.{h,c}}
mkdir -p vs2015/sdl/src/
mv _cdrom vs2015/sdl/src/cdrom

sed \
  -e '/Wconversion-null/d' \
  -e '/Wsign-promo/d' \
  -e '/Wno-int-to-void-pointer-cast/d' \
  -e '/^AC_CHECK_LIB(SDL_net,/s|^|#|' \
  -i configure.ac

./autogen.sh


%build
%configure \
  --enable-sdl2 \
  --disable-sdl \
  --disable-debug \
%if %{with ffmpeg}
  --enable-avcodec \
%endif
  --enable-core-inline \
%{nil}

%make_build


%check
make check


%install
%make_install

desktop-file-validate %{buildroot}%{_datadir}/applications/com.dosbox_x.DOSBox-X.desktop
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/com.dosbox_x.DOSBox-X.metainfo.xml


%files
%license COPYING
%doc AUTHORS CREDITS.md README.{debugger,joystick,md,video,xbrz} THANKS
%{perms_dx} %{_bindir}/%{name}
%{_datadir}/%{name}/
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/*/apps/*.*
%{_datadir}/metainfo/*.metainfo.xml


%changelog
* Wed Mar 03 2021 Phantom X <megaphantomx at hotmail dot com> - 0.83.11-1
- 0.83.11

* Sun Jan 31 2021 Phantom X <megaphantomx at hotmail dot com> - 0.83.9-1
- 0.86.9

* Fri Dec 18 2020 Phantom X <megaphantomx at hotmail dot com> - 0.83.7-1
- 0.83.8

* Sat Nov 07 2020 Phantom X <megaphantomx at hotmail dot com> - 0.83.7-1
- Initial spec
