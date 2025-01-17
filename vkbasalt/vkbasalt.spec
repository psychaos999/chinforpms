%global commit 111b0e8cf4aed03b7513a21be8298719038173ce
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20210218
%global with_snapshot 1

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

%global pkgname vkBasalt

Name:           vkbasalt
Version:        0.3.2.4
Release:        1%{?gver}%{?dist}
Summary:        A vulkan post processing layer

License:        zlib
URL:            https://github.com/DadSchoorse/vkBasalt

%if 0%{?with_snapshot}
Source0:        %{url}/archive/%{commit}/%{pkgname}-%{shortcommit}.tar.gz
%else
Source0:        %{url}/releases/download/v%{version}/%{pkgname}-%{version}.tar.gz
%endif

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  glslang
BuildRequires:  meson
BuildRequires:  ninja-build
BuildRequires:  spirv-headers-devel
BuildRequires:  vulkan-headers
BuildRequires:  pkgconfig(x11)
Requires:       vulkan-loader%{?_isa}

Provides:       %{pkgname}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}


%description
vkBasalt is a Vulkan post processing layer to enhance the visual graphics of
games.


%prep
%if 0%{?with_snapshot}
%autosetup -n %{pkgname}-%{commit} -p1
%else
%autosetup -n %{pkgname}-%{version} -p1
%endif


%build
%meson \
  -Dappend_libdir_vkbasalt=true \
%{nil}

%meson_build


%install
%meson_install

mkdir -p %{buildroot}%{_datadir}/%{pkgname}


%files
%license LICENSE
%doc README.md config/vkBasalt.conf
%{_libdir}/%{name}/lib%{name}.so
%dir %{_datadir}/%{pkgname}
%{_datadir}/vulkan/implicit_layer.d/%{pkgname}.json


%changelog
* Sun Feb 28 2021 Phantom X <megaphantomx at hotmail dot com> - 0.3.2.4-1.20210218git111b0e8
- 0.3.2.4

* Sat Jan 09 2021 Phantom X <megaphantomx at hotmail dot com> - 0.3.2.3-1.20210108gitce647da
- 0.3.2.3

* Wed Oct 21 2020 Phantom X <megaphantomx at hotmail dot com> - 0.3.2.2-1.20201001gitca921c8
- Initial spec
