%global __filter_GLIBC_PRIVATE 1

Name:           libstrangle
Version:        0.0.4
Release:        2%{?dist}
Summary:        Frame rate limiter

License:        GPLv3
URL:            https://gitlab.com/torkel104/%{name}
Source0:        %{url}/-/archive/%{version}/%{name}-%{version}.tar.bz2

Patch0:         %{url}/commit/4e6f3d6e5516c13774e73ff51141c8827dee9cf2.patch#/%{name}-gl-4e6f3d6e.patch

# Multilib friendly and cleanups for rpm packaging
Patch100:       %{name}-rpmbuild.patch
# Look for libdl.so.2
Patch101:       %{name}-libdl.patch

BuildRequires:  make
BuildRequires:  gcc


%description
%{summary}.


%prep
%autosetup -p1


%build
%set_build_flags
%make_build libdir=%{_libdir}


%install
%make_install libdir=%{_libdir}

rm -rf %{buildroot}%{_sysconfdir}


%files
%license COPYING
%doc README.md
%{_bindir}/strangle
%{_libdir}/%{name}/%{name}.so


%changelog
* Thu May 30 2019 Phantom X <megaphantomx at bol dot com dot br> - 0.0.4-2
- Remove unneeded ld.so.conf file

* Mon Feb 04 2019 Phantom X <megaphantomx at bol dot com dot br> - 0.0.4-1
- Initial spec
