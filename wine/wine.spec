%global commit f2058389add08357910e736aab256d15cebb17e9
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20191106
%global with_snapshot 0

# Compiling the preloader fails with hardening enabled
%undefine _hardened_build

%ifarch %{ix86} x86_64
%global wine_mingw 1
# Package mingw files with debuginfo
%global with_debug 0
%endif
%global no64bit   0
%global winegecko 2.47
%global winemono  4.9.4
%global _default_patch_fuzz 2

%global libext .so
%if 0%{?wine_mingw}
%global libext %{nil}
%endif

%global wineacm acm%{?libext}
%global winecpl cpl%{?libext}
%global winedll dll%{?libext}
%global winedll16 dll16%{?libext}
%global winedrv drv%{?libext}
%global winedrv16 drv16%{?libext}
%global wineexe exe%{?libext}
%global wineexe16 exe16%{?libext}
%global winemod16 mod16%{?libext}
%global wineocx ocx%{?libext}
%global winesys sys%{?libext}
%global winetlb tlb%{?libext}
%global winevxd vxd%{?libext}

# build with staging-patches, see:  https://wine-staging.com/
# uncomment to enable; comment-out to disable.
%global wine_staging 1
%global wine_stagingver 4.19
%if 0%(echo %{wine_stagingver} | grep -q \\. ; echo $?) == 0
%global strel v
%global stpkgver %{wine_stagingver}
%else
%global stpkgver %(c=%{wine_stagingver}; echo ${c:0:7})
%endif
%global tkg_id 2a80677c9da0da3c450732bad55f03ffb036ddeb
%global tkg_url https://github.com/Tk-Glitch/PKGBUILDS/raw/%{tkg_id}/wine-tkg-git/wine-tkg-patches

%global gtk3 0
# Broken
%global pba 0

# proton FS hack
%global wine_staging_opts -W winex11.drv-mouse-coorrds -W winex11-MWM_Decorations

%global whq_url  https://source.winehq.org/git/wine.git/patch
%global valve_url https://github.com/ValveSoftware/wine

%global staging_banner Chinforpms Staging

# binfmt macros for RHEL
%if 0%{?rhel} == 7
%global _binfmtdir /usr/lib/binfmt.d
%global binfmt_apply() \
/usr/lib/systemd/systemd-binfmt  %{?*} >/dev/null 2>&1 || : \
%{nil}
%endif

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

Name:           wine
# If rc, use "~" instead "-", as ~rc1
Version:        4.19
Release:        104%{?gver}%{?dist}
Summary:        A compatibility layer for windows applications

Epoch:          1

License:        LGPLv2+
URL:            http://www.winehq.org/

%global ver     %{lua:ver = string.gsub(rpm.expand("%{version}"), "~", "-"); print(ver)}
%global vermajor %(echo %{ver} | cut -d. -f1)
%if "%(echo %{ver} | cut -d. -f2 | cut -d- -f1 )" == "0"
%global verx 1
%endif
%if 0%{?with_snapshot}
Source0:        https://github.com/wine-mirror/%{name}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        https://dl.winehq.org/wine/source/%{vermajor}.%{?verx:0}%{!?verx:x}/wine-%{ver}.tar.xz
Source10:       https://dl.winehq.org/wine/source/%{vermajor}.%{?verx:0}%{!?verx:x}/wine-%{ver}.tar.xz.sign
%endif

Source1:        wine.init
Source2:        wine.systemd
Source3:        wine-README-Fedora
Source4:        wine-32.conf
Source5:        wine-64.conf
Source6:        wine-README-chinforpms

# desktop files
Source100:      wine-notepad.desktop
Source101:      wine-regedit.desktop
Source102:      wine-uninstaller.desktop
Source103:      wine-winecfg.desktop
Source104:      wine-winefile.desktop
Source105:      wine-winemine.desktop
Source106:      wine-winhelp.desktop
Source107:      wine-wineboot.desktop
Source108:      wine-wordpad.desktop
Source109:      wine-oleview.desktop
Source110:      wine-iexplore.desktop
Source111:      wine-inetcpl.desktop
Source112:      wine-joycpl.desktop
Source113:      wine-taskmgr.desktop

# build fixes

# wine bugs/upstream/reverts
#Patch???:      %%{whq_url}/commit#/%%{name}-whq-commit.patch
%if 0%{?wine_staging}
Patch100:       %{whq_url}/81f8b6e8c215dc04a19438e4369fcba8f7f4f333#/%{name}-whq-81f8b6e.patch
Patch101:       %{whq_url}/6dbb153ede48e77a87dddf37e5276276a701c5c3#/%{name}-whq-6dbb153.patch
Patch102:       %{whq_url}/9ae8da6bb4a8f66d55975fa0f14e5e413756d324#/%{name}-whq-9ae8da6.patch
Patch103:       %{whq_url}/de94cfa775f9f41d1d65cbd8e7bf861cd7f9a871#/%{name}-whq-de94cfa.patch
Patch104:       %{whq_url}/413aad39135b0b0f8255500b85fcc05337a5f138#/%{name}-whq-413aad3.patch
Patch105:       %{whq_url}/1b3fa021909fcb13d1517a8df0b84b6a225e6b98#/%{name}-whq-1b3fa02.patch
Patch106:       %{whq_url}/0b2e65f53aeb4fbda660828ad06bff554fccb1d5#/%{name}-whq-0b2e65f.patch
Patch107:       %{whq_url}/0e183cc3c0d3b6f89f79047cdd71c389afc75073#/%{name}-whq-0e183cc.patch
Patch108:       %{whq_url}/6796cd8ac4a3a03d7af3dd2139c12c53b984a089#/%{name}-whq-6796cd8.patch
Patch109:       %{whq_url}/aef11864a47a33830eca086de8bf337ee9b5114a#/%{name}-whq-aef1186.patch
Patch110:       %{whq_url}/1fddf230ffff2b0946f6b9ae13648b454785e23e#/%{name}-whq-1fddf23.patch
Patch111:       %{whq_url}/b06d272d635d30f570b440da2308b53fcc43c7e9#/%{name}-whq-b06d272.patch

# https://bugs.winehq.org/show_bug.cgi?id=48032
Patch120:       %{name}-bug48032.patch
%endif

# desktop dir
Source200:      wine.menu
Source201:      wine.directory

# mime types
Source300:      wine-mime-msi.desktop


# smooth tahoma (#693180)
# disable embedded bitmaps
Source501:      wine-tahoma.conf
# and provide a readme
Source502:      wine-README-tahoma

Patch511:       wine-cjk.patch
Patch599:       0003-winemenubuilder-silence-an-err.patch

%if 0%{?wine_staging}
# wine staging patches for wine-staging
Source900:      https://github.com/wine-staging/wine-staging/archive/%{?strel}%{wine_stagingver}/wine-staging-%{stpkgver}.tar.gz

# https://github.com/Tk-Glitch/PKGBUILDS/wine-tkg-git/wine-tkg-patches
Patch700:       %{tkg_url}/proton/use_clock_monotonic.patch#/%{name}-tkg-use_clock_monotonic.patch
Patch701:       %{tkg_url}/proton/use_clock_monotonic-2.patch#/%{name}-tkg-use_clock_monotonic-2.patch
Patch702:       %{tkg_url}/proton/FS_bypass_compositor.patch#/%{name}-tkg-FS_bypass_compositor.patch
Patch703:       %{tkg_url}/misc/childwindow.patch#/%{name}-tkg-childwindow.patch
Patch704:       %{tkg_url}/misc/legacy/steam.patch#/%{name}-tkg-steam.patch
Patch705:       %{tkg_url}/misc/CSMT-toggle.patch#/%{name}-tkg-CSMT-toggle.patch

Patch720:       %{tkg_url}/proton/fsync-staging.patch#/%{name}-tkg-fsync-staging.patch
Patch721:       %{tkg_url}/proton/fsync-staging-no_alloc_handle.patch#/%{name}-tkg-fsync-staging-no_alloc_handle.patch
Patch722:       %{tkg_url}/proton/valve_proton_fullscreen_hack-staging.patch#/%{name}-tkg-valve_proton_fullscreen_hack-staging.patch
Patch723:       %{tkg_url}/proton-tkg-specific/winevulkan-1.1.113-proton.patch#/%{name}-tkg-winevulkan-1.1.113-proton.patch
Patch724:       %{tkg_url}/proton/LAA-staging.patch#/%{name}-tkg-LAA-staging.patch
Patch725:       %{tkg_url}/proton/proton_mf_hacks.patch#/%{name}-tkg-proton_mf_hacks.patch
Patch726:       %{tkg_url}/misc/enable_stg_shared_mem_def.patch#/%{name}-tkg-enable_stg_shared_mem_def.patch

Patch800:       revert-grab-fullscreen.patch
Patch801:       %{valve_url}/commit/9cf81304c03046cb337d8b7275af600e39373702.patch#/%{name}-valve-9cf8130.patch
Patch802:       %{valve_url}/commit/561975d6da534cfe608d7c4068387e734c32b77c.patch#/%{name}-valve-561975d.patch
Patch803:       wine-xaudio2-pulseaudio-app-name.patch

%if 0%{?pba}
# acomminos PBA patches
Source1001:     wine-README-pba
Patch1000:      %{tkg_url}/PBA/PBA317+.patch#/%{name}-tkg-PBA317+.patch
%endif

# Patch the patch
Patch5000:      0001-chinforpms-message.patch

%endif

%if !0%{?no64bit}
ExclusiveArch:  %{ix86} x86_64 %{arm} aarch64
%else
ExclusiveArch:  %{ix86} %{arm}
%endif

BuildRequires:  bison
BuildRequires:  flex
BuildRequires:  autoconf
%ifarch aarch64
BuildRequires:  clang >= 5.0
%else
BuildRequires:  gcc
%endif
%if 0%{?wine_mingw}
%ifarch %{ix86} x86_64
BuildRequires:  mingw32-gcc
BuildRequires:  mingw64-gcc
%endif
%endif
BuildRequires:  chrpath
BuildRequires:  desktop-file-utils
BuildRequires:  fontforge
BuildRequires:  icoutils
BuildRequires:  perl-generators
BuildRequires:  pkgconfig(alsa)
BuildRequires:  cups-devel
BuildRequires:  pkgconfig(dbus-1)
BuildRequires:  pkgconfig(faudio)
BuildRequires:  pkgconfig(fontconfig)
BuildRequires:  pkgconfig(freeglut)
BuildRequires:  pkgconfig(freetype2)
BuildRequires:  fontpackages-devel
BuildRequires:  gettext-devel
BuildRequires:  giflib-devel
BuildRequires:  gsm-devel
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(glu)
BuildRequires:  pkgconfig(gnutls)
BuildRequires:  pkgconfig(gstreamer-1.0)
BuildRequires:  pkgconfig(gstreamer-audio-1.0)
BuildRequires:  pkgconfig(gstreamer-video-1.0)
BuildRequires:  pkgconfig(krb5)
BuildRequires:  pkgconfig(lcms2)
BuildRequires:  pkgconfig(libgphoto2)
BuildRequires:  libieee1284-devel
BuildRequires:  pkgconfig(libjpeg)
BuildRequires:  pkgconfig(libmpg123)
BuildRequires:  libpcap-devel
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(libpulse)
BuildRequires:  pkgconfig(librsvg-2.0)
BuildRequires:  librsvg2
BuildRequires:  librsvg2-tools
BuildRequires:  libstdc++-devel
BuildRequires:  pkgconfig(libtiff-4)
BuildRequires:  pkgconfig(libusb)
BuildRequires:  pkgconfig(libv4l2)
BuildRequires:  pkgconfig(libvkd3d)
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(libxslt)
BuildRequires:  pkgconfig(ncurses)
BuildRequires:  pkgconfig(netapi)
BuildRequires:  pkgconfig(ocl-icd)
BuildRequires:  pkgconfig(odbc)
BuildRequires:  pkgconfig(openal)
BuildRequires:  opencl-headers
BuildRequires:  openldap-devel
BuildRequires:  pkgconfig(osmesa)
BuildRequires:  pkgconfig(sane-backends)
BuildRequires:  pkgconfig(sdl2)
BuildRequires:  pkgconfig(systemd)
BuildRequires:  vulkan-devel
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xcomposite)
BuildRequires:  pkgconfig(xcursor)
BuildRequires:  pkgconfig(xext)
BuildRequires:  pkgconfig(xi)
BuildRequires:  pkgconfig(xinerama)
BuildRequires:  pkgconfig(xmu)
BuildRequires:  pkgconfig(xrandr)
BuildRequires:  pkgconfig(xrender)
BuildRequires:  pkgconfig(xxf86dga)
BuildRequires:  pkgconfig(xxf86vm)
BuildRequires:  pkgconfig(zlib)

# Silverlight DRM-stuff needs XATTR enabled.
%if 0%{?wine_staging}
%if 0%{?gtk3}
BuildRequires:  pkgconfig(gtk+-3.0)
%endif
BuildRequires:  pkgconfig(libattr)
BuildRequires:  pkgconfig(libva)
%endif

Requires:       wine-common = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       wine-desktop = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       wine-fonts = %{?epoch:%{epoch}:}%{version}-%{release}

# x86-32 parts
%ifarch %{ix86} x86_64
Requires:       wine-core(x86-32) = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       wine-capi(x86-32) = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       wine-cms(x86-32) = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       wine-ldap(x86-32) = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       wine-twain(x86-32) = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       wine-pulseaudio(x86-32) = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       wine-openal(x86-32) = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       wine-opencl(x86-32) = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       mingw32-wine-gecko = %winegecko
Requires:       wine-mono = %winemono
Requires:       /usr/bin/ntlm_auth
Requires:       mesa-dri-drivers(x86-32)
%endif

# x86-64 parts
%ifarch x86_64
Requires:       wine-core(x86-64) = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       wine-capi(x86-64) = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       wine-cms(x86-64) = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       wine-ldap(x86-64) = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       wine-twain(x86-64) = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       wine-pulseaudio(x86-64) = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       wine-openal(x86-64) = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       wine-opencl(x86-64) = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       mingw64-wine-gecko = %winegecko
Requires:       wine-mono = %winemono
Requires:       mesa-dri-drivers(x86-64)
%endif

# ARM parts
%ifarch %{arm} aarch64
Requires:       wine-core = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       wine-capi = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       wine-cms = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       wine-ldap = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       wine-twain = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       wine-pulseaudio = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       wine-openal = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       wine-opencl = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       mesa-dri-drivers
Requires:       samba-winbind-clients
%endif

# aarch64 parts
%ifarch aarch64
Requires:       wine-core(aarch-64) = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       wine-capi(aarch-64) = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       wine-cms(aarch-64) = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       wine-ldap(aarch-64) = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       wine-twain(aarch-64) = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       wine-pulseaudio(aarch-64) = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       wine-openal(aarch-64) = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       wine-opencl(aarch-64) = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       mingw64-wine-gecko = %winegecko
Requires:       mesa-dri-drivers(aarch-64)
%endif

%description
Wine as a compatibility layer for UNIX to run Windows applications. This
package includes a program loader, which allows unmodified Windows
3.x/9x/NT binaries to run on x86 and x86_64 Unixes. Wine can use native system
.dll files if they are available.

In Fedora wine is a meta-package which will install everything needed for wine
to work smoothly. Smaller setups can be achieved by installing some of the
wine-* sub packages.

%package core
Summary:        Wine core package
Requires(posttrans):   %{_sbindir}/alternatives
Requires(preun):       %{_sbindir}/alternatives

# require -filesystem
Requires:       wine-filesystem = %{?epoch:%{epoch}:}%{version}-%{release}

%ifarch %{ix86}
# CUPS support uses dlopen - rhbz#1367537
Requires:       cups-libs(x86-32)
Requires:       freetype(x86-32)
Requires:       nss-mdns(x86-32)
Requires:       gnutls(x86-32)
Requires:       gstreamer1-plugins-good(x86-32)
Requires:       libxslt(x86-32)
Requires:       libXcomposite(x86-32)
Requires:       libXcursor(x86-32)
Requires:       libXinerama(x86-32)
Requires:       libXrandr(x86-32)
Requires:       libXrender(x86-32)
#dlopen in windowscodesc (fixes rhbz#1085075)
Requires:       libpng(x86-32)
Requires:       libpcap(x86-32)
Requires:       mesa-libOSMesa(x86-32)
Requires:       libv4l(x86-32)
Requires:       samba-libs(x86-32)
Requires:       unixODBC(x86-32)
Requires:       SDL2(x86-32)
Requires:       vulkan-loader(x86-32)
%if 0%{?wine_staging}
Requires:       gtk3(x86-32)
Requires:       libva(x86-32)
%endif
%endif

%ifarch x86_64
# CUPS support uses dlopen - rhbz#1367537
Requires:       cups-libs(x86-64)
Requires:       freetype(x86-64)
Requires:       nss-mdns(x86-64)
Requires:       gnutls(x86-64)
Requires:       gstreamer1-plugins-good(x86-64)
Requires:       libxslt(x86-64)
Requires:       libXcomposite(x86-64)
Requires:       libXcursor(x86-64)
Requires:       libXinerama(x86-64)
Requires:       libXrandr(x86-64)
Requires:       libXrender(x86-64)
#dlopen in windowscodesc (fixes rhbz#1085075)
Requires:       libpng(x86-64)
Requires:       libpcap(x86-64)
Requires:       mesa-libOSMesa(x86-64)
Requires:       libv4l(x86-64)
Requires:       samba-libs(x86-64)
Requires:       unixODBC(x86-64)
Requires:       SDL2(x86-64)
Requires:       vulkan-loader(x86-64)
%if 0%{?wine_staging}
Requires:       gtk3(x86-64)
Requires:       libva(x86-64)
%endif
%endif

%ifarch %{arm} aarch64
# CUPS support uses dlopen - rhbz#1367537
Requires:       cups-libs
Requires:       freetype
Requires:       nss-mdns
Requires:       gnutls
Requires:       gstreamer1-plugins-good
Requires:       libXrender
Requires:       libXcursor
#dlopen in windowscodesc (fixes rhbz#1085075)
Requires:       libpng
Requires:       libpcap
Requires:       mesa-libOSMesa
Requires:       libv4l
Requires:       unixODBC
Requires:       SDL2
Requires:       vulkan
%if 0%{?wine_staging}
Requires:       gtk3
Requires:       libva
%endif
%endif

# removed as of 1.7.35
Obsoletes:      wine-wow < 1.7.35
Provides:       wine-wow = %{version}-%{release}

%description core
Wine core package includes the basic wine stuff needed by all other packages.

%package systemd
Summary:        Systemd config for the wine binfmt handler
Requires:       systemd >= 23
BuildArch:      noarch
Requires(post):  systemd
Requires(postun): systemd
Obsoletes:      wine-sysvinit < %{version}-%{release}

%description systemd
Register the wine binary handler for windows executables via systemd binfmt
handling. See man binfmt.d for further information.

%package filesystem
Summary:        Filesystem directories for wine
BuildArch:      noarch

%description filesystem
Filesystem directories and basic configuration for wine.

%package common
Summary:        Common files
Requires:       wine-core = %{?epoch:%{epoch}:}%{version}-%{release}
BuildArch:      noarch

%description common
Common wine files and scripts.

%package desktop
Summary:        Desktop integration features for wine
Requires:       wine-core = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       wine-common = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       wine-systemd = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       hicolor-icon-theme
BuildArch:      noarch

%description desktop
Desktop integration features for wine, including mime-types and a binary format
handler service.

%package fonts
Summary:       Wine font files
BuildArch:     noarch
# arial-fonts are available with staging-patchset, only.
%if 0%{?wine_staging}
Requires:      wine-arial-fonts = %{?epoch:%{epoch}:}%{version}-%{release}
%else
Obsoletes:     wine-arial-fonts <= %{?epoch:%{epoch}:}%{version}-%{release}
%endif
Requires:      wine-courier-fonts = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:      wine-fixedsys-fonts = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:      wine-small-fonts = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:      wine-system-fonts = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:      wine-marlett-fonts = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:      wine-ms-sans-serif-fonts = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:      wine-tahoma-fonts = %{?epoch:%{epoch}:}%{version}-%{release}
# times-new-roman-fonts are available with staging-patchset, only.
%if 0%{?wine_staging}
Requires:      wine-times-new-roman-fonts = %{?epoch:%{epoch}:}%{version}-%{release}
%else
Obsoletes:     wine-times-new-roman-fonts <= %{?epoch:%{epoch}:}%{version}-%{release}
%endif
Requires:      wine-symbol-fonts = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:      wine-wingdings-fonts = %{?epoch:%{epoch}:}%{version}-%{release}
# intermediate fix for #593140
Requires:      liberation-sans-fonts liberation-serif-fonts liberation-mono-fonts
Requires:      liberation-narrow-fonts

%description fonts
%{summary}

%if 0%{?wine_staging}
%package arial-fonts
Summary:       Wine Arial font family
BuildArch:     noarch
Requires:      fontpackages-filesystem

%description arial-fonts
%{summary}
%endif

%package courier-fonts
Summary:       Wine Courier font family
BuildArch:     noarch
Requires:      fontpackages-filesystem

%description courier-fonts
%{summary}

%package fixedsys-fonts
Summary:       Wine Fixedsys font family
BuildArch:     noarch
Requires:      fontpackages-filesystem

%description fixedsys-fonts
%{summary}

%package small-fonts
Summary:       Wine Small font family
BuildArch:     noarch
Requires:      fontpackages-filesystem

%description small-fonts
%{summary}

%package system-fonts
Summary:       Wine System font family
BuildArch:     noarch
Requires:      fontpackages-filesystem

%description system-fonts
%{summary}


%package marlett-fonts
Summary:       Wine Marlett font family
BuildArch:     noarch
Requires:      fontpackages-filesystem

%description marlett-fonts
%{summary}


%package ms-sans-serif-fonts
Summary:       Wine MS Sans Serif font family
BuildArch:     noarch
Requires:      fontpackages-filesystem

%description ms-sans-serif-fonts
%{summary}

# rhbz#693180
# http://lists.fedoraproject.org/pipermail/devel/2012-June/168153.html
%package tahoma-fonts
Summary:       Wine Tahoma font family
BuildArch:     noarch
Requires:      wine-filesystem = %{?epoch:%{epoch}:}%{version}-%{release}

%description tahoma-fonts
%{summary}
Please note: If you want system integration for wine tahoma fonts install the
wine-tahoma-fonts-system package.

%package tahoma-fonts-system
Summary:       Wine Tahoma font family system integration
BuildArch:     noarch
Requires:      fontpackages-filesystem
Requires:      wine-tahoma-fonts = %{?epoch:%{epoch}:}%{version}-%{release}

%description tahoma-fonts-system
%{summary}

%if 0%{?wine_staging}
%package times-new-roman-fonts
Summary:       Wine Times New Roman font family
BuildArch:     noarch
Requires:      wine-filesystem = %{?epoch:%{epoch}:}%{version}-%{release}

%description times-new-roman-fonts
%{summary}
Please note: If you want system integration for wine times new roman fonts install the
wine-times-new-roman-fonts-system package.

%package times-new-roman-fonts-system
Summary:       Wine Times New Roman font family system integration
BuildArch:     noarch
Requires:      fontpackages-filesystem
Requires:      wine-times-new-roman-fonts = %{?epoch:%{epoch}:}%{version}-%{release}

%description times-new-roman-fonts-system
%{summary}
%endif

%package symbol-fonts
Summary:       Wine Symbol font family
BuildArch:     noarch
Requires:      fontpackages-filesystem

%description symbol-fonts
%{summary}

%package wingdings-fonts
Summary:       Wine Wingdings font family
BuildArch:     noarch
Requires:      fontpackages-filesystem

%description wingdings-fonts
%{summary}
Please note: If you want system integration for wine wingdings fonts install the
wine-wingdings-fonts-system package.

%package wingdings-fonts-system
Summary:       Wine Wingdings font family system integration
BuildArch:     noarch
Requires:      fontpackages-filesystem
Requires:      wine-wingdings-fonts = %{?epoch:%{epoch}:}%{version}-%{release}

%description wingdings-fonts-system
%{summary}


%package ldap
Summary: LDAP support for wine
Requires: wine-core = %{?epoch:%{epoch}:}%{version}-%{release}

%description ldap
LDAP support for wine

%package cms
Summary: Color Management for wine
Requires: wine-core = %{?epoch:%{epoch}:}%{version}-%{release}

%description cms
Color Management for wine

%package twain
Summary: Twain support for wine
Requires: wine-core = %{?epoch:%{epoch}:}%{version}-%{release}
%ifarch %{ix86}
Requires: sane-backends-libs(x86-32)
%endif
%ifarch x86_64
Requires: sane-backends-libs(x86-64)
%endif
%ifarch %{arm} aarch64
Requires: sane-backends-libs
%endif

%description twain
Twain support for wine

%package capi
Summary: ISDN support for wine
Requires: wine-core = %{?epoch:%{epoch}:}%{version}-%{release}

%description capi
ISDN support for wine

%package devel
Summary: Wine development environment
Requires: wine-core = %{?epoch:%{epoch}:}%{version}-%{release}

%description devel
Header, include files and library definition files for developing applications
with the Wine Windows(TM) emulation libraries.

%package pulseaudio
Summary: Pulseaudio support for wine
Requires: wine-core = %{?epoch:%{epoch}:}%{version}-%{release}
# midi output
Requires: wine-alsa%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description pulseaudio
This package adds a pulseaudio driver for wine.

%package alsa
Summary: Alsa support for wine
Requires: wine-core = %{?epoch:%{epoch}:}%{version}-%{release}

%description alsa
This package adds an alsa driver for wine.

%package openal
Summary: Openal support for wine
Requires: wine-core = %{?epoch:%{epoch}:}%{version}-%{release}

%description openal
This package adds an openal driver for wine.

%package opencl
Summary: OpenCL support for wine
Requires: wine-core = %{?epoch:%{epoch}:}%{version}-%{release}

%Description opencl
This package adds the opencl driver for wine.

%prep
%if 0%{?with_snapshot}
%setup -q -n %{name}-%{commit}
%else
%setup -q -n %{name}-%{ver}
%endif

%if 0%{?wine_staging}
%patch104 -p1 -R
%patch103 -p1 -R
%patch102 -p1 -R
%patch101 -p1 -R
%patch100 -p1 -R
%patch105 -p1
%patch106 -p1
%patch107 -p1
%patch108 -p1
%patch109 -p1
%patch110 -p1
%patch111 -p1
%patch120 -p1
%endif

%patch511 -p1 -b.cjk
%patch599 -p1

# setup and apply wine-staging patches
%if 0%{?wine_staging}

gzip -dc %{SOURCE900} | tar -xf - --strip-components=1

%patch700 -p1
%patch701 -p1
%patch702 -p1
%patch703 -p1
%patch704 -p1
%patch705 -p1
%patch801 -p1
sed -e 's|__stdcall XACT_NOTIFICATION_CALLBACK|XACT_NOTIFICATION_CALLBACK|g' -i include/xact3.idl
%patch802 -p1
%patch803 -p1

%patch5000 -p1

./patches/patchinstall.sh DESTDIR="`pwd`" --all %{?wine_staging_opts}

sed -i "s/  (Staging)/  (%{staging_banner})/g" libs/wine/Makefile.in

%if 0%{?pba}
cp -p %{S:1001} README-pba-pkg

%patch1000 -p1
%endif

%patch720 -p1
%patch721 -p1
%patch722 -p1
%patch723 -p1
%patch724 -p1
%patch725 -p1
%patch726 -p1
%patch800 -p1 -R


# fix parallelized build
sed -i -e 's!^loader server: libs/port libs/wine tools.*!& include!' Makefile.in

%else

rm -rf patches/

%endif

# Verify gecko and mono versions
GECKO_VER="$(grep '^#define' dlls/appwiz.cpl/addons.c | grep ' GECKO_VERSION ' | awk '{print $3}' | tr -d \")"
if [ "${GECKO_VER}" != "%{winegecko}" ] ;then
  echo "winegecko version mismatch. Edit %%global winegecko to ${GECKO_VER}."
  exit 1
fi
MONO_VER="$(grep '^#define' dlls/appwiz.cpl/addons.c | grep ' MONO_VERSION ' | awk '{print $3}' | tr -d \")"
if [ "${MONO_VER}" != "%{winemono}" ] ;then
  echo "winemono version mismatch. Edit %%global winemono to ${MONO_VER}."
  exit 1
fi

sed -e '/winemenubuilder\.exe/s|-a ||g' -i loader/wine.inf.in

sed -i \
  -e 's|-lncurses |-lncursesw |g' \
  -e 's|"-lncurses"|"-lncursesw"|g' \
  -e 's|OpenCL/opencl.h|CL/opencl.h|g' \
  configure

./tools/make_requests


%build

# disable fortify as it breaks wine
# http://bugs.winehq.org/show_bug.cgi?id=24606
# http://bugs.winehq.org/show_bug.cgi?id=25073
export CFLAGS="`echo %{build_cflags} | sed -e 's/-Wp,-D_FORTIFY_SOURCE=2//'` -Wno-error"

export CFLAGS="$CFLAGS -ftree-vectorize"

%ifarch aarch64
# ARM64 now requires clang
# https://source.winehq.org/git/wine.git/commit/8fb8cc03c3edb599dd98f369e14a08f899cbff95
export CC="/usr/bin/clang"
# Fedora's default compiler flags now conflict with what clang supports
# https://bugzilla.redhat.com/show_bug.cgi?id=1658311
export CFLAGS="`echo $CFLAGS | sed -e 's/-fstack-clash-protection//'`" 
%endif

%if 0%{?wine_mingw}
# mingw compiler do not support plugins and some flags are crashing it
export CROSSCFLAGS="`echo $CFLAGS | sed \
  -e 's/-Wp,-D_GLIBCXX_ASSERTIONS//' \
  -e 's/-fstack-protector-strong//' \
  -e 's/-grecord-gcc-switches//' \
  -e 's,-specs=/usr/lib/rpm/redhat/redhat-hardened-cc1,,' \
  -e 's,-specs=/usr/lib/rpm/redhat/redhat-annobin-cc1,,' \
  -e 's/-fasynchronous-unwind-tables//' \
  -e 's/-fstack-clash-protection//' \
  -e 's/-fcf-protection//' \
  ` --param=ssp-buffer-size=4"
# mingw linker do not support -z,relro and now
export LDFLAGS=" "

# Put them again on gcc
mkdir bin
cat > bin/gcc <<'EOF'
#!/usr/bin/sh
exec %{_bindir}/gcc %{build_ldflags} "$@"
EOF
%if !0%{?with_debug}
# -Wl -S to build working stripped PEs
cat > bin/x86_64-w64-mingw32-gcc <<'EOF'
#!/usr/bin/sh
exec %{_bindir}/x86_64-w64-mingw32-gcc -Wl,-S "$@"
EOF
cat > bin/i686-w64-mingw32-gcc <<'EOF'
#!/usr/bin/sh
exec %{_bindir}/i686-w64-mingw32-gcc -Wl,-S "$@"
EOF
%endif
chmod 0755 bin/*gcc
export PATH="$(pwd)/bin:$PATH"
%endif

%configure \
 --sysconfdir=%{_sysconfdir}/wine \
 --x-includes=%{_includedir} --x-libraries=%{_libdir} \
 --without-hal --with-dbus \
 --with-x \
%ifarch %{arm}
 --with-float-abi=hard \
%endif
%ifarch x86_64 aarch64
 --enable-win64 \
%endif
%if 0%{?wine_mingw}
 --with-mingw \
%else
 --without-mingw \
%endif
%if 0%{?wine_staging}
 --with-xattr \
%if !0%{?gtk3}
 --without-gtk3 \
%endif
%endif
 --disable-tests \
%{nil}

%make_build TARGETFLAGS=""

%install
%if 0%{?wine_mingw}
export PATH="$(pwd)/bin:$PATH"
%endif

%makeinstall \
        includedir=%{buildroot}%{_includedir} \
        sysconfdir=%{buildroot}%{_sysconfdir}/wine \
        dlldir=%{buildroot}%{_libdir}/wine \
        LDCONFIG=/bin/true \
        UPDATE_DESKTOP_DATABASE=/bin/true

# setup for alternatives usage
%ifarch x86_64 aarch64
mv %{buildroot}%{_bindir}/wineserver %{buildroot}%{_bindir}/wineserver64
%endif
%ifarch %{ix86} %{arm}
mv %{buildroot}%{_bindir}/wine %{buildroot}%{_bindir}/wine32
mv %{buildroot}%{_bindir}/wineserver %{buildroot}%{_bindir}/wineserver32
%endif
%ifnarch %{arm} aarch64 x86_64
mv %{buildroot}%{_bindir}/wine-preloader %{buildroot}%{_bindir}/wine32-preloader
%endif
touch %{buildroot}%{_bindir}/wine
%ifnarch %{arm}
touch %{buildroot}%{_bindir}/wine-preloader
%endif
touch %{buildroot}%{_bindir}/wineserver

# remove rpath
chrpath --delete %{buildroot}%{_bindir}/wmc
chrpath --delete %{buildroot}%{_bindir}/wrc
%ifarch x86_64 aarch64
chrpath --delete %{buildroot}%{_bindir}/wine64
chrpath --delete %{buildroot}%{_bindir}/wineserver64
%else
chrpath --delete %{buildroot}%{_bindir}/wine32
chrpath --delete %{buildroot}%{_bindir}/wineserver32
%endif

mkdir -p %{buildroot}%{_sysconfdir}/wine

# Allow users to launch Windows programs by just clicking on the .exe file...
mkdir -p %{buildroot}%{_binfmtdir}
install -p -c -m 644 %{SOURCE2} %{buildroot}%{_binfmtdir}/wine.conf

# add wine dir to desktop
mkdir -p %{buildroot}%{_sysconfdir}/xdg/menus/applications-merged
install -p -m 644 %{SOURCE200} \
%{buildroot}%{_sysconfdir}/xdg/menus/applications-merged/wine.menu
mkdir -p %{buildroot}%{_datadir}/desktop-directories
install -p -m 644 %{SOURCE201} \
%{buildroot}%{_datadir}/desktop-directories/Wine.directory

# add gecko dir
mkdir -p %{buildroot}%{_datadir}/wine/gecko

# add mono dir
mkdir -p %{buildroot}%{_datadir}/wine/mono

# extract and install icons
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/scalable/apps

# This replacement masks a composite program icon .SVG down
# so that only its full-size scalable icon is visible
PROGRAM_ICONFIX='s/height="272"/height="256"/;'\
's/width="632"/width="256"\n'\
'   x="368"\n'\
'   y="8"\n'\
'   viewBox="368, 8, 256, 256"/;'

# This icon file is still in the legacy format
install -p -m 644 dlls/user32/resources/oic_winlogo.svg \
 %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/wine.svg
sed -i -e '3s/368/64/' %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/wine.svg

# The rest come from programs/, and contain larger scalable icons
# with a new layout that requires the PROGRAM_ICONFIX sed adjustment
install -p -m 644 programs/notepad/notepad.svg \
 %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/notepad.svg
sed -i -e "$PROGRAM_ICONFIX" %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/notepad.svg

install -p -m 644 programs/regedit/regedit.svg \
 %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/regedit.svg
sed -i -e "$PROGRAM_ICONFIX" %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/regedit.svg

install -p -m 644 programs/msiexec/msiexec.svg \
 %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/msiexec.svg
sed -i -e "$PROGRAM_ICONFIX" %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/msiexec.svg

install -p -m 644 programs/winecfg/winecfg.svg \
 %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/winecfg.svg
sed -i -e "$PROGRAM_ICONFIX" %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/winecfg.svg

install -p -m 644 programs/winefile/winefile.svg \
 %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/winefile.svg
sed -i -e "$PROGRAM_ICONFIX" %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/winefile.svg

install -p -m 644 programs/winemine/winemine.svg \
 %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/winemine.svg
sed -i -e "$PROGRAM_ICONFIX" %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/winemine.svg

install -p -m 644 programs/winhlp32/winhelp.svg \
 %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/winhelp.svg
sed -i -e "$PROGRAM_ICONFIX" %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/winhelp.svg

install -p -m 644 programs/wordpad/wordpad.svg \
 %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/wordpad.svg
sed -i -e "$PROGRAM_ICONFIX" %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/wordpad.svg

install -p -m 644 programs/iexplore/iexplore.svg \
 %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/iexplore.svg
sed -i -e "$PROGRAM_ICONFIX" %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/iexplore.svg

install -p -m 644 dlls/joy.cpl/joy.svg \
  %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/joycpl.svg
sed -i -e '3s/368/64/' %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/joycpl.svg

install -p -m 644 programs/taskmgr/taskmgr.svg \
 %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/taskmgr.svg
sed -i -e "$PROGRAM_ICONFIX" %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/taskmgr.svg

for file in %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/*.svg ;do
  basefile=$(basename ${file} .svg)
  for res in 16 22 24 32 36 48 64 72 96 128 192 256 512 ;do
    dir=%{buildroot}%{_datadir}/icons/hicolor/${res}x${res}/apps
    mkdir -p ${dir}
    rsvg-convert -w ${res} -h ${res} ${file} \
      -o ${dir}/${basefile}.png
  done
done

# install desktop files
desktop-file-install \
  --dir=%{buildroot}%{_datadir}/applications \
  %{SOURCE100}

desktop-file-install \
  --dir=%{buildroot}%{_datadir}/applications \
  %{SOURCE101}

desktop-file-install \
  --dir=%{buildroot}%{_datadir}/applications \
  %{SOURCE102}

desktop-file-install \
  --dir=%{buildroot}%{_datadir}/applications \
  %{SOURCE103}

desktop-file-install \
  --dir=%{buildroot}%{_datadir}/applications \
  %{SOURCE104}

desktop-file-install \
  --dir=%{buildroot}%{_datadir}/applications \
  %{SOURCE105}

desktop-file-install \
  --dir=%{buildroot}%{_datadir}/applications \
  %{SOURCE106}

desktop-file-install \
  --dir=%{buildroot}%{_datadir}/applications \
  %{SOURCE107}

desktop-file-install \
  --dir=%{buildroot}%{_datadir}/applications \
  %{SOURCE108}

desktop-file-install \
  --dir=%{buildroot}%{_datadir}/applications \
  %{SOURCE109}

desktop-file-install \
  --dir=%{buildroot}%{_datadir}/applications \
  %{SOURCE110}

desktop-file-install \
  --dir=%{buildroot}%{_datadir}/applications \
  %{SOURCE111}

desktop-file-install \
  --dir=%{buildroot}%{_datadir}/applications \
  %{SOURCE112}

desktop-file-install \
  --dir=%{buildroot}%{_datadir}/applications \
  %{SOURCE113}

desktop-file-install \
  --dir=%{buildroot}%{_datadir}/applications \
  --delete-original \
  %{buildroot}%{_datadir}/applications/wine.desktop

#mime-types
desktop-file-install \
  --dir=%{buildroot}%{_datadir}/applications \
  %{SOURCE300}

cp -p %{SOURCE3} README-FEDORA
cp -p %{SOURCE6} README-chinforpms

cp -p %{SOURCE502} README-tahoma

mkdir -p %{buildroot}%{_sysconfdir}/ld.so.conf.d/

%ifarch %{ix86} %{arm}
install -p -m644 %{SOURCE4} %{buildroot}%{_sysconfdir}/ld.so.conf.d/
%endif

%ifarch x86_64 aarch64
install -p -m644 %{SOURCE5} %{buildroot}%{_sysconfdir}/ld.so.conf.d/
%endif


# install Tahoma font for system package
install -p -m 0755 -d %{buildroot}/%{_datadir}/fonts/wine-tahoma-fonts
pushd %{buildroot}/%{_datadir}/fonts/wine-tahoma-fonts
ln -s ../../wine/fonts/tahoma.ttf tahoma.ttf
ln -s ../../wine/fonts/tahomabd.ttf tahomabd.ttf
popd

# add config and readme for tahoma
install -m 0755 -d %{buildroot}%{_fontconfig_templatedir} \
                   %{buildroot}%{_fontconfig_confdir}
install -p -m 0644 %{SOURCE501} %{buildroot}%{_fontconfig_templatedir}/20-wine-tahoma-nobitmaps.conf

ln -s %{_fontconfig_templatedir}/20-wine-tahoma-nobitmaps.conf \
      %{buildroot}%{_fontconfig_confdir}/20-wine-tahoma-nobitmaps.conf

%if 0%{?wine_staging}
# install Times New Roman font for system package
install -p -m 0755 -d %{buildroot}/%{_datadir}/fonts/wine-times-new-roman-fonts
pushd %{buildroot}/%{_datadir}/fonts/wine-times-new-roman-fonts
ln -s ../../wine/fonts/times.ttf times.ttf
popd
%endif

# install Wingdings font for system package
install -p -m 0755 -d %{buildroot}/%{_datadir}/fonts/wine-wingdings-fonts
pushd %{buildroot}/%{_datadir}/fonts/wine-wingdings-fonts
ln -s ../../wine/fonts/wingding.ttf wingding.ttf
popd

# clean readme files
pushd documentation
for lang in it hu sv es pt pt_br;
do iconv -f iso8859-1 -t utf-8 README.$lang > \
 README.$lang.conv && mv -f README.$lang.conv README.$lang
done;
popd

rm -f %{buildroot}%{_initrddir}/wine

# wine makefiles are currently broken and don't install the wine man page
install -p -m 0644 loader/wine.man %{buildroot}%{_mandir}/man1/wine.1
install -p -m 0644 loader/wine.de.UTF-8.man %{buildroot}%{_mandir}/de.UTF-8/man1/wine.1
install -p -m 0644 loader/wine.fr.UTF-8.man %{buildroot}%{_mandir}/fr.UTF-8/man1/wine.1
mkdir -p %{buildroot}%{_mandir}/pl.UTF-8/man1
install -p -m 0644 loader/wine.pl.UTF-8.man %{buildroot}%{_mandir}/pl.UTF-8/man1/wine.1

%if 0%{?rhel} == 6
%post sysvinit
if [ $1 -eq 1 ]; then
/sbin/chkconfig --add wine
/sbin/chkconfig --level 2345 wine on
/sbin/service wine start &>/dev/null || :
fi

%preun sysvinit
if [ $1 -eq 0 ]; then
/sbin/service wine stop >/dev/null 2>&1
/sbin/chkconfig --del wine
fi
%endif

%post systemd
%binfmt_apply wine.conf

%postun systemd
if [ $1 -eq 0 ]; then
/bin/systemctl try-restart systemd-binfmt.service
fi

%posttrans core
%ifarch x86_64 aarch64
%{_sbindir}/alternatives --install %{_bindir}/wine \
  wine %{_bindir}/wine64 10 \
  --slave %{_bindir}/wine-preloader wine-preloader %{_bindir}/wine64-preloader
%{_sbindir}/alternatives --install %{_bindir}/wineserver \
  wineserver %{_bindir}/wineserver64 20
%else
%ifnarch %{arm}
%{_sbindir}/alternatives --install %{_bindir}/wine \
  wine %{_bindir}/wine32 20 \
  --slave %{_bindir}/wine-preloader wine-preloader %{_bindir}/wine32-preloader
%{_sbindir}/alternatives --install %{_bindir}/wineserver \
  wineserver %{_bindir}/wineserver32 10
%else
%{_sbindir}/alternatives --install %{_bindir}/wine \
  wine %{_bindir}/wine32 20
%{_sbindir}/alternatives --install %{_bindir}/wineserver \
  wineserver %{_bindir}/wineserver32 10
%endif
%endif

%postun core
if [ $1 -eq 0 ] ; then
%ifarch x86_64 aarch64 aarch64
  %{_sbindir}/alternatives --remove wine %{_bindir}/wine64
  %{_sbindir}/alternatives --remove wineserver %{_bindir}/wineserver64
%else
  %{_sbindir}/alternatives --remove wine %{_bindir}/wine32
  %{_sbindir}/alternatives --remove wineserver %{_bindir}/wineserver32
%endif
fi

%files
# meta package

%files core
%license COPYING.LIB
%license LICENSE
%license LICENSE.OLD
%doc ANNOUNCE
%doc AUTHORS
%doc README-FEDORA
%doc README-chinforpms
%doc README
%doc VERSION
# do not include huge changelogs .OLD .ALPHA .BETA (#204302)
%doc documentation/README.*
%if 0%{?wine_staging}
%doc README.esync
%if 0%{?pba}
%license LICENSE_pba.md
%doc README_pba.md
%doc README-pba-pkg
%endif
%{_bindir}/msidb
%{_libdir}/wine/runas.%{wineexe}
%endif
%{_bindir}/winedump
%{_libdir}/wine/explorer.%{wineexe}
%{_libdir}/wine/cabarc.%{wineexe}
%{_libdir}/wine/control.%{wineexe}
%{_libdir}/wine/cmd.%{wineexe}
%{_libdir}/wine/dxdiag.%{wineexe}
%{_libdir}/wine/notepad.%{wineexe}
%{_libdir}/wine/plugplay.%{wineexe}
%{_libdir}/wine/progman.%{wineexe}
%{_libdir}/wine/taskmgr.%{wineexe}
%{_libdir}/wine/winedbg.exe.so
%{_libdir}/wine/winefile.%{wineexe}
%{_libdir}/wine/winemine.%{wineexe}
%{_libdir}/wine/winemsibuilder.%{wineexe}
%{_libdir}/wine/winepath.exe.so
%{_libdir}/wine/winmgmt.%{wineexe}
%{_libdir}/wine/winver.exe.so
%{_libdir}/wine/wordpad.%{wineexe}
%{_libdir}/wine/write.%{wineexe}
%{_libdir}/wine/wusa.%{wineexe}

%ifarch %{ix86} %{arm}
%{_bindir}/wine32
%ifnarch %{arm}
%{_bindir}/wine32-preloader
%endif
%{_bindir}/wineserver32
%config %{_sysconfdir}/ld.so.conf.d/wine-32.conf
%endif

%ifarch x86_64 aarch64
%{_bindir}/wine64
%{_bindir}/wineserver64
%config %{_sysconfdir}/ld.so.conf.d/wine-64.conf
%endif
%ifarch x86_64 aarch64
%{_bindir}/wine64-preloader
%endif

%ghost %{_bindir}/wine
%ifnarch %{arm}
%ghost %{_bindir}/wine-preloader
%endif
%ghost %{_bindir}/wineserver

%dir %{_libdir}/wine
%dir %{_libdir}/wine/fakedlls
%{_libdir}/wine/fakedlls/*

%{_libdir}/wine/attrib.%{wineexe}
%{_libdir}/wine/arp.%{wineexe}
%{_libdir}/wine/aspnet_regiis.%{wineexe}
%{_libdir}/wine/cacls.%{wineexe}
%{_libdir}/wine/conhost.%{wineexe}
%{_libdir}/wine/cscript.%{wineexe}
%{_libdir}/wine/dism.%{wineexe}
%{_libdir}/wine/dpnsvr.%{wineexe}
%{_libdir}/wine/eject.%{wineexe}
%{_libdir}/wine/expand.%{wineexe}
%{_libdir}/wine/extrac32.%{wineexe}
%{_libdir}/wine/fc.%{wineexe}
%{_libdir}/wine/find.%{wineexe}
%{_libdir}/wine/findstr.%{wineexe}
%{_libdir}/wine/fsutil.%{wineexe}
%{_libdir}/wine/hostname.%{wineexe}
%{_libdir}/wine/ipconfig.%{wineexe}
%{_libdir}/wine/winhlp32.%{wineexe}
%{_libdir}/wine/mshta.%{wineexe}
%if 0%{?wine_staging}
%{_libdir}/wine/msidb.%{wineexe}
%endif
%{_libdir}/wine/msiexec.%{wineexe}
%{_libdir}/wine/net.%{wineexe}
%{_libdir}/wine/netstat.%{wineexe}
%{_libdir}/wine/ngen.%{wineexe}
%{_libdir}/wine/ntoskrnl.%{wineexe}
%{_libdir}/wine/oleview.%{wineexe}
%{_libdir}/wine/ping.%{wineexe}
%{_libdir}/wine/powershell.%{wineexe}
%{_libdir}/wine/reg.%{wineexe}
%{_libdir}/wine/regasm.%{wineexe}
%{_libdir}/wine/regedit.%{wineexe}
%{_libdir}/wine/regini.%{wineexe}
%{_libdir}/wine/regsvcs.%{wineexe}
%{_libdir}/wine/regsvr32.%{wineexe}
%{_libdir}/wine/rpcss.%{wineexe}
%{_libdir}/wine/rundll32.%{wineexe}
%{_libdir}/wine/schtasks.%{wineexe}
%{_libdir}/wine/sdbinst.%{wineexe}
%{_libdir}/wine/secedit.%{wineexe}
%{_libdir}/wine/servicemodelreg.%{wineexe}
%{_libdir}/wine/services.%{wineexe}
%{_libdir}/wine/start.%{wineexe}
%{_libdir}/wine/tasklist.%{wineexe}
%{_libdir}/wine/termsv.%{wineexe}
%{_libdir}/wine/view.%{wineexe}
%{_libdir}/wine/wevtutil.%{wineexe}
%{_libdir}/wine/wineboot.%{wineexe}
%{_libdir}/wine/winebrowser.exe.so
%{_libdir}/wine/wineconsole.exe.so
%{_libdir}/wine/winemenubuilder.exe.so
%{_libdir}/wine/winecfg.exe.so
%{_libdir}/wine/winedevice.%{wineexe}
%{_libdir}/wine/wmplayer.%{wineexe}
%{_libdir}/wine/wscript.%{wineexe}
%{_libdir}/wine/uninstaller.%{wineexe}

%{_libdir}/libwine.so.1*

%{_libdir}/wine/acledit.%{winedll}
%{_libdir}/wine/aclui.%{winedll}
%{_libdir}/wine/activeds.%{winedll}
%{_libdir}/wine/actxprxy.%{winedll}
%{_libdir}/wine/adsldp.%{winedll}
%{_libdir}/wine/adsldpc.%{winedll}
%{_libdir}/wine/advapi32.dll.so
%{_libdir}/wine/advpack.%{winedll}
%{_libdir}/wine/amsi.%{winedll}
%{_libdir}/wine/amstream.%{winedll}
%{_libdir}/wine/api-ms-win-appmodel-identity-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-appmodel-runtime-l1-1-1.%{winedll}
%{_libdir}/wine/api-ms-win-appmodel-runtime-l1-1-2.%{winedll}
%{_libdir}/wine/api-ms-win-core-apiquery-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-appcompat-l1-1-1.%{winedll}
%{_libdir}/wine/api-ms-win-core-appinit-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-atoms-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-bem-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-com-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-com-l1-1-1.%{winedll}
%{_libdir}/wine/api-ms-win-core-com-private-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-comm-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-console-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-console-l2-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-crt-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-crt-l2-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-datetime-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-datetime-l1-1-1.%{winedll}
%{_libdir}/wine/api-ms-win-core-debug-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-debug-l1-1-1.%{winedll}
%{_libdir}/wine/api-ms-win-core-delayload-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-delayload-l1-1-1.%{winedll}
%{_libdir}/wine/api-ms-win-core-errorhandling-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-errorhandling-l1-1-1.%{winedll}
%{_libdir}/wine/api-ms-win-core-errorhandling-l1-1-2.%{winedll}
%{_libdir}/wine/api-ms-win-core-errorhandling-l1-1-3.%{winedll}
%{_libdir}/wine/api-ms-win-core-fibers-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-fibers-l1-1-1.%{winedll}
%{_libdir}/wine/api-ms-win-core-file-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-file-l1-2-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-file-l1-2-1.%{winedll}
%{_libdir}/wine/api-ms-win-core-file-l1-2-2.%{winedll}
%{_libdir}/wine/api-ms-win-core-file-l2-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-file-l2-1-1.%{winedll}
%{_libdir}/wine/api-ms-win-core-file-l2-1-2.%{winedll}
%{_libdir}/wine/api-ms-win-core-handle-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-heap-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-heap-l1-2-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-heap-l2-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-heap-obsolete-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-interlocked-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-interlocked-l1-2-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-io-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-io-l1-1-1.%{winedll}
%{_libdir}/wine/api-ms-win-core-job-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-job-l2-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-largeinteger-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-kernel32-legacy-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-kernel32-legacy-l1-1-1.%{winedll}
%{_libdir}/wine/api-ms-win-core-kernel32-private-l1-1-1.%{winedll}
%{_libdir}/wine/api-ms-win-core-libraryloader-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-libraryloader-l1-1-1.%{winedll}
%{_libdir}/wine/api-ms-win-core-libraryloader-l1-2-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-libraryloader-l1-2-1.%{winedll}
%{_libdir}/wine/api-ms-win-core-libraryloader-l1-2-2.%{winedll}
%{_libdir}/wine/api-ms-win-core-localization-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-localization-l1-2-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-localization-l1-2-1.%{winedll}
%{_libdir}/wine/api-ms-win-core-localization-l2-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-localization-obsolete-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-localization-obsolete-l1-2-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-localization-obsolete-l1-3-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-localization-private-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-localregistry-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-memory-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-memory-l1-1-1.%{winedll}
%{_libdir}/wine/api-ms-win-core-memory-l1-1-2.%{winedll}
%{_libdir}/wine/api-ms-win-core-misc-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-namedpipe-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-namedpipe-l1-2-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-namespace-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-normalization-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-path-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-privateprofile-l1-1-1.%{winedll}
%{_libdir}/wine/api-ms-win-core-processenvironment-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-processenvironment-l1-2-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-processthreads-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-processthreads-l1-1-1.%{winedll}
%{_libdir}/wine/api-ms-win-core-processthreads-l1-1-2.%{winedll}
%{_libdir}/wine/api-ms-win-core-processthreads-l1-1-3.%{winedll}
%{_libdir}/wine/api-ms-win-core-processtopology-obsolete-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-profile-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-psapi-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-psapi-ansi-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-psapi-obsolete-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-quirks-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-realtime-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-registry-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-registry-l2-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-registryuserspecific-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-rtlsupport-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-rtlsupport-l1-2-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-shlwapi-legacy-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-shlwapi-obsolete-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-shlwapi-obsolete-l1-2-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-shutdown-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-sidebyside-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-string-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-string-l2-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-string-obsolete-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-stringansi-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-stringloader-l1-1-1.%{winedll}
%{_libdir}/wine/api-ms-win-core-synch-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-synch-l1-2-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-synch-l1-2-1.%{winedll}
%{_libdir}/wine/api-ms-win-core-synch-ansi-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-sysinfo-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-sysinfo-l1-2-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-sysinfo-l1-2-1.%{winedll}
%{_libdir}/wine/api-ms-win-core-threadpool-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-threadpool-l1-2-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-threadpool-legacy-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-threadpool-private-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-timezone-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-toolhelp-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-url-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-util-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-version-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-version-l1-1-1.%{winedll}
%{_libdir}/wine/api-ms-win-core-version-private-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-versionansi-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-windowserrorreporting-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-winrt-error-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-winrt-error-l1-1-1.%{winedll}
%{_libdir}/wine/api-ms-win-core-winrt-errorprivate-l1-1-1.%{winedll}
%{_libdir}/wine/api-ms-win-core-winrt-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-winrt-registration-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-winrt-roparameterizediid-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-winrt-string-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-winrt-string-l1-1-1.%{winedll}
%{_libdir}/wine/api-ms-win-core-wow64-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-wow64-l1-1-1.%{winedll}
%{_libdir}/wine/api-ms-win-core-xstate-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-xstate-l2-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-crt-conio-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-crt-convert-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-crt-environment-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-crt-filesystem-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-crt-heap-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-crt-locale-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-crt-math-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-crt-multibyte-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-crt-private-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-crt-process-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-crt-runtime-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-crt-stdio-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-crt-string-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-crt-time-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-crt-utility-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-devices-config-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-devices-config-l1-1-1.%{winedll}
%{_libdir}/wine/api-ms-win-devices-query-l1-1-1.%{winedll}
%{_libdir}/wine/api-ms-win-downlevel-advapi32-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-downlevel-advapi32-l2-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-downlevel-normaliz-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-downlevel-ole32-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-downlevel-shell32-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-downlevel-shlwapi-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-downlevel-shlwapi-l2-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-downlevel-user32-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-downlevel-version-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-dx-d3dkmt-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-eventing-classicprovider-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-eventing-consumer-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-eventing-controller-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-eventing-legacy-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-eventing-provider-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-eventlog-legacy-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-gdi-dpiinfo-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-mm-joystick-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-mm-misc-l1-1-1.%{winedll}
%{_libdir}/wine/api-ms-win-mm-mme-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-mm-time-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-ntuser-dc-access-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-ntuser-rectangle-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-ntuser-sysparams-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-perf-legacy-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-power-base-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-power-setting-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-rtcore-ntuser-draw-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-rtcore-ntuser-private-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-rtcore-ntuser-private-l1-1-4.%{winedll}
%{_libdir}/wine/api-ms-win-rtcore-ntuser-window-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-rtcore-ntuser-winevent-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-rtcore-ntuser-wmpointer-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-rtcore-ntuser-wmpointer-l1-1-3.%{winedll}
%{_libdir}/wine/api-ms-win-security-activedirectoryclient-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-security-audit-l1-1-1.%{winedll}
%{_libdir}/wine/api-ms-win-security-base-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-security-base-l1-2-0.%{winedll}
%{_libdir}/wine/api-ms-win-security-base-private-l1-1-1.%{winedll}
%{_libdir}/wine/api-ms-win-security-credentials-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-security-cryptoapi-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-security-grouppolicy-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-security-lsalookup-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-security-lsalookup-l1-1-1.%{winedll}
%{_libdir}/wine/api-ms-win-security-lsalookup-l2-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-security-lsalookup-l2-1-1.%{winedll}
%{_libdir}/wine/api-ms-win-security-lsapolicy-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-security-provider-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-security-sddl-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-security-systemfunctions-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-service-core-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-service-core-l1-1-1.%{winedll}
%{_libdir}/wine/api-ms-win-service-management-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-service-management-l2-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-service-private-l1-1-1.%{winedll}
%{_libdir}/wine/api-ms-win-service-winsvc-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-service-winsvc-l1-2-0.%{winedll}
%{_libdir}/wine/api-ms-win-shcore-obsolete-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-shcore-scaling-l1-1-1.%{winedll}
%{_libdir}/wine/api-ms-win-shcore-stream-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-shcore-thread-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-shell-shellcom-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-shell-shellfolders-l1-1-0.%{winedll}
%{_libdir}/wine/apphelp.%{winedll}
%{_libdir}/wine/appwiz.%{winecpl}
%{_libdir}/wine/atl.%{winedll}
%{_libdir}/wine/atl80.%{winedll}
%{_libdir}/wine/atl90.%{winedll}
%{_libdir}/wine/atl100.%{winedll}
%{_libdir}/wine/atl110.%{winedll}
%{_libdir}/wine/atlthunk.%{winedll}
%{_libdir}/wine/atmlib.%{winedll}
%{_libdir}/wine/authz.%{winedll}
%{_libdir}/wine/avicap32.dll.so
%{_libdir}/wine/avifil32.%{winedll}
%{_libdir}/wine/avrt.%{winedll}
%{_libdir}/wine/bcrypt.dll.so
%{_libdir}/wine/bluetoothapis.%{winedll}
%{_libdir}/wine/browseui.%{winedll}
%{_libdir}/wine/bthprops.%{winecpl}
%{_libdir}/wine/cabinet.dll.so
%{_libdir}/wine/cards.%{winedll}
%{_libdir}/wine/cdosys.%{winedll}
%{_libdir}/wine/cfgmgr32.%{winedll}
%{_libdir}/wine/clock.%{wineexe}
%{_libdir}/wine/clusapi.%{winedll}
%{_libdir}/wine/combase.%{winedll}
%{_libdir}/wine/comcat.%{winedll}
%{_libdir}/wine/comctl32.%{winedll}
%{_libdir}/wine/comdlg32.%{winedll}
%{_libdir}/wine/compstui.%{winedll}
%{_libdir}/wine/comsvcs.%{winedll}
%{_libdir}/wine/concrt140.%{winedll}
%{_libdir}/wine/connect.%{winedll}
%{_libdir}/wine/credui.%{winedll}
%{_libdir}/wine/crtdll.dll.so
%{_libdir}/wine/crypt32.dll.so
%{_libdir}/wine/cryptdlg.%{winedll}
%{_libdir}/wine/cryptdll.%{winedll}
%{_libdir}/wine/cryptext.%{winedll}
%{_libdir}/wine/cryptnet.%{winedll}
%{_libdir}/wine/cryptui.%{winedll}
%{_libdir}/wine/ctapi32.dll.so
%{_libdir}/wine/ctl3d32.%{winedll}
%{_libdir}/wine/d2d1.%{winedll}
%{_libdir}/wine/d3d10.%{winedll}
%{_libdir}/wine/d3d10_1.%{winedll}
%{_libdir}/wine/d3d10core.%{winedll}
%{_libdir}/wine/d3d11.%{winedll}
%{_libdir}/wine/d3d12.dll.so
%{_libdir}/wine/d3dcompiler_*.%{winedll}
%{_libdir}/wine/d3dim.%{winedll}
%{_libdir}/wine/d3drm.%{winedll}
%{_libdir}/wine/d3dx9_*.%{winedll}
%{_libdir}/wine/d3dx10_*.%{winedll}
%{_libdir}/wine/d3dx11_42.%{winedll}
%{_libdir}/wine/d3dx11_43.%{winedll}
%{_libdir}/wine/d3dxof.%{winedll}
%{_libdir}/wine/davclnt.%{winedll}
%{_libdir}/wine/dbgeng.%{winedll}
%{_libdir}/wine/dbghelp.dll.so
%{_libdir}/wine/dciman32.%{winedll}
%{_libdir}/wine/ddraw.%{winedll}
%{_libdir}/wine/ddrawex.%{winedll}
%{_libdir}/wine/devenum.%{winedll}
%{_libdir}/wine/dhcpcsvc.%{winedll}
%{_libdir}/wine/dhtmled.%{wineocx}
%{_libdir}/wine/difxapi.%{winedll}
%{_libdir}/wine/dinput.dll.so
%{_libdir}/wine/dinput8.dll.so
%{_libdir}/wine/directmanipulation.%{winedll}
%{_libdir}/wine/dispex.%{winedll}
%{_libdir}/wine/dmband.%{winedll}
%{_libdir}/wine/dmcompos.%{winedll}
%{_libdir}/wine/dmime.%{winedll}
%{_libdir}/wine/dmloader.%{winedll}
%{_libdir}/wine/dmscript.%{winedll}
%{_libdir}/wine/dmstyle.%{winedll}
%{_libdir}/wine/dmsynth.%{winedll}
%{_libdir}/wine/dmusic.%{winedll}
%{_libdir}/wine/dmusic32.%{winedll}
%{_libdir}/wine/dplay.%{winedll}
%{_libdir}/wine/dplayx.%{winedll}
%{_libdir}/wine/dpnaddr.%{winedll}
%{_libdir}/wine/dpnet.%{winedll}
%{_libdir}/wine/dpnhpast.%{winedll}
%{_libdir}/wine/dpnlobby.%{winedll}
%{_libdir}/wine/dpvoice.%{winedll}
%{_libdir}/wine/dpwsockx.%{winedll}
%{_libdir}/wine/drmclien.%{winedll}
%if 0%{?wine_staging}
%{_libdir}/wine/dsdmo.%{winedll}
%endif
%{_libdir}/wine/dsound.%{winedll}
%{_libdir}/wine/dsquery.%{winedll}
%{_libdir}/wine/dssenh.%{winedll}
%{_libdir}/wine/dswave.%{winedll}
%{_libdir}/wine/dwmapi.%{winedll}
%{_libdir}/wine/dwrite.dll.so
%{_libdir}/wine/dx8vb.%{winedll}
%{_libdir}/wine/dxdiagn.%{winedll}
%{_libdir}/wine/dxgi.dll.so
%if 0%{?wine_staging}
%{_libdir}/wine/dxgkrnl.%{winesys}
%{_libdir}/wine/dxgmms1.%{winesys}
%endif
%{_libdir}/wine/dxva2.dll.so
%{_libdir}/wine/esent.%{winedll}
%{_libdir}/wine/evr.%{winedll}
%{_libdir}/wine/explorerframe.%{winedll}
%{_libdir}/wine/ext-ms-win-authz-context-l1-1-0.%{winedll}
%{_libdir}/wine/ext-ms-win-domainjoin-netjoin-l1-1-0.%{winedll}
%{_libdir}/wine/ext-ms-win-dwmapi-ext-l1-1-0.%{winedll}
%{_libdir}/wine/ext-ms-win-gdi-dc-l1-2-0.%{winedll}
%{_libdir}/wine/ext-ms-win-gdi-dc-create-l1-1-0.%{winedll}
%{_libdir}/wine/ext-ms-win-gdi-dc-create-l1-1-1.%{winedll}
%{_libdir}/wine/ext-ms-win-gdi-devcaps-l1-1-0.%{winedll}
%{_libdir}/wine/ext-ms-win-gdi-draw-l1-1-0.%{winedll}
%{_libdir}/wine/ext-ms-win-gdi-draw-l1-1-1.%{winedll}
%{_libdir}/wine/ext-ms-win-gdi-font-l1-1-0.%{winedll}
%{_libdir}/wine/ext-ms-win-gdi-font-l1-1-1.%{winedll}
%{_libdir}/wine/ext-ms-win-gdi-render-l1-1-0.%{winedll}
%{_libdir}/wine/ext-ms-win-kernel32-package-l1-1-1.%{winedll}
%{_libdir}/wine/ext-ms-win-kernel32-package-current-l1-1-0.%{winedll}
%{_libdir}/wine/ext-ms-win-ntuser-dialogbox-l1-1-0.%{winedll}
%{_libdir}/wine/ext-ms-win-ntuser-draw-l1-1-0.%{winedll}
%{_libdir}/wine/ext-ms-win-ntuser-gui-l1-1-0.%{winedll}
%{_libdir}/wine/ext-ms-win-ntuser-gui-l1-3-0.%{winedll}
%{_libdir}/wine/ext-ms-win-ntuser-keyboard-l1-3-0.%{winedll}
%{_libdir}/wine/ext-ms-win-ntuser-misc-l1-2-0.%{winedll}
%{_libdir}/wine/ext-ms-win-ntuser-misc-l1-5-1.%{winedll}
%{_libdir}/wine/ext-ms-win-ntuser-message-l1-1-0.%{winedll}
%{_libdir}/wine/ext-ms-win-ntuser-message-l1-1-1.%{winedll}
%{_libdir}/wine/ext-ms-win-ntuser-misc-l1-1-0.%{winedll}
%{_libdir}/wine/ext-ms-win-ntuser-mouse-l1-1-0.%{winedll}
%{_libdir}/wine/ext-ms-win-ntuser-private-l1-1-1.%{winedll}
%{_libdir}/wine/ext-ms-win-ntuser-private-l1-3-1.%{winedll}
%{_libdir}/wine/ext-ms-win-ntuser-rectangle-ext-l1-1-0.%{winedll}
%{_libdir}/wine/ext-ms-win-ntuser-uicontext-ext-l1-1-0.%{winedll}
%{_libdir}/wine/ext-ms-win-ntuser-window-l1-1-0.%{winedll}
%{_libdir}/wine/ext-ms-win-ntuser-window-l1-1-1.%{winedll}
%{_libdir}/wine/ext-ms-win-ntuser-window-l1-1-4.%{winedll}
%{_libdir}/wine/ext-ms-win-ntuser-windowclass-l1-1-0.%{winedll}
%{_libdir}/wine/ext-ms-win-ntuser-windowclass-l1-1-1.%{winedll}
%{_libdir}/wine/ext-ms-win-oleacc-l1-1-0.%{winedll}
%{_libdir}/wine/ext-ms-win-ras-rasapi32-l1-1-0.%{winedll}
%{_libdir}/wine/ext-ms-win-rtcore-gdi-devcaps-l1-1-0.%{winedll}
%{_libdir}/wine/ext-ms-win-rtcore-gdi-object-l1-1-0.%{winedll}
%{_libdir}/wine/ext-ms-win-rtcore-gdi-rgn-l1-1-0.%{winedll}
%{_libdir}/wine/ext-ms-win-rtcore-ntuser-cursor-l1-1-0.%{winedll}
%{_libdir}/wine/ext-ms-win-rtcore-ntuser-dc-access-l1-1-0.%{winedll}
%{_libdir}/wine/ext-ms-win-rtcore-ntuser-dpi-l1-1-0.%{winedll}
%{_libdir}/wine/ext-ms-win-rtcore-ntuser-dpi-l1-2-0.%{winedll}
%{_libdir}/wine/ext-ms-win-rtcore-ntuser-rawinput-l1-1-0.%{winedll}
%{_libdir}/wine/ext-ms-win-rtcore-ntuser-syscolors-l1-1-0.%{winedll}
%{_libdir}/wine/ext-ms-win-rtcore-ntuser-sysparams-l1-1-0.%{winedll}
%{_libdir}/wine/ext-ms-win-security-credui-l1-1-0.%{winedll}
%{_libdir}/wine/ext-ms-win-security-cryptui-l1-1-0.%{winedll}
%{_libdir}/wine/ext-ms-win-shell-comctl32-init-l1-1-0.%{winedll}
%{_libdir}/wine/ext-ms-win-shell-comdlg32-l1-1-0.%{winedll}
%{_libdir}/wine/ext-ms-win-shell-shell32-l1-2-0.%{winedll}
%{_libdir}/wine/ext-ms-win-uxtheme-themes-l1-1-0.%{winedll}
%if 0%{?wine_staging}
%{_libdir}/wine/ext-ms-win-appmodel-usercontext-l1-1-0.dll.so
%{_libdir}/wine/ext-ms-win-xaml-pal-l1-1-0.dll.so
%endif
%{_libdir}/wine/faultrep.%{winedll}
%{_libdir}/wine/feclient.%{winedll}
%{_libdir}/wine/fltlib.%{winedll}
%{_libdir}/wine/fltmgr.%{winesys}
%{_libdir}/wine/fntcache.%{winedll}
%{_libdir}/wine/fontsub.%{winedll}
%{_libdir}/wine/fusion.%{winedll}
%{_libdir}/wine/fwpuclnt.%{winedll}
%{_libdir}/wine/gameux.%{winedll}
%{_libdir}/wine/gdi32.dll.so
%{_libdir}/wine/gdiplus.%{winedll}
%{_libdir}/wine/glu32.dll.so
%{_libdir}/wine/gphoto2.ds.so
%{_libdir}/wine/gpkcsp.%{winedll}
%{_libdir}/wine/hal.%{winedll}
%{_libdir}/wine/hh.%{wineexe}
%{_libdir}/wine/hhctrl.%{wineocx}
%{_libdir}/wine/hid.%{winedll}
%{_libdir}/wine/hidclass.%{winesys}
%{_libdir}/wine/hlink.%{winedll}
%{_libdir}/wine/hnetcfg.%{winedll}
%{_libdir}/wine/http.%{winesys}
%{_libdir}/wine/httpapi.%{winedll}
%{_libdir}/wine/icacls.%{wineexe}
%{_libdir}/wine/iccvid.%{winedll}
%{_libdir}/wine/icinfo.%{wineexe}
%{_libdir}/wine/icmp.%{winedll}
%{_libdir}/wine/ieframe.%{winedll}
%if 0%{?wine_staging}
%{_libdir}/wine/iertutil.dll.so
%endif
%{_libdir}/wine/ieproxy.%{winedll}
%{_libdir}/wine/imaadp32.%{wineacm}
%{_libdir}/wine/imagehlp.%{winedll}
%{_libdir}/wine/imm32.%{winedll}
%{_libdir}/wine/inetcomm.%{winedll}
%{_libdir}/wine/inetcpl.%{winecpl}
%{_libdir}/wine/inetmib1.%{winedll}
%{_libdir}/wine/infosoft.%{winedll}
%{_libdir}/wine/initpki.%{winedll}
%{_libdir}/wine/inkobj.%{winedll}
%{_libdir}/wine/inseng.%{winedll}
%{_libdir}/wine/iphlpapi.dll.so
%{_libdir}/wine/iprop.%{winedll}
%{_libdir}/wine/irprops.%{winecpl}
%{_libdir}/wine/itircl.%{winedll}
%{_libdir}/wine/itss.%{winedll}
%{_libdir}/wine/joy.%{winecpl}
%{_libdir}/wine/jscript.%{winedll}
%{_libdir}/wine/jsproxy.%{winedll}
%{_libdir}/wine/kerberos.dll.so
%{_libdir}/wine/kernel32.dll.so
%{_libdir}/wine/kernelbase.%{winedll}
%{_libdir}/wine/ksecdd.%{winesys}
%{_libdir}/wine/ksuser.%{winedll}
%{_libdir}/wine/ktmw32.%{winedll}
%{_libdir}/wine/l3codeca.acm.so
%{_libdir}/wine/loadperf.%{winedll}
%{_libdir}/wine/localspl.%{winedll}
%{_libdir}/wine/localui.%{winedll}
%{_libdir}/wine/lodctr.%{wineexe}
%{_libdir}/wine/lz32.%{winedll}
%{_libdir}/wine/mapi32.%{winedll}
%{_libdir}/wine/mapistub.%{winedll}
%{_libdir}/wine/mciavi32.%{winedll}
%{_libdir}/wine/mcicda.%{winedll}
%{_libdir}/wine/mciqtz32.%{winedll}
%{_libdir}/wine/mciseq.%{winedll}
%{_libdir}/wine/mciwave.%{winedll}
%{_libdir}/wine/mf.%{winedll}
%{_libdir}/wine/mf3216.%{winedll}
%{_libdir}/wine/mferror.%{winedll}
%{_libdir}/wine/mfmediaengine.%{winedll}
%{_libdir}/wine/mfplat.%{winedll}
%{_libdir}/wine/mfplay.%{winedll}
%{_libdir}/wine/mfreadwrite.%{winedll}
%{_libdir}/wine/mgmtapi.%{winedll}
%{_libdir}/wine/midimap.%{winedll}
%{_libdir}/wine/mlang.%{winedll}
%{_libdir}/wine/mmcndmgr.%{winedll}
%{_libdir}/wine/mmdevapi.%{winedll}
%{_libdir}/wine/mofcomp.%{wineexe}
%{_libdir}/wine/mountmgr.sys.so
%{_libdir}/wine/mp3dmod.dll.so
%{_libdir}/wine/mpr.%{winedll}
%{_libdir}/wine/mprapi.%{winedll}
%{_libdir}/wine/msacm32.%{winedll}
%{_libdir}/wine/msacm32.%{winedrv}
%{_libdir}/wine/msadp32.%{wineacm}
%{_libdir}/wine/msasn1.%{winedll}
%{_libdir}/wine/mscat32.%{winedll}
%{_libdir}/wine/mscoree.%{winedll}
%{_libdir}/wine/mscorwks.%{winedll}
%{_libdir}/wine/msctf.%{winedll}
%{_libdir}/wine/msctfp.%{winedll}
%{_libdir}/wine/msdaps.%{winedll}
%{_libdir}/wine/msdelta.%{winedll}
%{_libdir}/wine/msdmo.%{winedll}
%{_libdir}/wine/msdrm.%{winedll}
%{_libdir}/wine/msftedit.%{winedll}
%{_libdir}/wine/msg711.%{wineacm}
%{_libdir}/wine/msgsm32.acm.so
%{_libdir}/wine/mshtml.%{winedll}
%{_libdir}/wine/mshtml.%{winetlb}
%{_libdir}/wine/msi.%{winedll}
%{_libdir}/wine/msident.%{winedll}
%{_libdir}/wine/msimtf.%{winedll}
%{_libdir}/wine/msimg32.%{winedll}
%{_libdir}/wine/msimsg.%{winedll}
%{_libdir}/wine/msinfo32.%{wineexe}
%{_libdir}/wine/msisip.%{winedll}
%{_libdir}/wine/msisys.%{wineocx}
%{_libdir}/wine/msls31.%{winedll}
%{_libdir}/wine/msnet32.%{winedll}
%{_libdir}/wine/mspatcha.%{winedll}
%{_libdir}/wine/msports.%{winedll}
%{_libdir}/wine/msscript.%{wineocx}
%{_libdir}/wine/mssign32.%{winedll}
%{_libdir}/wine/mssip32.%{winedll}
%{_libdir}/wine/msrle32.%{winedll}
%{_libdir}/wine/mstask.%{winedll}
%{_libdir}/wine/msvcirt.%{winedll}
%{_libdir}/wine/msvcm80.%{winedll}
%{_libdir}/wine/msvcm90.%{winedll}
%{_libdir}/wine/msvcp60.%{winedll}
%{_libdir}/wine/msvcp70.%{winedll}
%{_libdir}/wine/msvcp71.%{winedll}
%{_libdir}/wine/msvcp80.%{winedll}
%{_libdir}/wine/msvcp90.%{winedll}
%{_libdir}/wine/msvcp100.%{winedll}
%{_libdir}/wine/msvcp110.%{winedll}
%{_libdir}/wine/msvcp120.%{winedll}
%{_libdir}/wine/msvcp120_app.%{winedll}
%{_libdir}/wine/msvcp140.%{winedll}
%{_libdir}/wine/msvcr70.dll.so
%{_libdir}/wine/msvcr71.dll.so
%{_libdir}/wine/msvcr80.dll.so
%{_libdir}/wine/msvcr90.dll.so
%{_libdir}/wine/msvcr100.dll.so
%{_libdir}/wine/msvcr110.dll.so
%{_libdir}/wine/msvcr120.dll.so
%{_libdir}/wine/msvcr120_app.%{winedll}
%{_libdir}/wine/msvcrt.dll.so
%{_libdir}/wine/msvcrt20.%{winedll}
%{_libdir}/wine/msvcrt40.%{winedll}
%{_libdir}/wine/msvcrtd.dll.so
%{_libdir}/wine/msvfw32.%{winedll}
%{_libdir}/wine/msvidc32.%{winedll}
%{_libdir}/wine/mswsock.%{winedll}
%{_libdir}/wine/msxml.%{winedll}
%{_libdir}/wine/msxml2.%{winedll}
%{_libdir}/wine/msxml3.dll.so
%{_libdir}/wine/msxml4.%{winedll}
%{_libdir}/wine/msxml6.%{winedll}
%{_libdir}/wine/mtxdm.%{winedll}
%{_libdir}/wine/nddeapi.%{winedll}
%{_libdir}/wine/ncrypt.%{winedll}
%{_libdir}/wine/ndis.%{winesys}
%{_libdir}/wine/netapi32.dll.so
%{_libdir}/wine/netcfgx.%{winedll}
%{_libdir}/wine/netprofm.%{winedll}
%{_libdir}/wine/netsh.%{wineexe}
%{_libdir}/wine/newdev.%{winedll}
%{_libdir}/wine/ninput.%{winedll}
%{_libdir}/wine/normaliz.%{winedll}
%{_libdir}/wine/npmshtml.%{winedll}
%{_libdir}/wine/npptools.%{winedll}
%{_libdir}/wine/ntdll.dll.so
%{_libdir}/wine/ntdsapi.%{winedll}
%{_libdir}/wine/ntprint.%{winedll}
%if 0%{?wine_staging}
%{_libdir}/wine/nvcuda.dll.so
%{_libdir}/wine/nvcuvid.dll.so
%endif
%{_libdir}/wine/objsel.%{winedll}
%{_libdir}/wine/odbc32.dll.so
%{_libdir}/wine/odbccp32.%{winedll}
%{_libdir}/wine/odbccu32.%{winedll}
%{_libdir}/wine/ole32.%{winedll}
%{_libdir}/wine/oleacc.%{winedll}
%{_libdir}/wine/oleaut32.%{winedll}
%{_libdir}/wine/olecli32.%{winedll}
%{_libdir}/wine/oledb32.%{winedll}
%{_libdir}/wine/oledlg.%{winedll}
%{_libdir}/wine/olepro32.%{winedll}
%{_libdir}/wine/olesvr32.%{winedll}
%{_libdir}/wine/olethk32.%{winedll}
%{_libdir}/wine/opcservices.dll.so
%{_libdir}/wine/packager.%{winedll}
%{_libdir}/wine/pdh.%{winedll}
%{_libdir}/wine/photometadatahandler.%{winedll}
%{_libdir}/wine/pidgen.%{winedll}
%{_libdir}/wine/powrprof.%{winedll}
%{_libdir}/wine/presentationfontcache.%{wineexe}
%{_libdir}/wine/printui.%{winedll}
%{_libdir}/wine/prntvpt.%{winedll}
%{_libdir}/wine/propsys.%{winedll}
%{_libdir}/wine/psapi.%{winedll}
%{_libdir}/wine/pstorec.%{winedll}
%{_libdir}/wine/qcap.dll.so
%{_libdir}/wine/qedit.%{winedll}
%{_libdir}/wine/qmgr.%{winedll}
%{_libdir}/wine/qmgrprxy.%{winedll}
%{_libdir}/wine/quartz.%{winedll}
%{_libdir}/wine/query.%{winedll}
%{_libdir}/wine/qwave.%{winedll}
%{_libdir}/wine/rasapi32.%{winedll}
%{_libdir}/wine/rasdlg.%{winedll}
%{_libdir}/wine/regapi.%{winedll}
%{_libdir}/wine/resutils.%{winedll}
%{_libdir}/wine/riched20.%{winedll}
%{_libdir}/wine/riched32.%{winedll}
%{_libdir}/wine/rpcrt4.%{winedll}
%{_libdir}/wine/rsabase.%{winedll}
%{_libdir}/wine/rsaenh.%{winedll}
%{_libdir}/wine/rstrtmgr.%{winedll}
%{_libdir}/wine/rtutils.%{winedll}
%{_libdir}/wine/samlib.%{winedll}
%{_libdir}/wine/sapi.%{winedll}
%{_libdir}/wine/sas.%{winedll}
%{_libdir}/wine/sc.%{wineexe}
%{_libdir}/wine/scarddlg.%{winedll}
%{_libdir}/wine/sccbase.%{winedll}
%{_libdir}/wine/schannel.%{winedll}
%{_libdir}/wine/scrobj.%{winedll}
%{_libdir}/wine/scrrun.%{winedll}
%{_libdir}/wine/scsiport.%{winesys}
%{_libdir}/wine/secur32.dll.so
%{_libdir}/wine/sensapi.%{winedll}
%{_libdir}/wine/serialui.%{winedll}
%{_libdir}/wine/setupapi.%{winedll}
%{_libdir}/wine/sfc_os.%{winedll}
%{_libdir}/wine/shcore.%{winedll}
%{_libdir}/wine/shdoclc.%{winedll}
%{_libdir}/wine/shdocvw.%{winedll}
%{_libdir}/wine/schedsvc.%{winedll}
%{_libdir}/wine/shell32.dll.so
%{_libdir}/wine/shfolder.%{winedll}
%{_libdir}/wine/shlwapi.%{winedll}
%{_libdir}/wine/shutdown.%{wineexe}
%{_libdir}/wine/slbcsp.%{winedll}
%{_libdir}/wine/slc.%{winedll}
%{_libdir}/wine/snmpapi.%{winedll}
%{_libdir}/wine/softpub.%{winedll}
%{_libdir}/wine/spoolsv.%{wineexe}
%{_libdir}/wine/srclient.%{winedll}
%{_libdir}/wine/sspicli.%{winedll}
%{_libdir}/wine/stdole2.%{winetlb}
%{_libdir}/wine/stdole32.%{winetlb}
%{_libdir}/wine/sti.%{winedll}
%{_libdir}/wine/strmdll.%{winedll}
%{_libdir}/wine/subst.%{wineexe}
%{_libdir}/wine/svchost.%{wineexe}
%{_libdir}/wine/svrapi.%{winedll}
%{_libdir}/wine/sxs.%{winedll}
%{_libdir}/wine/systeminfo.%{wineexe}
%{_libdir}/wine/t2embed.%{winedll}
%{_libdir}/wine/tapi32.%{winedll}
%{_libdir}/wine/taskkill.%{wineexe}
%{_libdir}/wine/taskschd.%{winedll}
%{_libdir}/wine/tdh.%{winedll}
%{_libdir}/wine/tdi.%{winesys}
%{_libdir}/wine/traffic.%{winedll}
%{_libdir}/wine/tzres.%{winedll}
%{_libdir}/wine/ucrtbase.dll.so
%if 0%{?wine_staging}
%{_libdir}/wine/uianimation.%{winedll}
%endif
%{_libdir}/wine/uiautomationcore.%{winedll}
%{_libdir}/wine/uiribbon.%{winedll}
%{_libdir}/wine/unicows.%{winedll}
%{_libdir}/wine/unlodctr.%{wineexe}
%{_libdir}/wine/updspapi.%{winedll}
%{_libdir}/wine/url.%{winedll}
%{_libdir}/wine/urlmon.%{winedll}
%{_libdir}/wine/usbd.%{winesys}
%{_libdir}/wine/user32.dll.so
%{_libdir}/wine/usp10.%{winedll}
%{_libdir}/wine/utildll.%{winedll}
%{_libdir}/wine/uxtheme.dll.so
%{_libdir}/wine/userenv.%{winedll}
%{_libdir}/wine/vbscript.%{winedll}
%{_libdir}/wine/vcomp.%{winedll}
%{_libdir}/wine/vcomp90.%{winedll}
%{_libdir}/wine/vcomp100.%{winedll}
%{_libdir}/wine/vcomp110.%{winedll}
%{_libdir}/wine/vcomp120.%{winedll}
%{_libdir}/wine/vcomp140.%{winedll}
%{_libdir}/wine/vcruntime140.%{winedll}
%{_libdir}/wine/vdmdbg.%{winedll}
%{_libdir}/wine/version.%{winedll}
%{_libdir}/wine/virtdisk.%{winedll}
%{_libdir}/wine/vssapi.%{winedll}
%{_libdir}/wine/vulkan-1.%{winedll}
%{_libdir}/wine/wbemdisp.%{winedll}
%{_libdir}/wine/wbemprox.%{winedll}
%{_libdir}/wine/wdscore.%{winedll}
%{_libdir}/wine/webservices.%{winedll}
%{_libdir}/wine/wer.%{winedll}
%{_libdir}/wine/wevtapi.%{winedll}
%{_libdir}/wine/wiaservc.%{winedll}
%{_libdir}/wine/wimgapi.%{winedll}
%if 0%{?wine_staging}
%{_libdir}/wine/win32k.%{winesys}
%endif
%{_libdir}/wine/windowscodecs.dll.so
%{_libdir}/wine/windowscodecsext.%{winedll}
%{_libdir}/wine/winebus.sys.so
%{_libdir}/wine/winegstreamer.dll.so
%{_libdir}/wine/winehid.%{winesys}
%{_libdir}/wine/winejoystick.drv.so
%{_libdir}/wine/winemapi.%{winedll}
%{_libdir}/wine/winevulkan.dll.so
%{_libdir}/wine/winex11.drv.so
%{_libdir}/wine/wing32.%{winedll}
%{_libdir}/wine/winhttp.dll.so
%{_libdir}/wine/wininet.dll.so
%{_libdir}/wine/winmm.%{winedll}
%{_libdir}/wine/winnls32.%{winedll}
%{_libdir}/wine/winspool.drv.so
%{_libdir}/wine/winsta.%{winedll}
%{_libdir}/wine/wlanui.%{winedll}
%{_libdir}/wine/wmasf.%{winedll}
%{_libdir}/wine/wmi.%{winedll}
%{_libdir}/wine/wmic.%{wineexe}
%{_libdir}/wine/wmiutils.%{winedll}
%{_libdir}/wine/wmp.%{winedll}
%{_libdir}/wine/wmvcore.%{winedll}
%{_libdir}/wine/spoolss.%{winedll}
%{_libdir}/wine/winscard.%{winedll}
%{_libdir}/wine/wintab32.%{winedll}
%{_libdir}/wine/wintrust.%{winedll}
%{_libdir}/wine/winusb.%{winedll}
%{_libdir}/wine/wlanapi.%{winedll}
%{_libdir}/wine/wmphoto.%{winedll}
%{_libdir}/wine/wnaspi32.dll.so
%if 0%{?wine_staging}
%{_libdir}/wine/wow64cpu.dll.so
%endif
%{_libdir}/wine/wpc.%{winedll}
%{_libdir}/wine/wpcap.dll.so
%{_libdir}/wine/ws2_32.dll.so
%{_libdir}/wine/wsdapi.%{winedll}
%{_libdir}/wine/wshom.%{wineocx}
%{_libdir}/wine/wsnmp32.%{winedll}
%{_libdir}/wine/wsock32.%{winedll}
%{_libdir}/wine/wtsapi32.%{winedll}
%{_libdir}/wine/wuapi.%{winedll}
%{_libdir}/wine/wuaueng.%{winedll}
%if 0%{?wine_staging}
%{_libdir}/wine/wuauserv.%{wineexe}
%endif
%{_libdir}/wine/security.%{winedll}
%{_libdir}/wine/sfc.%{winedll}
%{_libdir}/wine/wineps.%{winedrv}
%{_libdir}/wine/d3d8.%{winedll}
%{_libdir}/wine/d3d9.%{winedll}
%{_libdir}/wine/opengl32.dll.so
%{_libdir}/wine/wined3d.dll.so
%{_libdir}/wine/dnsapi.dll.so
%{_libdir}/wine/iexplore.%{wineexe}
%{_libdir}/wine/xactengine3_0.dll.so
%{_libdir}/wine/xactengine3_1.dll.so
%{_libdir}/wine/xactengine3_2.dll.so
%{_libdir}/wine/xactengine3_3.dll.so
%{_libdir}/wine/xactengine3_4.dll.so
%{_libdir}/wine/xactengine3_5.dll.so
%{_libdir}/wine/xactengine3_6.dll.so
%{_libdir}/wine/xactengine3_7.dll.so
%{_libdir}/wine/x3daudio1_0.dll.so
%{_libdir}/wine/x3daudio1_1.dll.so
%{_libdir}/wine/x3daudio1_2.dll.so
%{_libdir}/wine/x3daudio1_3.dll.so
%{_libdir}/wine/x3daudio1_4.dll.so
%{_libdir}/wine/x3daudio1_5.dll.so
%{_libdir}/wine/x3daudio1_6.dll.so
%{_libdir}/wine/x3daudio1_7.dll.so
%{_libdir}/wine/xapofx1_1.dll.so
%{_libdir}/wine/xapofx1_2.dll.so
%{_libdir}/wine/xapofx1_3.dll.so
%{_libdir}/wine/xapofx1_4.dll.so
%{_libdir}/wine/xapofx1_5.dll.so
%{_libdir}/wine/xaudio2_0.dll.so
%{_libdir}/wine/xaudio2_1.dll.so
%{_libdir}/wine/xaudio2_2.dll.so
%{_libdir}/wine/xaudio2_3.dll.so
%{_libdir}/wine/xaudio2_4.dll.so
%{_libdir}/wine/xaudio2_5.dll.so
%{_libdir}/wine/xaudio2_6.dll.so
%{_libdir}/wine/xaudio2_7.dll.so
%{_libdir}/wine/xaudio2_8.dll.so
%{_libdir}/wine/xaudio2_9.dll.so
%{_libdir}/wine/xcopy.%{wineexe}
%{_libdir}/wine/xinput1_1.%{winedll}
%{_libdir}/wine/xinput1_2.%{winedll}
%{_libdir}/wine/xinput1_3.%{winedll}
%{_libdir}/wine/xinput1_4.%{winedll}
%{_libdir}/wine/xinput9_1_0.%{winedll}
%{_libdir}/wine/xmllite.%{winedll}
%{_libdir}/wine/xolehlp.%{winedll}
%{_libdir}/wine/xpsprint.%{winedll}
%{_libdir}/wine/xpssvcs.%{winedll}

%if 0%{?wine_staging}
%ifarch x86_64 aarch64
%{_libdir}/wine/nvapi64.dll.so
%{_libdir}/wine/nvencodeapi64.dll.so
%else
%{_libdir}/wine/nvapi.dll.so
%{_libdir}/wine/nvencodeapi.dll.so
%endif
%endif

# 16 bit and other non 64bit stuff
%ifnarch x86_64 %{arm} aarch64
%{_libdir}/wine/winevdm.exe.so
%{_libdir}/wine/ifsmgr.%{winevxd}
%{_libdir}/wine/mmdevldr.%{winevxd}
%{_libdir}/wine/monodebg.%{winevxd}
%{_libdir}/wine/rundll.%{wineexe16}
%{_libdir}/wine/vdhcp.%{winevxd}
%{_libdir}/wine/user.%{wineexe16}
%{_libdir}/wine/vmm.%{winevxd}
%{_libdir}/wine/vnbt.%{winevxd}
%{_libdir}/wine/vnetbios.%{winevxd}
%{_libdir}/wine/vtdapi.%{winevxd}
%{_libdir}/wine/vwin32.%{winevxd}
%{_libdir}/wine/w32skrnl.%{winedll}
%{_libdir}/wine/avifile.%{winedll16}
%{_libdir}/wine/comm.%{winedrv16}
%{_libdir}/wine/commdlg.%{winedll16}
%{_libdir}/wine/compobj.%{winedll16}
%{_libdir}/wine/ctl3d.%{winedll16}
%{_libdir}/wine/ctl3dv2.%{winedll16}
%{_libdir}/wine/ddeml.%{winedll16}
%{_libdir}/wine/dispdib.%{winedll16}
%{_libdir}/wine/display.%{winedrv16}
%{_libdir}/wine/gdi.exe16.so
%{_libdir}/wine/imm.%{winedll16}
%{_libdir}/wine/krnl386.exe16.so
%{_libdir}/wine/keyboard.%{winedrv16}
%{_libdir}/wine/lzexpand.%{winedll16}
%{_libdir}/wine/mmsystem.%{winedll16}
%{_libdir}/wine/mouse.%{winedrv16}
%{_libdir}/wine/msacm.%{winedll16}
%{_libdir}/wine/msvideo.%{winedll16}
%{_libdir}/wine/ole2.%{winedll16}
%{_libdir}/wine/ole2conv.%{winedll16}
%{_libdir}/wine/ole2disp.%{winedll16}
%{_libdir}/wine/ole2nls.%{winedll16}
%{_libdir}/wine/ole2prox.%{winedll16}
%{_libdir}/wine/ole2thk.%{winedll16}
%{_libdir}/wine/olecli.%{winedll16}
%{_libdir}/wine/olesvr.%{winedll16}
%{_libdir}/wine/rasapi16.%{winedll16}
%{_libdir}/wine/setupx.%{winedll16}
%{_libdir}/wine/shell.%{winedll16}
%{_libdir}/wine/sound.%{winedrv16}
%{_libdir}/wine/storage.%{winedll16}
%{_libdir}/wine/stress.%{winedll16}
%{_libdir}/wine/system.%{winedrv16}
%{_libdir}/wine/toolhelp.%{winedll16}
%{_libdir}/wine/twain.%{winedll16}
%{_libdir}/wine/typelib.%{winedll16}
%{_libdir}/wine/ver.%{winedll16}
%{_libdir}/wine/w32sys.%{winedll16}
%{_libdir}/wine/win32s16.%{winedll16}
%{_libdir}/wine/win87em.%{winedll16}
%{_libdir}/wine/winaspi.dll16.so
%{_libdir}/wine/windebug.%{winedll16}
%{_libdir}/wine/wineps16.%{winedrv16}
%{_libdir}/wine/wing.%{winedll16}
%{_libdir}/wine/winhelp.%{wineexe16}
%{_libdir}/wine/winnls.%{winedll16}
%{_libdir}/wine/winoldap.%{winemod16}
%{_libdir}/wine/winsock.%{winedll16}
%{_libdir}/wine/wintab.%{winedll16}
%{_libdir}/wine/wow32.%{winedll}
%endif

%files filesystem
%doc COPYING.LIB
%dir %{_datadir}/wine
%dir %{_datadir}/wine/gecko
%dir %{_datadir}/wine/mono
%dir %{_datadir}/wine/fonts
%{_datadir}/wine/wine.inf
%{_datadir}/wine/winebus.inf
%{_datadir}/wine/winehid.inf
%{_datadir}/wine/l_intl.nls

%files common
%{_bindir}/notepad
%{_bindir}/winedbg
%{_bindir}/winefile
%{_bindir}/winemine
%{_bindir}/winemaker
%{_bindir}/winepath
%{_bindir}/msiexec
%{_bindir}/regedit
%{_bindir}/regsvr32
%{_bindir}/wineboot
%{_bindir}/wineconsole
%{_bindir}/winecfg
%{_mandir}/man1/wine.1*
%{_mandir}/man1/wineserver.1*
%{_mandir}/man1/msiexec.1*
%{_mandir}/man1/notepad.1*
%{_mandir}/man1/regedit.1*
%{_mandir}/man1/regsvr32.1*
%{_mandir}/man1/wineboot.1*
%{_mandir}/man1/winecfg.1*
%{_mandir}/man1/wineconsole.1*
%{_mandir}/man1/winefile.1*
%{_mandir}/man1/winemine.1*
%{_mandir}/man1/winepath.1*
%lang(de) %{_mandir}/de.UTF-8/man1/wine.1*
%lang(de) %{_mandir}/de.UTF-8/man1/wineserver.1*
%lang(fr) %{_mandir}/fr.UTF-8/man1/wine.1*
%lang(fr) %{_mandir}/fr.UTF-8/man1/wineserver.1*
%lang(pl) %{_mandir}/pl.UTF-8/man1/wine.1*

%files fonts
# meta package

%if 0%{?wine_staging}
%files arial-fonts
%doc COPYING.LIB
%{_datadir}/wine/fonts/arial*
%endif

%files courier-fonts
%doc COPYING.LIB
%{_datadir}/wine/fonts/cou*

%files fixedsys-fonts
%doc COPYING.LIB
%{_datadir}/wine/fonts/*vgafix.fon

%files system-fonts
%doc COPYING.LIB
%{_datadir}/wine/fonts/cvgasys.fon
%{_datadir}/wine/fonts/hvgasys.fon
%{_datadir}/wine/fonts/jvgasys.fon
%{_datadir}/wine/fonts/svgasys.fon
%{_datadir}/wine/fonts/vgas1255.fon
%{_datadir}/wine/fonts/vgas1256.fon
%{_datadir}/wine/fonts/vgas1257.fon
%{_datadir}/wine/fonts/vgas874.fon
%{_datadir}/wine/fonts/vgasys.fon
%{_datadir}/wine/fonts/vgasyse.fon
%{_datadir}/wine/fonts/vgasysg.fon
%{_datadir}/wine/fonts/vgasysr.fon
%{_datadir}/wine/fonts/vgasyst.fon

%files small-fonts
%doc COPYING.LIB
%{_datadir}/wine/fonts/sma*
%{_datadir}/wine/fonts/jsma*

%files marlett-fonts
%doc COPYING.LIB
%{_datadir}/wine/fonts/marlett.ttf

%files ms-sans-serif-fonts
%doc COPYING.LIB
%{_datadir}/wine/fonts/sse*
%if 0%{?wine_staging}
%{_datadir}/wine/fonts/msyh.ttf
%endif

%files tahoma-fonts
%doc COPYING.LIB
%{_datadir}/wine/fonts/tahoma*ttf

%files tahoma-fonts-system
%doc README-tahoma
%{_datadir}/fonts/wine-tahoma-fonts
%{_fontconfig_confdir}/20-wine-tahoma*conf
%{_fontconfig_templatedir}/20-wine-tahoma*conf

%if 0%{?wine_staging}
%files times-new-roman-fonts
%doc COPYING.LIB
%{_datadir}/wine/fonts/times.ttf

%files times-new-roman-fonts-system
%{_datadir}/fonts/wine-times-new-roman-fonts
%endif

%files symbol-fonts
%doc COPYING.LIB
%{_datadir}/wine/fonts/symbol.ttf

%files wingdings-fonts
%doc COPYING.LIB
%{_datadir}/wine/fonts/wingding.ttf

%files wingdings-fonts-system
%{_datadir}/fonts/wine-wingdings-fonts

%files desktop
%{_datadir}/applications/wine-iexplore.desktop
%{_datadir}/applications/wine-inetcpl.desktop
%{_datadir}/applications/wine-joycpl.desktop
%{_datadir}/applications/wine-taskmgr.desktop
%{_datadir}/applications/wine-notepad.desktop
%{_datadir}/applications/wine-winefile.desktop
%{_datadir}/applications/wine-winemine.desktop
%{_datadir}/applications/wine-mime-msi.desktop
%{_datadir}/applications/wine.desktop
%{_datadir}/applications/wine-regedit.desktop
%{_datadir}/applications/wine-uninstaller.desktop
%{_datadir}/applications/wine-winecfg.desktop
%{_datadir}/applications/wine-wineboot.desktop
%{_datadir}/applications/wine-winhelp.desktop
%{_datadir}/applications/wine-wordpad.desktop
%{_datadir}/applications/wine-oleview.desktop
%{_datadir}/desktop-directories/Wine.directory
%config %{_sysconfdir}/xdg/menus/applications-merged/wine.menu
%{_datadir}/icons/hicolor/*/apps/*png
%{_datadir}/icons/hicolor/scalable/apps/*svg

%files systemd
%config %{_binfmtdir}/wine.conf

%if 0%{?rhel} == 6
%files sysvinit
%{_initrddir}/wine
%endif

# ldap subpackage
%files ldap
%{_libdir}/wine/wldap32.dll.so

# cms subpackage
%files cms
%{_libdir}/wine/mscms.dll.so

# twain subpackage
%files twain
%{_libdir}/wine/twain_32.%{winedll}
%{_libdir}/wine/sane.ds.so

# capi subpackage
%files capi
%{_libdir}/wine/capi2032.dll.so

%files devel
%{_bindir}/function_grep.pl
%{_bindir}/widl
%{_bindir}/winebuild
%{_bindir}/winecpp
%{_bindir}/winedump
%{_bindir}/wineg++
%{_bindir}/winegcc
%{_bindir}/winemaker
%{_bindir}/wmc
%{_bindir}/wrc
%{_mandir}/man1/widl.1*
%{_mandir}/man1/winebuild.1*
%{_mandir}/man1/winecpp.1*
%{_mandir}/man1/winedump.1*
%{_mandir}/man1/winegcc.1*
%{_mandir}/man1/winemaker.1*
%{_mandir}/man1/wmc.1*
%{_mandir}/man1/wrc.1*
%{_mandir}/man1/winedbg.1*
%{_mandir}/man1/wineg++.1*
%lang(de) %{_mandir}/de.UTF-8/man1/winemaker.1*
%lang(fr) %{_mandir}/fr.UTF-8/man1/winemaker.1*
%attr(0755, root, root) %dir %{_includedir}/wine
%{_includedir}/wine/*
%{_libdir}/*.so
%{_libdir}/wine/*.a
%{_libdir}/wine/*.def

%files pulseaudio
%{_libdir}/wine/winepulse.drv.so

%files alsa
%{_libdir}/wine/winealsa.drv.so

%files openal
%{_libdir}/wine/openal32.dll.so

%files opencl
%{_libdir}/wine/opencl.dll.so


%changelog
* Thu Nov 07 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.19-104
- Revert to release

* Thu Nov 07 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.19-103.20191106gitf205838
- Try to fix last one

* Wed Nov 06 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.19-102.20191105git7f469b6
- New snapshot
- Patchsets review. All extra patches applied only with staging

* Mon Nov 04 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.19-101
- Update revert list

* Sat Nov 02 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.19-100
- 4.19

* Sat Oct 19 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.18-100
- 4.18

* Mon Oct 14 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.17-103.20191009git71e96bd
- New snapshot
- R: gstreamer1-plugins-good

* Thu Oct 03 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.17-102.20191002git5e8eb5f
- Snapshot

* Sun Sep 29 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.17-101
- tkg updates and some reverts

* Sat Sep 28 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.17-100
- 4.17
- Retire deprecated isdn4k-utils support

* Wed Sep 25 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.16-102
- tkg updates

* Sun Sep 15 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.16-101
- tkg updates

* Sat Sep 14 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.16-100
- 4.16
- raw-input switch

* Sun Sep 08 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.15-101
- Disable raw-input

* Sat Aug 31 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.15-100
- 4.15

* Tue Aug 27 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.14-103
- tkg updates

* Fri Aug 23 2019 Phantom X <megaphantomx at bol dot com dot br>  - 1:4.14-102
- tkg updates

* Mon Aug 19 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.14-101
- Missing patch
- Deprecate old unmaintained patches

* Sat Aug 17 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.14-100
- 4.14

* Fri Aug 09 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.13-101
- Upstream and tkg updates
- Mono update

* Sat Aug 03 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.13-100
- 4.13

* Tue Jul 30 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.12.1-105
- Staging and tkg updates

* Fri Jul 19 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.12.1-104
- Try again

* Thu Jul 18 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.12.1-103
- Something broke

* Wed Jul 17 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.12.1-102
- Update staging patchset
- Raw input fix by Guy1524

* Sun Jul 07 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.12.1-101
- mingw build
- gtk3 switch, disabled by default

* Sun Jul 07 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.12.1-100
- 4.12.1

* Sat Jul 06 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.12-100
- 4.12
- f30 sync

* Sat Jun 22 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.11-100
- 4.11

* Sat Jun 15 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.10-101
- Monotonic patch update from tkg

* Mon Jun 10 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.10-100
- 4.10

* Fri May 31 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.9-101
- Some fixes from bugzilla

* Sat May 25 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.9-100
- 4.9

* Tue May 14 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.8-102
- Trim down reverts
- Update staging
- chinforpms experimental message and README
- Trim changelog

* Sat May 11 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.8-101
- Revert some upstream patches to fix joystick issues
- Revert staging patch to fix symlink issues

* Sat May 11 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.8-100
- 4.8

* Thu May 02 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.7-101
- no-PIC flags patches from upstream

* Mon Apr 29 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.7-100
- 4.7

* Thu Apr 18 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.6-101
- wine-mono 4.8.2

* Sun Apr 14 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.6-100
- 4.6
- esync merged with staging

* Sat Mar 30 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.5-100
- 4.5

* Wed Mar 27 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.4-103
- Revert xaudio2_7 application name patch, new one fail

* Wed Mar 27 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.4-102
- Replace xaudio2_7 application name with pulseaudio patch

* Mon Mar 25 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.4-101
- Some FAudio updates from Valve git

* Sun Mar 17 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.4-100
- 4.4

* Mon Mar 11 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.3-101
- Upstream fixes for whq#42982 and whq#43071

* Sun Mar 03 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.3-100
- 4.3
- pkgconfig style BRs
- Upstream FAudio support

* Mon Feb 18 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.2-101
- faudio update from tkg

* Sun Feb 17 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.2-100
- 4.2
- Add -ftree-vectorize -ftree-slp-vectorize to CFLAGS

* Mon Feb 04 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.1-100
- 4.1

* Fri Jan 25 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.0-101
- Optional enabled FAudio support. Obsoletes wine-xaudio and wine-freeworld
- Remove old Fedora and RH conditionals, only current Fedora is supported

* Tue Jan 22 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.0-100
- 4.0

* Mon Jan 21 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.0~rc7-101
- Patch to fix wine-dxup build

* Sat Jan 19 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.0~rc7-100
- 4.0-rc7

* Sat Jan 12 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.0~rc6-100
- 4.0-rc6
- Revert -O1 optimizations, seems good now
- Disable mime type registering

* Mon Jan 07 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.0~rc5-101
- Fix includedir

* Sat Jan 05 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:4.0~rc5-100
- 4.0-rc5

* Sun Dec 30 2018 Phantom X <megaphantomx at bol dot com dot br> - 4.0~rc4-100
- 4.0-rc4

* Sat Dec 22 2018 Phantom X <megaphantomx at bol dot com dot br> - 4.0~rc3-100
- 4.0-rc3

* Tue Dec 18 2018 Phantom X <megaphantomx at bol dot com dot br> - 4.0~rc2-101
- Some Tk-Glitch patches, including optional esync

* Mon Dec 17 2018 Phantom X <megaphantomx at bol dot com dot br> - 4.0~rc2-100
- 4.0-rc2

* Sat Dec 08 2018 Phantom X <megaphantomx at bol dot com dot br> - 4.0~rc1-100
- 4.0-rc1

* Tue Dec 04 2018 Phantom X <megaphantomx at bol dot com dot br> - 3.21-100
- 3.21
- Disable broken wine-pba
- Change rc versioning to "~" system

* Fri Nov 16 2018 Phantom X <megaphantomx at bol dot com dot br> - 3.20-100.chinfo
- 3.20

* Mon Oct 29 2018 Phantom X <megaphantomx at bol dot com dot br> - 3.19-100.chinfo
- 3.19

* Sun Oct 14 2018 Phantom X <megaphantomx at bol dot com dot br> - 3.18-100.chinfo
- 3.18

* Sun Sep 30 2018 Phantom X <megaphantomx at bol dot com dot br> - 3.17-100.chinfo
- 3.17

* Thu Sep 13 2018 Phantom X <megaphantomx at bol dot com dot br> - 3.16-100.chinfo
- 3.16

* Thu Sep 13 2018 Phantom X <megaphantomx at bol dot com dot br> - 3.15-104.chinfo
- More upstream fixes
- Change compiler optimizations to -O1 to fix whq#45199

* Sat Sep 08 2018 Phantom X <megaphantomx at bol dot com dot br> - 3.15-103.chinfo
- Try again again

* Fri Sep 07 2018 Phantom X <megaphantomx at bol dot com dot br> - 3.15-102.chinfo
- Try again

* Thu Sep 06 2018 Phantom X <megaphantomx at bol dot com dot br> - 3.15-101.chinfo
- Random upstream patches

* Sun Sep 02 2018 Phantom X <megaphantomx at bol dot com dot br> - 3.15-100.chinfo
- 3.15

* Mon Aug 27 2018 Phantom X <megaphantomx at bol dot com dot br> - 3.14-103.chinfo
- Revert pulseaudio fixes

* Mon Aug 27 2018 Phantom X <megaphantomx at bol dot com dot br> - 3.14-102.chinfo
- wine-pba patches
- Try new pulseaudio fixes
- license macros

* Fri Aug 24 2018 Phantom X <megaphantomx at bol dot com dot br> - 3.14-101.chinfo
- Virtual desktop fix

* Mon Aug 20 2018 Phantom X <megaphantomx at bol dot com dot br> - 3.14-100.chinfo
- 3.14

* Sun Aug 05 2018 Phantom X <megaphantomx at bol dot com dot br> - 3.13-102.chinfo
- Staging update

* Sun Jul 22 2018 Phantom X <megaphantomx at bol dot com dot br> - 3.13-101.chinfo
- Revert to old staging winepulse patches

* Sat Jul 21 2018 Phantom X <megaphantomx at bol dot com dot br> - 3.13-100.chinfo
- 3.13
- Clean xaudio2 package, only xaudio2_7.dll.so is needed

* Tue Jul 10 2018 Phantom X <megaphantomx at bol dot com dot br> - 3.12-100.chinfo
- 3.12
- Split xaudio2, for freeworld packages support

* Sun Jun 24 2018 Phantom X <megaphantomx at bol dot com dot br> - 3.11-100.chinfo
- 3.11

* Mon Jun 11 2018 Phantom X <megaphantomx at bol dot com dot br> - 3.10-100.chinfo
- 3.10

* Sat May 26 2018 Phantom X <megaphantomx at bol dot com dot br> - 3.9-100.chinfo
- 3.9
- BR: vkd3d-devel
- f28 sync

* Sat May 12 2018 Phantom X <megaphantomx at bol dot com dot br> - 3.8-100.chinfo
- 3.8

* Sat Apr 28 2018 Phantom X <megaphantomx at bol dot com dot br> - 3.7-100.chinfo
- 3.7

* Sun Apr 15 2018 Phantom X <megaphantomx at bol dot com dot br> - 3.6-102.chinfo
- Revert ARMv7 fix.

* Sun Apr 15 2018 Phantom X <megaphantomx at bol dot com dot br> - 3.6-101.chinfo
- f28 sync

* Sat Apr 14 2018 Phantom X <megaphantomx at bol dot com dot br> - 3.6-100.chinfo
- 3.6

* Fri Apr 06 2018 Phantom X <megaphantomx at bol dot com dot br> - 3.5-100.chinfo
- 3.5

* Fri Mar 16 2018 Phantom X <megaphantomx at bol dot com dot br> - 3.4-100.chinfo
- 3.4

* Sun Mar 04 2018 Phantom X <megaphantomx at bol dot com dot br> - 3.3-100.chinfo
- 3.3
- Updated URLs
- New wine-staging URL
- s/compholio/staging/
- BR: samba-devel
- BR: SDL2-devel
- BR: vulkan-devel
- R: samba-libs

* Tue Nov 21 2017 Phantom X <megaphantomx at bol dot com dot br> - 2.21-100.chinfo
- 2.21
- Drop nine, it have proper separated wine-nine package now
- Drop laino package, only one patch is needed
- Update patch list from AUR

* Mon Nov 06 2017 Phantom X <megaphantomx at bol dot com dot br> - 2.20-100.chinfo
- 2.20
- Rearrange files that are already in default wine from %%{?compholios} sections

* Mon Oct 23 2017 Phantom X <megaphantomx at bol dot com dot br> - 2.19-101.chinfo
- wine-d3d9 2.19

* Sat Oct 21 2017 Phantom X <megaphantomx at bol dot com dot br> - 2.19-100.chinfo
- 2.19

* Fri Oct 06 2017 Phantom X <megaphantomx at bol dot com dot br> - 2.18-101.chinfo
- BR: mesa-libEGL-devel with nine, fixes Fedora 27 build

* Thu Oct 05 2017 Phantom X <megaphantomx at bol dot com dot br> - 2.18-100.chinfo
- 2.18

* Wed Sep 20 2017 Phantom X <megaphantomx at bol dot com dot br> - 2.17-100.chinfo
- 2.17

* Thu Sep 07 2017 Phantom X <megaphantomx at bol dot com dot br> - 2.16-100.chinfo
- 2.16

* Wed Aug 23 2017 Phantom X <megaphantomx at bol dot com dot br> - 2.15-100.chinfo
- 2.15

* Thu Aug 10 2017 Phantom X <megaphantomx at bol dot com dot br> - 2.14-101.chinfo
- nine 2.14

* Tue Aug 08 2017 Phantom X <megaphantomx at bol dot com dot br> - 2.14-100.chinfo
- 2.14

* Tue Jul 25 2017 Phantom X <megaphantomx at bol dot com dot br> - 2.13-100.chinfo
- 2.13
- Disable laino patches

* Wed Jul 12 2017 Phantom X <megaphantomx at bol dot com dot br> - 2.12-100.chinfo
- 2.12

* Tue Jun 27 2017 Phantom X <megaphantomx at bol dot com dot br> - 2.11-100.chinfo
- 2.11

* Tue Jun 13 2017 Phantom X <megaphantomx at bol dot com dot br> - 2.10-100.chinfo
- 2.10
- laino patches

* Mon May 29 2017 Phantom X <megaphantomx at bol dot com dot br> - 2.9-100.chinfo
- 2.9

* Tue May 16 2017 Phantom X <megaphantomx at bol dot com dot br> - 2.8-100.chinfo
- 2.8

* Tue May 02 2017 Phantom X <megaphantomx at bol dot com dot br> - 2.7-100.chinfo
- 2.7

* Wed Apr 19 2017 Phantom X <megaphantomx at bol dot com dot br> - 2.6-100.chinfo
- 2.6

* Sun Apr 09 2017 Phantom X <megaphantomx at bol dot com dot br> - 2.5-100.chinfo
- 2.5

* Sun Mar 26 2017 Phantom X <megaphantomx at bol dot com dot br> - 2.4-101.chinfo
- Fix wine-mono version

* Tue Mar 21 2017 Phantom X <megaphantomx at bol dot com dot br> - 2.4-100.chinfo
- 2.4

* Mon Mar 06 2017 Phantom X <megaphantomx at bol dot com dot br> - 2.3-100.chinfo
- 2.3

* Wed Feb 22 2017 Phantom X <megaphantomx at bol dot com dot br> - 2.2-100.chinfo
- 2.2

* Thu Feb 09 2017 Phantom X <megaphantomx at bol dot com dot br> - 2.1-100.chinfo
- 2.1

* Wed Jan 25 2017 Phantom X <megaphantomx at bol dot com dot br> - 2.0-100.chinfo
- 2.0 final

* Mon Jan 23 2017 Phantom X <megaphantomx at bol dot com dot br> - 2.0-0.7.rc7.chinfo
- 2.0-rc6

* Mon Jan 16 2017 Phantom X <megaphantomx at bol dot com dot br> - 2.0-0.6.rc5.chinfo
- 2.0-rc5

* Mon Jan 09 2017 Phantom X <megaphantomx at bol dot com dot br> - 2.0-0.5.rc4.chinfo
- 2.0-rc4

* Wed Dec 28 2016 Phantom X <megaphantomx at bol dot com dot br> - 2.0-0.4.rc3.nine
- rebuilt

* Wed Dec 28 2016 Phantom X <megaphantomx at bol dot com dot br> - 2.0-0.3.rc3.nine
- Drop epoch.

* Wed Dec 28 2016 Phantom X <megaphantomx at bol dot com dot br> - 2.0-0.2.rc3.nine
- nine patches
- extra patches
- joy.cpl desktop file

* Tue Dec 27 2016 Michael Cronenworth <mike@cchtml.com> 2.0-0.1.rc3
- version update

* Wed Dec 21 2016 Michael Cronenworth <mike@cchtml.com> 2.0-0.1.rc2
- version update

* Thu Dec 15 2016 Michael Cronenworth <mike@cchtml.com> 2.0-0.1.rc1
- version update

* Wed Nov 23 2016 Michael Cronenworth <mike@cchtml.com> 1.9.23-2
- drop sysvinit on Fedora, again

* Wed Nov 16 2016 Michael Cronenworth <mike@cchtml.com> 1.9.23-1
- version update
- remove old cruft in spec
- add hard cups-libs dependency (rhbz#1367537)
- include mp3 support (rhbz#1395711)

* Thu Nov 03 2016 Michael Cronenworth <mike@cchtml.com> 1.9.22-1
- version update

* Mon Oct 17 2016 Michael Cronenworth <mike@cchtml.com> 1.9.21-1
- version update

* Sun Oct 02 2016 Michael Cronenworth <mike@cchtml.com> 1.9.20-1
- version update

* Mon Sep 19 2016 Michael Cronenworth <mike@cchtml.com> 1.9.19-1
- version update

* Thu Sep 15 2016 Peter Robinson <pbrobinson@fedoraproject.org> 1.9.18-2
- fix aarch64 definition

* Wed Sep 07 2016 Michael Cronenworth <mike@cchtml.com> 1.9.18-1
- version update

* Sun Aug 28 2016 Michael Cronenworth <mike@cchtml.com> 1.9.17-1
- version update

* Sat Aug 20 2016 Peter Robinson <pbrobinson@fedoraproject.org> 1.9.16-2
- build on aarch64

* Tue Aug 09 2016 Michael Cronenworth <mike@cchtml.com> 1.9.16-1
- version update

* Fri Jul 29 2016 Michael Cronenworth <mike@cchtml.com> 1.9.15-1
- version update

* Mon Jul 11 2016 Michael Cronenworth <mike@cchtml.com> 1.9.14-1
- version update

* Fri Jul 01 2016 Michael Cronenworth <mike@cchtml.com> 1.9.13-1
- version update

* Wed Jun 15 2016 Michael Cronenworth <mike@cchtml.com> 1.9.12-1
- version update

* Tue Jun 07 2016 Michael Cronenworth <mike@cchtml.com> 1.9.11-1
- version update

* Tue May 24 2016 Michael Cronenworth <mike@cchtml.com> 1.9.10-2
- gecko update

* Tue May 17 2016 Michael Cronenworth <mike@cchtml.com> 1.9.10-1
- version upgrade

* Sun May 01 2016 Michael Cronenworth <mike@cchtml.com> 1.9.9-1
- version upgrade

* Sun Apr 17 2016 Michael Cronenworth <mike@cchtml.com> 1.9.8-1
- version upgrade

* Sun Apr 03 2016 Michael Cronenworth <mike@cchtml.com> 1.9.7-1
- version upgrade

* Mon Mar 21 2016 Michael Cronenworth <mike@cchtml.com> 1.9.6-1
- version upgrade

* Tue Mar 08 2016 Michael Cronenworth <mike@cchtml.com> 1.9.5-2
- update mono requirement

* Tue Mar 08 2016 Michael Cronenworth <mike@cchtml.com> 1.9.5-1
- version upgrade

* Mon Feb 22 2016 Michael Cronenworth <mike@cchtml.com> 1.9.4-1
- version upgrade

* Mon Feb 08 2016 Michael Cronenworth <mike@cchtml.com> 1.9.3-1
- version upgrade

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sun Jan 24 2016 Michael Cronenworth <mike@cchtml.com> 1.9.2-1
- version upgrade
- enable gstreamer support

* Sun Jan 10 2016 Michael Cronenworth <mike@cchtml.com> 1.9.1-1
- version upgrade

* Mon Dec 28 2015 Michael Cronenworth <mike@cchtml.com> 1.9.0-1
- version upgrade

* Wed Dec 23 2015 Michael Cronenworth <mike@cchtml.com> 1.8-1
- version upgrade

* Tue Dec 15 2015 Michael Cronenworth <mike@cchtml.com> 1.8-0.2
- version upgrade, 1.8-rc4
- enabling compiler optimizations again (-O2), thanks to gcc 5.3

* Sun Dec 06 2015 Michael Cronenworth <mike@cchtml.com> 1.8-0.1
- version upgrade, 1.8-rc3

* Sun Nov 15 2015 Michael Cronenworth <mike@cchtml.com> 1.7.55-1
- version upgrade

* Wed Nov 04 2015 Michael Cronenworth <mike@cchtml.com> 1.7.54-1
- version upgrade

* Wed Oct 21 2015 Michael Cronenworth <mike@cchtml.com> 1.7.53-1
- version upgrade

* Sat Oct 03 2015 Michael Cronenworth <mike@cchtml.com> 1.7.52-1
- version upgrade

* Tue Sep 08 2015 Michael Cronenworth <mike@cchtml.com> 1.7.51-1
- version upgrade

* Mon Aug 24 2015 Michael Cronenworth <mike@cchtml.com> 1.7.50-1
- version upgrade

* Fri Aug 14 2015 Michael Cronenworth <mike@cchtml.com> 1.7.49-2
- backport gecko 2.40 patch

* Fri Aug 14 2015 Michael Cronenworth <mike@cchtml.com> 1.7.49-1
- version upgrade

* Mon Aug 10 2015 Björn Esser <bjoern.esser@gmail.com> - 1.7.48-2
- rebuilt for mingw-wine-gecko-2.40

* Fri Jul 31 2015 Michael Cronenworth <mike@cchtml.com> 1.7.48-1
- version upgrade

* Sun Jul 12 2015 Michael Cronenworth <mike@cchtml.com> 1.7.47-1
- version upgrade

* Mon Jun 29 2015 Michael Cronenworth <mike@cchtml.com> 1.7.46-1
- version upgrade

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.45-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 14 2015 Michael Cronenworth <mike@cchtml.com> 1.7.45-1
- version upgrade

* Sun May 31 2015 Michael Cronenworth <mike@cchtml.com> 1.7.44-1
- version upgrade

* Mon May 18 2015 Michael Cronenworth <mike@cchtml.com> 1.7.43-1
- version upgrade

* Mon May 04 2015 Michael Cronenworth <mike@cchtml.com> 1.7.42-1
- version upgrade

* Sat Apr 18 2015 Michael Cronenworth <mike@cchtml.com> 1.7.41-1
- version upgrade
- Disable gstreamer support (rhbz#1204185)

* Mon Apr 06 2015 Michael Cronenworth <mike@cchtml.com> 1.7.40-1
- version upgrade

* Sun Mar 22 2015 Michael Cronenworth <mike@cchtml.com> 1.7.39-1
- version upgrade
- Enable some optimizations and workarounds for GCC5 regressions

* Tue Mar 10 2015 Adam Jackson <ajax@redhat.com> 1.7.38-3
- Drop sysvinit subpackage on F23+

* Sat Mar 07 2015 Michael Cronenworth <mike@cchtml.com> - 1.7.38-2
- Fix wine-gecko and wine-mono versions

* Sat Mar 07 2015 Michael Cronenworth <mike@cchtml.com> - 1.7.38-1
- version upgrade

* Sun Feb 22 2015 Andreas Bierfert <andreas.bierfert@lowlatency.de>
- 1.7.37-1
- version upgrade

* Mon Feb 16 2015 Michael Cronenworth <mike@cchtml.com> - 1.7.36-2
- Patch for RtlUnwindEx fix (staging bz #68)
- Use new systemd macros for binfmt handling

* Sun Feb 08 2015 Michael Cronenworth <mike@cchtml.com> - 1.7.36-1
- version upgrade

* Wed Feb 04 2015 Orion Poplawski <orion@cora.nwra.com> - 1.7.35-3
- Add patch to fix stack smashing (bug #1110419)

* Mon Jan 26 2015 Michael Cronenworth <mike@cchtml.com> - 1.7.35-2
- Rebuild (libgphoto2)

* Sun Jan 25 2015 Michael Cronenworth <mike@cchtml.com> - 1.7.35-1
- version upgrade
- use alternatives system, remove wow sub-package

* Tue Jan 20 2015 Peter Robinson <pbrobinson@fedoraproject.org> 1.7.34-2
- Rebuild (libgphoto2)

* Sat Jan 10 2015 Michael Cronenworth <mike@cchtml.com>
- 1.7.34-1
- version upgrade
- enable OpenCL support (rhbz#1176605)

* Sun Dec 14 2014 Michael Cronenworth <mike@cchtml.com>
- 1.7.33-1
- version upgrade

* Sun Nov 30 2014 Michael Cronenworth <mike@cchtml.com>
- 1.7.32-1
- version upgrade
- wine-mono upgrade

* Fri Nov 14 2014 Andreas Bierfert <andreas.bierfert@lowlatency.de>
- 1.7.31-1
- version upgrade
- wine-gecko upgrade
- add some missing arch requires

* Sun Nov 02 2014 Andreas Bierfert <andreas.bierfert@lowlatency.de>
- 1.7.30-1
- version upgrade (rhbz#1159548)
- use winepulse patch from compholio patchset when build w/o
  compholio (rhbz#1151862)

* Fri Oct 24 2014 Michael Cronenworth <mike@cchtml.com>
- 1.7.29-1
- version upgrade

* Sun Oct 05 2014 Michael Cronenworth <mike@cchtml.com>
- 1.7.28-1
- version upgrade
- New sub-package for wingdings font system integration

* Wed Sep 24 2014 Michael Cronenworth <mike@cchtml.com>
- 1.7.27-1
- version upgrade

* Mon Sep 08 2014 Michael Cronenworth <mike@cchtml.com>
- 1.7.26-1
- version upgrade

* Sun Aug 24 2014 Michael Cronenworth <mike@cchtml.com>
- 1.7.25-1
- version upgrade

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.24-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Aug 15 2014 Michael Cronenworth <mike@cchtml.com>
- 1.7.24-1
- version upgrade
- No longer install Wine fonts into system directory (rhbz#1039763)

* Thu Jul 17 2014 Björn Esser <bjoern.esser@gmail.com> - 1.7.22-4
- prevent accidential build with compholio-patchset on EPEL
- rebuild for pulseaudio (bug #1117683)

* Mon Jul 14 2014 Björn Esser <bjoern.esser@gmail.com> - 1.7.22-3
- dropped virtual Provides: %%{name}(compholio)

* Sat Jul 12 2014 Björn Esser <bjoern.esser@gmail.com> - 1.7.22-2
- added conditionalized option to build with compholio-patchset for pipelight
  Source900 -- compholio-patchset, wine-arial-fonts sub-package,
  BR: libattr-devel and configure --with-xattr for Silverlight DRM-stuff

* Fri Jul 11 2014 Michael Cronenworth <mike@cchtml.com>
- 1.7.22-1
- version upgrade

* Wed Jul 09 2014 Michael Cronenworth <mike@cchtml.com>
- 1.7.21-2
- Fixes for EPEL7 (rhbz#1117422)

* Tue Jul 01 2014 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.7.21-1
- version upgrade

* Thu Jun 19 2014 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.7.20-1
- version upgrade

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.19-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun May 18 2014 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.7.19-1
- version upgrade

* Sat May 10 2014 Michael Cronenworth <mike@cchtml.com>
- 1.7.18-1
- version upgrade

* Fri Apr 25 2014 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.7.17-2
- fix systemd binfmt location (rhbz#1090170)

* Tue Apr 22 2014 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.7.17-1
- version upgrade

* Mon Apr 07 2014 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.7.16-2
- explicitly require libpng (fixes rhbz#1085075)

* Mon Apr 07 2014 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.7.16-1
- version upgrade

* Mon Mar 24 2014 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.7.15-1
- version upgrade

* Sat Mar 08 2014 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.7.14-1
- version upgrade

* Sun Feb 23 2014 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.7.13-1
- version upgrade
- upgraded winepulse

* Sat Feb 08 2014 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.7.12-1
- version upgrade

* Sun Jan 26 2014 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.7.11-1
- version upgrade

* Thu Jan 09 2014 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.7.10-1
- version upgrade
- upgraded winepulse
