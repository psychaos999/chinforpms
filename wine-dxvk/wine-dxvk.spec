%undefine _hardened_build

%global winecommonver 3.10

%global pkgname dxvk

Name:           wine-%{pkgname}
Version:        0.95
Release:        2%{?dist}
Summary:        Vulkan-based D3D11 implementation for Linux / Wine

License:        zlib
URL:            https://github.com/doitsujin/%{pkgname}

Source0:        %{url}/archive/v%{version}/%{pkgname}-%{version}.tar.gz
Source1:        README.%{pkgname}
Source2:        wine%{pkgname}cfg

Patch0:         %{name}-optflags.patch

ExclusiveArch:  %{ix86} x86_64

BuildRequires:  gcc
BuildRequires:  gcc-c++

# glslangValidator
BuildRequires:  glslang
BuildRequires:  meson
BuildRequires:  wine-devel >= %{winecommonver}

Requires:       wine-common >= %{winecommonver}
Requires:       wine-desktop >= %{winecommonver}
Enhances:       wine

Provides:       %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      %{name}%{?_isa} < %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      mingw%{__isa_bits}-%{name} < %{?epoch:%{epoch}:}%{version}-%{release}

%ifarch x86_64
Requires:       %{name}(x86-32) = %{?epoch:%{epoch}:}%{version}-%{release}
%endif

Provides:       d3d11_%{pkgname}.dll.so%{?_isa} = %{?epoch:%{epoch}:}%{version}
Provides:       d3d10_%{pkgname}.dll.so%{?_isa} = %{?epoch:%{epoch}:}%{version}
Provides:       d3d10_1_%{pkgname}.dll.so%{?_isa} = %{?epoch:%{epoch}:}%{version}
Provides:       d3d10core_%{pkgname}.dll.so%{?_isa} = %{?epoch:%{epoch}:}%{version}


%description
Provides a Vulkan-based implementation of DXGI and D3D11 in order to
run 3D applications on Linux using Wine.


%prep
%autosetup -n %{pkgname}-%{version} -p1

cp %{S:1} .

sed -e "/strip =/s|=.*|= 'true'|g" -i build-wine*.txt

mesonarray(){
  echo -n "$1" | sed -e "s|\s\s| |g" -e "s|\s*$||g" -e "s|\\\\||g" -e "s|'|\\\'|g" -e "s| |', '|g"
}

# disable fortify as it breaks wine
# http://bugs.winehq.org/show_bug.cgi?id=24606
# http://bugs.winehq.org/show_bug.cgi?id=25073
# https://bugzilla.redhat.com/show_bug.cgi?id=1406093
TEMP_CFLAGS="`echo "%{build_cflags}" | sed -e 's/-Wp,-D_FORTIFY_SOURCE=2//'` -Wno-error"
TEMP_CFLAGS="`mesonarray "$TEMP_CFLAGS"`"

TEMP_LDFLAGS="`mesonarray "%{build_ldflags}"`"

sed \
  -e "s|RPM_OPT_FLAGS|$TEMP_CFLAGS|g" \
  -e "s|RPM_LD_FLAGS|$TEMP_LDFLAGS|g" \
  -i build-wine%{__isa_bits}.txt

%build

meson \
  --cross-file build-wine%{__isa_bits}.txt \
  --buildtype "release" \
  %{_target_platform}

pushd %{_target_platform}
ninja -v %{?_smp_mflags}

for spec in d3d11 ;do
  winebuild --dll --fake-module -E ../src/${spec}/${spec}.spec -F ${spec}_%{pkgname}.dll -o ${spec}_%{pkgname}.dll.fake
done
for spec in d3d10 d3d10core d3d10_1 ;do
  winebuild --dll --fake-module -E ../src/d3d10/${spec}.spec -F ${spec}_%{pkgname}.dll -o ${spec}_%{pkgname}.dll.fake
done
popd

%install
mkdir -p %{buildroot}/%{_libdir}/wine
mkdir -p %{buildroot}/%{_libdir}/wine/fakedlls

for dll in d3d11 ;do
  install -pm0755 %{_target_platform}/src/${dll}/${dll}.dll.so \
    %{buildroot}%{_libdir}/wine/${dll}_%{pkgname}.dll.so
done

for dll in d3d10 d3d10_1 d3d10core ;do
  install -pm0755 %{_target_platform}/src/d3d10/${dll}.dll.so \
    %{buildroot}%{_libdir}/wine/${dll}_%{pkgname}.dll.so
done

for fake in d3d11 d3d10 d3d10_1 d3d10core ;do
  install -pm0755 %{_target_platform}/${fake}_%{pkgname}.dll.fake \
    %{buildroot}/%{_libdir}/wine/fakedlls/${fake}_%{pkgname}.dll
done

mkdir -p %{buildroot}/%{_bindir}
install -pm0755 %{S:2} %{buildroot}/%{_bindir}/


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%files
%license LICENSE
%doc README.md README.dxvk
%{_bindir}/wine%{pkgname}cfg
%{_libdir}/wine/*.dll.so
%{_libdir}/wine/fakedlls/*.dll


%changelog
* Mon Jan 21 2019 Phantom X <megaphantomx at bol dot com dot br> - 0.95-2
- dxgi unneeded now
- Update dlls suffix

* Sat Jan 12 2019 Phantom X <megaphantomx at bol dot com dot br> - 0.95-1
- 0.95

* Tue Jan 08 2019 Phantom X <megaphantomx at bol dot com dot br> - 0.94-1
- 0.94
- libwine renamed build

* Mon Nov 12 2018 Phantom X <megaphantomx at bol dot com dot br> - 0.92-1
- 0.92

* Sun Nov 04 2018 Phantom X <megaphantomx at bol dot com dot br> - 0.91-1
- 0.91

* Sun Oct 14 2018 Phantom X <megaphantomx at bol dot com dot br> - 0.90-1
- 0.90

* Mon Oct 08 2018 Phantom X <megaphantomx at bol dot com dot br> - 0.81-2
- BR: gcc
- BR: gcc-c++

* Fri Oct 05 2018 Phantom X <megaphantomx at bol dot com dot br> - 0.81-1
- 0.81

* Sun Sep 23 2018 Phantom X <megaphantomx at bol dot com dot br> - 0.80-1
- 0.80

* Sat Sep 15 2018 Phantom X <megaphantomx at bol dot com dot br> - 0.72-1
- 0.72

* Sun Sep 02 2018 Phantom X <megaphantomx at bol dot com dot br> - 0.71-1
- 0.71

* Wed Aug 29 2018 Phantom X <megaphantomx at bol dot com dot br> - 0.70-2
- Add forgotten d3d10 dlls

* Fri Aug 17 2018 Phantom X <megaphantomx at bol dot com dot br> - 0.70-1
- 0.70

* Sun Aug 12 2018 Phantom X <megaphantomx at bol dot com dot br> - 0.65-1
- 0.65

* Sun Aug 05 2018 Phantom X <megaphantomx at bol dot com dot br> - 0.64-1
- 0.64

* Sat Jul 21 2018 Phantom X <megaphantomx at bol dot com dot br> - 0.63-1
- 0.63

* Mon Jul 16 2018 Phantom X <megaphantomx at bol dot com dot br> - 0.62-1
- 0.62

* Thu Jun 28 2018 Phantom X <megaphantomx at bol dot com dot br> - 0.61-1
- 0.61
- Set minimal version for wine requirements

* Thu Jun 07 2018 Phantom X <megaphantomx at bol dot com dot br> - 0.54-1
- 0.54

* Mon May 28 2018 Phantom X <megaphantomx at bol dot com dot br> - 0.53-1
- 0.53

* Wed May 23 2018 Phantom X <megaphantomx at bol dot com dot br> - 0.52-1
- 0.52

* Sun May 13 2018 Phantom X <megaphantomx at bol dot com dot br> - 0.51-1
- 0.51

* Mon May 07 2018 Phantom X <megaphantomx at bol dot com dot br> - 0.50-1
- 0.50

* Sat Apr 14 2018 Phantom X <megaphantomx at bol dot com dot br> - 0.42-1
- 0.42

* Sat Apr 07 2018 Phantom X <megaphantomx at bol dot com dot br> - 0.41-1
- 0.41

* Fri Mar 09 2018 Phantom X <megaphantomx at bol dot com dot br> - 0.31-2
- Update script

* Thu Mar 08 2018 Phantom X <megaphantomx at bol dot com dot br> - 0.31-1
- 0.31
- Rename spec file to mingw-wine-dxvk
- Change installation paths
- Strip

* Fri Mar 02 2018 Phantom X <megaphantomx at bol dot com dot br> - 0.30-1
- 0.30

* Tue Jan 30 2018 Phantom X <megaphantomx at bol dot com dot br> - 0.21-1
- Fix dll names.

* Fri Jan 26 2018 Phantom X <megaphantomx at bol dot com dot br>
- Install as fakedll, to use with wine-staging dll redirection
- Configuration script

* Fri Jan 19 2018 Phantom X <megaphantomx at bol dot com dot br>
- Initial spec
