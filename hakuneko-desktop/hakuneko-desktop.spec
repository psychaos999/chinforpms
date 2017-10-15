%global debug_package %{nil}
%global _build_id_links none
%global __strip /bin/true

%ifarch x86_64
%global parch amd64
%else
%global parch i386
%endif

%global real_name hakuneko

Name:           %{real_name}-desktop
Version:        0.0.32
Release:        1%{?dist}
Summary:        Manga Downloader

License:        MIT
URL:            https://sourceforge.net/projects/%{real_name}/
Source0:        http://downloads.sourceforge.net/%{real_name}/%{name}_%{version}_linux_%{parch}.rpm

ExclusiveArch:  %{ix86} x86_64

BuildRequires:  chrpath
BuildRequires:  desktop-file-utils
Requires:       hicolor-icon-theme

%global __provides_exclude_from ^%{_libdir}/%{name}/.*


%global __requires_exclude ^libffmpeg.so
%global __requires_exclude %__requires_exclude|^libnode.so

%description
HakuNeko allows you to download manga images from some selected online
manga reader websites.

%prep
%setup -c -T
rpm2cpio %{SOURCE0} | cpio -imdv --no-absolute-filenames

find usr/lib/%{name}/ -name '*.so*' | xargs chmod 0755

chrpath --delete usr/lib/%{name}/%{real_name}

%build

%install
mkdir -p %{buildroot}%{_bindir}
cat > %{buildroot}%{_bindir}/%{name} <<'EOF'
#!/usr/bin/sh
LD_LIBRARY_PATH="%{_libdir}/%{name}${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
export LD_LIBRARY_PATH
exec %{_libdir}/%{name}/%{real_name} "$@"
EOF
chmod 0755 %{buildroot}%{_bindir}/%{name}

mkdir -p %{buildroot}%{_libdir}/%{name}
cp -rp usr/lib/%{name}/{%{real_name},resources,*.{bin,dat,pak,so}} \
  %{buildroot}%{_libdir}/%{name}/

mkdir -p %{buildroot}%{_datadir}/applications
desktop-file-install \
  --dir %{buildroot}%{_datadir}/applications \
  usr/share/applications/%{name}.desktop

mkdir -p %{buildroot}%{_datadir}
cp -rp usr/share/icons %{buildroot}%{_datadir}/

%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
  touch --no-create %{_datadir}/icons/hicolor &>/dev/null
  gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files
%{_bindir}/%{name}
%{_libdir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/*.png


%changelog
* Sat Oct 14 2017 Phantom X <megaphantomx at bol dot com dot br>
- Fist spec