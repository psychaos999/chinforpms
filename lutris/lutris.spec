Name:           lutris
Version:        0.4.20
Epoch:          1
Release:        1%{?dist}
Summary:        Install and play any video game easily

License:        GPL-3.0+
URL:            http://lutris.net

Source0:        http://lutris.net/releases/%{name}_%{version}.tar.xz

BuildArch:      noarch

BuildRequires:  desktop-file-utils
BuildRequires:  python3-devel
BuildRequires:  python3-gobject
BuildRequires:  python3-wheel
BuildRequires:  python3-setuptools
BuildRequires:  fdupes
Requires:       cabextract
Requires:       gtk3
Requires:       psmisc
Requires:       python3-gobject
Requires:       python3-PyYAML
Requires:       xorg-x11-server-Xephyr
Requires:       xorg-x11-server-utils
Recommends:     xboxdrv
Recommends:     wine
Suggests:       steam


%description
Lutris is a gaming platform for GNU/Linux. Its goal is to make
gaming on Linux as easy as possible by taking care of installing
and setting up the game for the user. The only thing you have to
do is play the game. It aims to support every game that is playable
on Linux.

%prep
%autosetup -n %{name}


%build
%py3_build


%install
%py3_install

rm -f %{buildroot}%{_datadir}/polkit-1/actions/net.lutris.xboxdrv*

%fdupes %{buildroot}%{python3_sitelib}

mv %{buildroot}%{_datadir}/appdata %{buildroot}%{_metainfodir}

desktop-file-edit \
  --add-category=GTK \
  %{buildroot}%{_datadir}/applications/%{name}.desktop
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop


%files
%license LICENSE
%doc AUTHORS README.rst
%{_bindir}/%{name}
%{_datadir}/%{name}/
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.*
%{_datadir}/polkit-1/actions/*.policy
%{python3_sitelib}/%{name}-*.egg-info
%{python3_sitelib}/%{name}/
%{_metainfodir}/*.appdata.xml


%changelog
* Fri Oct 05 2018 Phantom X <megaphantomx at bol dot com dot br> - 1:0.4.20-1
- 0.4.20

* Mon Sep 24 2018 Phantom X <megaphantomx at bol dot com dot br> - 0.4.19-5
- chinforpms cleanup

* Tue Nov 29 2016 Mathieu Comandon <strycore@gmail.com> - 0.4.3
- Ensure correct Python3 dependencies
- Set up Python macros for building (Thanks to Pharaoh_Atem on #opensuse-buildservice)

* Sat Oct 15 2016 Mathieu Comandon <strycore@gmail.com> - 0.4.0
- Update to Python 3
- Bump version to 0.4.0

* Sat Dec 12 2015 Rémi Verschelde <akien@mageia.org> - 0.3.7-2
- Remove ownership of system directories
- Spec file cleanup

* Fri Nov 27 2015 Mathieu Comandon <strycore@gmail.com> - 0.3.7-1
- Bump to version 0.3.7

* Thu Oct 30 2014 Mathieu Comandon <strycore@gmail.com> - 0.3.6-1
- Bump to version 0.3.6
- Add OpenSuse compatibility (contribution by @malkavi)

* Fri Sep 12 2014 Mathieu Comandon <strycore@gmail.com> - 0.3.5-1
- Bump version to 0.3.5

* Thu Aug 14 2014 Travis Nickles <nickles.travis@gmail.com> - 0.3.4-3
- Edited Requires to include pygobject3.

* Wed Jun 04 2014 Travis Nickles <nickles.travis@gmail.com> - 0.3.4-2
- Changed build and install step based on template generated by
  rpmdev-newspec.
- Added Requires.
- Ensure package can be built using mock.

* Tue Jun 03 2014 Travis Nickles <nickles.travis@gmail.com> - 0.3.4-1
- Initial version of the package
