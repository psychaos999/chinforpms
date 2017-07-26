Name:           belle-sip
Version:        1.6.3
Release:        1.chinfo%{?dist}
Summary:        Linphone SIP stack

License:        GPLv2+ and BSD and BSD with advertising and MIT
URL:            http://www.linphone.org/technical-corner/belle-sip/overview
Source0:        https://www.linphone.org/releases/sources/%{name}/%{name}-%{version}.tar.gz
Source1:        http://www.antlr3.org/download/antlr-3.4-complete.jar

BuildRequires:  antlr3-tool
BuildRequires:  antlr3-C-devel
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  java-headless
BuildRequires:  mbedtls-devel
BuildRequires:  libtool
BuildRequires:  pkgconfig(bctoolbox)
BuildRequires:  pkgconfig(zlib)

# The version is used from src/md5.c line:
# /* $Id: md5.c,v 1.6 2002/04/13 19:20:28 lpd Exp $ */
Provides: bundled(md5-deutsch) = 1.6

%description
Belle-sip is an object oriented C written SIP stack used by Linphone.

%package devel
Summary:       Development libraries for belle-sip
Requires:      %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description    devel
Libraries and headers required to develop software with belle-sip.

%prep
%autosetup -n %{name}-%{version}-0

# seds from Arch
sed -i \
  -e "s|-Werror||g" \
  configure.ac

autoreconf -ivf

pushd src/grammars/
java -Xmx256m -jar %{SOURCE1} -make -Xmultithreaded -Xconversiontimeout 10000 -fo . belle_sip_message.g
java -Xmx256m -jar %{SOURCE1} -make -Xmultithreaded -Xconversiontimeout 10000 -fo . belle_sdp.g
popd

%build
%configure \
  --disable-tests \
  --disable-silent-rules \
  --disable-static

sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

%make_build


%install
%make_install

find %{buildroot} -name '*.la' -delete

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%license COPYING
%doc README.md
%{_libdir}/libbellesip.so.*

%files devel
%{_includedir}/%{name}/*.h
%{_libdir}/libbellesip.so
%{_libdir}/pkgconfig/%{name}.pc

%changelog
* Tue Jul 25 2017 Phantom X <megaphantomx at bol dot com dot br> - 1.6.3-1.chinfo
- 1.6.3

* Tue Jun 20 2017 Phantom X <megaphantomx at bol dot com dot br> - 1.6.1-1.chinfo
- 1.6.1

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jul 19 2016 Alexey Kurov <nucleo@fedoraproject.org> - 1.4.2-2
- Fix typo in comparison code (patch from bug #1050744)

* Sat Nov  7 2015 Alexey Kurov <nucleo@fedoraproject.org> - 1.4.2-1
- belle-sip-1.4.2

* Sat Sep 19 2015 Alexey Kurov <nucleo@fedoraproject.org> - 1.4.1-2
- disabled TLS for F23+ (mbedtls 2 incompatible)

* Fri Sep  4 2015 Alexey Kurov <nucleo@fedoraproject.org> - 1.4.1-1
- belle-sip-1.4.1
- removed atlr3 3.4 SOURCE1
- added patch with files generated by antlr-3.4-complete.jar
- BR: mbedtls-devel instead of polarssl-devel

* Sun Feb 15 2015 Alexey Kurov <nucleo@fedoraproject.org> - 1.4.0-1
- belle-sip-1.4.0
- update Source0 URL
- use %%license macro

* Sun Feb 15 2015 Alexey Kurov <nucleo@fedoraproject.org> - 1.3.3-1
- belle-sip-1.3.3
- added atlr3 3.4 SOURCE1
- License: GPLv2+ and BSD and BSD with advertising and MIT
- Provides: bundled(md5-deutsch) = 1.6

* Fri Feb 21 2014 Alexey Kurov <nucleo@fedoraproject.org> - 1.3.0-1
- belle-sip-1.3.0
- revert fix FSF address in COPYING

* Sat Jan 18 2014 Alexey Kurov <nucleo@fedoraproject.org> - 1.2.4-3
- License: GPLv2+
- fix FSF address in COPYING

* Sun Jan 12 2014 Alexey Kurov <nucleo@fedoraproject.org> - 1.2.4-2
- add %%{?_isa} in -devel Requires
- add verbose option to autoreconf
- verbose build output

* Thu Jan  9 2014 Alexey Kurov <nucleo@fedoraproject.org> - 1.2.4-1
- Initial RPM release
