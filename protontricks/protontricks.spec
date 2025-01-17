Name:           protontricks
Version:        1.4.3
Release:        1%{?dist}
Summary:        A simple wrapper that does winetricks things for Proton enabled games

License:        GPLv3
URL:            https://github.com/Matoking/protontricks
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz

Patch0:         %{url}/commit/c91bcc932d1892e7804869d3cb3dfb70846feaca.patch#/%{name}-gh-c91bcc9.patch
Patch10:        0001-Disable-setuptools_scm-version-check.patch

BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  %{py3_dist setuptools}
BuildRequires:  %{py3_dist vdf}
Requires:       %{py3_dist vdf}
Requires:       winetricks
Suggests:       zenity


%description
%{summary}.


%prep
%autosetup -p1

echo "version = '%{version}'" > src/protontricks/_version.py

%build
%py3_build


%install
%py3_install


%check
%{__python3} setup.py test


%files
%license LICENSE
%doc CONTRIBUTING.md README.md
%{_bindir}/%{name}
%{python3_sitelib}/%{name}
%{python3_sitelib}/*-*.egg-info


%changelog
* Mon Dec 28 2020 Phantom X <megaphantomx at hotmail dot com> - 1.4.3-1
- 1.4.3

* Wed Mar 18 2020 Phantom X <megaphantomx at bol dot com dot br> - 1.4.1-2
- 1.4.1

* Wed Feb 05 2020 Phantom X <megaphantomx at bol dot com dot br> - 1.4-1
- 1.4
- Remove git BR

* Sat Nov 09 2019 Phantom X <megaphantomx at bol dot com dot br> - 1.3-1
- 1.3

* Wed Sep 18 2019 Phantom X <megaphantomx at bol dot com dot br> - 1.2.5-1
- 1.2.5

* Wed Jul 31 2019 Phantom X <megaphantomx at bol dot com dot br> - 1.2.4-1
- Initial spec
