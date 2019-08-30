%global commit 046d3913a35700239a994626602a0506de73c2ea
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20190823
%global with_snapshot 0

%global with_bin 0

%if 0%{?with_bin}
%global debug_package %{nil}
%global _build_id_links none
%global __strip /bin/true
%endif

%global pkgname amdvlk

%global commit1 9bc5dd4450a6361faf5c5661056a7ee494fad830
%global shortcommit1 %(c=%{commit1}; echo ${c:0:7})
%global srcname1 %{pkgname}-llvm

%global commit2 4fa48ef1cf0f81eafdb56df91c2f2180d4865101
%global shortcommit2 %(c=%{commit2}; echo ${c:0:7})
%global srcname2 %{pkgname}-llpc

%global commit3 331558e93794068a786bf699d3fe23bb11bac021
%global shortcommit3 %(c=%{commit3}; echo ${c:0:7})
%global srcname3 %{pkgname}-xgl

%global commit4 68b57dba33a4d922e8f1ef1b3781c2f659ffbd1c
%global shortcommit4 %(c=%{commit4}; echo ${c:0:7})
%global srcname4 %{pkgname}-pal

%global commit5 2f31d1170e8a12a66168b23235638c4bbc43ecdc
%global shortcommit5 %(c=%{commit5}; echo ${c:0:7})
%global srcname5 %{pkgname}-spvgen

%global commit6 2b6fee002db6cc92345b02aeee963ebaaf4c0e2f
%global shortcommit6 %(c=%{commit6}; echo ${c:0:7})
%global srcname6 %{pkgname}-MetroHash

%global commit7 9702d47c6fe4cefbc55f905b0e9966452124b6c2
%global shortcommit7 %(c=%{commit7}; echo ${c:0:7})
%global srcname7 SPIRV-Tools

%global commit8 123dc278f204f8e833e1a88d31c46d0edf81d4b2
%global shortcommit8 %(c=%{commit8}; echo ${c:0:7})
%global srcname8 SPIRV-Headers

%global commit9 22683b409e6df419da940df561b24b4b5d8ab90a
%global shortcommit9 %(c=%{commit9}; echo ${c:0:7})
%global srcname9 glslang

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

%global optflags %(echo %{optflags} | sed -e 's/ -g\\b/ -g1/')

%global vc_url  https://github.com/GPUOpen-Drivers

Name:           amdvlk-vulkan-driver
Version:        2019.3.5
Release:        1%{?gver}%{?dist}
Summary:        AMD Open Source Driver For Vulkan
License:        MIT
URL:            %{vc_url}/AMDVLK

%global ver     %(echo %{version} | sed 's/\\./.Q/1')
%if 0%{?with_bin}
Source0:        %{url}/releases/download/v-%{ver}/%{pkgname}_%{ver}_amd64.deb

# Don't have x86 binary release
ExclusiveArch:  x86_64

%else
%if 0%{?with_snapshot}
Source0:        %{url}/archive/%{commit}.tar.gz#/%{pkgname}-%{shortcommit}.tar.gz
%else
Source0:        %{url}/archive/v-%{ver}.tar.gz#/%{pkgname}-%{ver}.tar.gz
%endif
Source1:        %{vc_url}/llvm/archive/%{commit1}.tar.gz#/%{srcname1}-%{shortcommit1}.tar.gz
Source2:        %{vc_url}/llpc/archive/%{commit2}.tar.gz#/%{srcname2}-%{shortcommit2}.tar.gz
Source3:        %{vc_url}/xgl/archive/%{commit3}.tar.gz#/%{srcname3}-%{shortcommit3}.tar.gz
Source4:        %{vc_url}/pal/archive/%{commit4}.tar.gz#/%{srcname4}-%{shortcommit4}.tar.gz
Source5:        %{vc_url}/spvgen/archive/%{commit5}.tar.gz#/%{srcname5}-%{shortcommit5}.tar.gz
Source6:        %{vc_url}/MetroHash/archive/%{commit6}.tar.gz#/%{srcname6}-%{shortcommit6}.tar.gz
Source7:        https://github.com/KhronosGroup/%{srcname7}/archive/%{commit7}/%{srcname7}-%{shortcommit7}.tar.gz
Source8:        https://github.com/KhronosGroup/%{srcname8}/archive/%{commit8}/%{srcname8}-%{shortcommit8}.tar.gz
Source9:        https://github.com/KhronosGroup/%{srcname9}/archive/%{commit9}/%{srcname9}-%{shortcommit9}.tar.gz
%endif
Source20:        %{url}/raw/master/README.md

%if !0%{?with_bin}
BuildRequires:   gcc
BuildRequires:   gcc-c++
BuildRequires:   cmake
BuildRequires:   ninja-build
BuildRequires:   perl-interpreter
BuildRequires:   python3
BuildRequires:   glibc-devel
BuildRequires:   libstdc++-devel
BuildRequires:   pkgconfig(gtest)
BuildRequires:   pkgconfig(x11)
BuildRequires:   pkgconfig(xcb)
BuildRequires:   pkgconfig(xrandr)
BuildRequires:   pkgconfig(xshmfence)
BuildRequires:   pkgconfig(wayland-client)
%endif

Requires:       vulkan
Requires:       vulkan-filesystem


%description
The AMD Open Source Driver for Vulkan® is an open-source Vulkan driver
for Radeon™ graphics adapters on Linux®.


%prep
%if 0%{?with_bin}
%setup -q -c -T
ar p %{S:0} data.tar.xz | tar xJ

cp -p %{S:20} .
mv usr/share/doc/amdvlk/copyright LICENSE.txt

sed -e 's|/usr/lib/x86_64-linux-gnu|%{_libdir}|g' -i etc/vulkan/icd.d/*.json

%else
%setup -q -c -n %{name}-%{version} -a 0 -a 1 -a 2 -a 3 -a 4 -a 5 -a 6 -a 7 -a 8 -a 9

%if 0%{?with_snapshot}
ln -sf AMDVLK-%{commit} AMDVLK
%else
ln -sf AMDVLK-v-%{ver} AMDVLK
%endif
ln -sf llvm-%{commit1} llvm
ln -sf llpc-%{commit2} llpc
ln -sf xgl-%{commit3} xgl
ln -sf pal-%{commit4} pal
ln -sf spvgen-%{commit5} spvgen
mv MetroHash-%{commit6} pal/src/util/imported/metrohash
mv SPIRV-Tools-%{commit7} spvgen/external/SPIRV-tools
mv SPIRV-Headers-%{commit8} spvgen/external/SPIRV-tools/external/SPIRV-Headers
mv glslang-%{commit9} spvgen/external/glslang

cp -p AMDVLK/LICENSE.txt .
cp -p AMDVLK/README.md .

# workaround for AMDVLK#89
find . -name 'CMakeLists.txt' -exec sed -e "s/-Werror\b//g" -i "{}" ';'
sed -e "s/-Werror\b//g" -i pal/shared/gpuopen/cmake/AMD.cmake

sed -e '/CMAKE_SHARED_LINKER_FLAGS_RELEASE/s| -s\b| |g' -i xgl/CMakeLists.txt
sed -e '/soname=/s|so.1|so|g' -i xgl/icd/CMakeLists.txt
%endif

%build
%if !0%{?with_bin}
mkdir -p xgl/%{_target_platform}
pushd xgl/%{_target_platform}

%cmake .. \
  -DCMAKE_VERBOSE_MAKEFILE=ON \
  -DBUILD_SHARED_LIBS:BOOL=OFF \
  -DBUILD_WAYLAND_SUPPORT:BOOL=ON \
  -D-DCMAKE_BUILD_TYPE:STRING="Release" \
  -DCMAKE_AR:FILEPATH=%{_bindir}/gcc-ar \
  -DCMAKE_NM:FILEPATH=%{_bindir}/gcc-nm \
  -DCMAKE_RANLIB:FILEPATH=%{_bindir}/gcc-ranlib \
  -G Ninja \
%{nil}

%ninja_build
%ninja_build spvgen

popd
%endif


%install
mkdir -p %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{_datadir}/vulkan/icd.d

%if %{?__isa_bits} == 64
mkdir _temp_install
%if 0%{?with_bin}
  mv usr/lib/x86_64-linux-gnu/*.so _temp_install/
  mv etc/vulkan/icd.d/amd_icd64.json _temp_install/
%else
  mv xgl/%{_target_platform}/icd/amdvlk64.so _temp_install/
  mv xgl/%{_target_platform}/spvgen/spvgen.so _temp_install/
  mv AMDVLK/json/Redhat/amd_icd64.json _temp_install/
%endif
  install -pm0644 _temp_install/amd_icd64.json \
    %{buildroot}%{_datadir}/vulkan/icd.d/amd_icd.%{_arch}.json
  install -pm0755 _temp_install/*.so %{buildroot}%{_libdir}/
%else
  install -pm0644 AMDVLK/json/Redhat/amd_icd32.json \
    %{buildroot}%{_datadir}/vulkan/icd.d/amd_icd.%{_arch}.json
  install -pm0755 xgl/%{_target_platform}/icd/amdvlk32.so %{buildroot}%{_libdir}/
  install -pm0755 xgl/%{_target_platform}/spvgen/spvgen.so %{buildroot}%{_libdir}/
%endif

mkdir -p %{buildroot}%{_sysconfdir}/amd
echo "MaxNumCmdStreamsPerSubmit,4" > %{buildroot}%{_sysconfdir}/amd/amdPalSettings.cfg


%files
%license LICENSE.txt
%doc README.md
%dir %{_sysconfdir}/amd
%config %{_sysconfdir}/amd/amdPalSettings.cfg
%{_datadir}/vulkan/icd.d/amd_icd.%{_arch}.json
%{_libdir}/amdvlk*.so
%{_libdir}/spvgen*.so


%changelog
* Thu Aug 29 2019 Phantom X <megaphantomx at bol dot com dot br> - 2019.3.5-1
- 2019.Q3.5

* Tue Aug 27 2019 Phantom X <megaphantomx at bol dot com dot br> - 2019.3.4-1
- chinforpms changes and bin support

* Mon Jul 29 2019 Mihai Vultur <xanto@egaming.ro>
- Implement some version autodetection to reduce maintenance work.
- Don't build wsa anymore.