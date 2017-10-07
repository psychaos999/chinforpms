Name:           libmirage
Version:        3.1.0
Release:        1.chinfo%{?dist}
Summary:        A CD/DVD-ROM image access library

License:        GPLv2+
URL:            http://sourceforge.net/projects/cdemu
Source0:        http://downloads.sourceforge.net/cdemu/%{name}-%{version}.tar.bz2

BuildRequires:  cmake
BuildRequires:  pkgconfig(bzip2)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gobject-introspection-1.0)
BuildRequires:  pkgconfig(liblzma)
BuildRequires:  pkgconfig(samplerate)
BuildRequires:  pkgconfig(sndfile)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  gtk-doc
BuildRequires:  intltool

BuildRequires:  shared-mime-info
Requires(postun): shared-mime-info
Requires(posttrans): shared-mime-info

%description
The libMirage library is a CD/DVD-ROM image access library - it aims to
provide abstraction of data stored in various optical disc image formats.
It is part of CDEmu, a CD/DVD-ROM device emulator for Linux.

%package devel
Summary:        A CD/DVD-ROM image access library
Requires:       %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       gtk-doc

%description devel
The libMirage library is a CD/DVD-ROM image access library - it aims to
provide abstraction of data stored in various optical disc image formats.
It is part of CDEmu, a CD/DVD-ROM device emulator for Linux.

This package contains files needed to develop with libMirage.

%prep
%autosetup

%build
mkdir build
pushd build

%cmake .. \
  -DCMAKE_VERBOSE_MAKEFILE:BOOL=ON \
  -DPOST_INSTALL_HOOKS:BOOL=OFF

%make_build

popd

%install
%make_install -C build

%find_lang %{name}

%post
/sbin/ldconfig
touch --no-create %{_datadir}/mime/packages &>/dev/null || :

%postun
/sbin/ldconfig
if [ $1 -eq 0 ] ; then
  touch --no-create %{_datadir}/mime/packages &>/dev/null || :
  update-mime-database %{_datadir}/mime &>/dev/null || :
fi

%posttrans
update-mime-database %{?fedora:-n} %{_datadir}/mime &>/dev/null || :

%files -f %{name}.lang
%license COPYING
%doc AUTHORS README ChangeLog
%{_libdir}/libmirage.so.*
%{_libdir}/libmirage-*/*.so
%{_datadir}/mime/packages/*
%{_libdir}/girepository-1.0/*
%{_datadir}/gir-1.0/*

%files devel
%{_libdir}/lib*.so
%{_includedir}/*
%{_libdir}/pkgconfig/*
%doc %{_datadir}/gtk-doc/html/*

%changelog
* Fri Oct 06 2017 Phantom X <megaphantomx at bol dot com dot br> - 3.1.0-100.chinfo
- chinforpms release

* Sat Jun 10 2017 Rok Mandeljc <rok.mandeljc@gmail.com> - 3.1.0-1
- Updated to 3.1.0

* Sun Oct  9 2016 Rok Mandeljc <rok.mandeljc@gmail.com> - 3.0.5-1
- Updated to 3.0.5

* Sat Apr 23 2016 Rok Mandeljc <rok.mandeljc@gmail.com> - 3.0.4-2
- Fixed rpmlint errors and warnings

* Sat Nov 21 2015 Rok Mandeljc <rok.mandeljc@gmail.com> - 3.0.4-1
- Updated to 3.0.4
- Updated mime scripts

* Sun Nov  9 2014 Rok Mandeljc <rok.mandeljc@gmail.com> - 3.0.3-1
- Updated to 3.0.3

* Sun Sep 28 2014 Rok Mandeljc <rok.mandeljc@gmail.com> - 3.0.2-1
- Updated to 3.0.2

* Fri Jul 25 2014 Rok Mandeljc <rok.mandeljc@gmail.com> - 3.0.1-1
- Updated to 3.0.1

* Sun Jun 29 2014 Rok Mandeljc <rok.mandeljc@gmail.com> - 3.0.0-1
- Updated to 3.0.0

* Thu Sep 19 2013 Rok Mandeljc <rok.mandeljc@gmail.com> - 2.1.1-1
- Updated to 2.1.1

* Fri Jun  7 2013 Rok Mandeljc <rok.mandeljc@gmail.com> - 2.1.0-1
- Updated to 2.1.0

* Mon Dec 24 2012 Rok Mandeljc <rok.mandeljc@gmail.com> - 2.0.0-1
- RPM release for new version