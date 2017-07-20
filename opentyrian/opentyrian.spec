%global commit db67cf6eb3ae4913a85c3a2489f4cc511d09f412
%global shortcommit %(c=%{commit}; echo ${c:0:12})
%global date 20170414
%global use_snapshot 1

%if 0%{?use_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

Name:           opentyrian
Version:        2.1
Release:        1%{?gver}%{?dist}
Summary:        An arcade-style vertical scrolling shooter

License:        GPLv2
URL:            https://bitbucket.org/opentyrian/opentyrian
%if 0%{?use_snapshot}
Source0:        https://bitbucket.org/%{name}/%{name}/get/%{commit}.tar.gz#/%{name}-%{shortcommit}.tar.gz
%else
Source0:        http://www.camanis.net/opentyrian/releases/%{name}-%{version}-src.tar.gz
%endif

Patch0:         %{name}-wild.patch

BuildRequires:  desktop-file-utils
BuildRequires:  pkgconfig(sdl2)
BuildRequires:  pkgconfig(SDL2_net)
Requires:       tyrian-data >= 2.1
Requires:       hicolor-icon-theme

%description
Tyrian is an arcade-style vertical scrolling shooter. The story is set
in 20,031 where you play as Trent Hawkins, a skilled fighter-pilot
employed to fight Microsol and save the galaxy.

%prep
%if 0%{?use_snapshot}
%autosetup -n %{name}-%{name}-%{shortcommit} -p0
%else
%autosetup -p0
%endif

chmod -x CREDITS

%if 0%{?use_snapshot}
sed \
  -e "/^HG_REV/s|:=.*|:= %{version}.%{shortcommit}|g" \
  -e '/touch src\/hg_revision.h/d' \
  -i Makefile
%endif

sed \
  -e 's|$(gamesdir)|%{_datadir}|g' \
  -e "s|-O2|%{optflags}|g" \
  -i Makefile

%build
%make_build \
  STRIP=/bin/true \
  LDFLAGS="%{__global_ldflags}"

%install
mkdir -p %{buildroot}%{_datadir}/tyrian

mkdir -p %{buildroot}%{_bindir}
install -pm0755 %{name} %{buildroot}%{_bindir}/

mkdir -p %{buildroot}%{_mandir}/man6
install -pm0644 linux/man/%{name}.6 %{buildroot}%{_mandir}/man6/

mkdir -p %{buildroot}%{_datadir}/applications
desktop-file-install --mode 0644 \
  --dir %{buildroot}%{_datadir}/applications \
  --remove-category="Application" \
  linux/%{name}.desktop

for res in 22 24 32 48 128 ;do
  dir=%{buildroot}%{_datadir}/icons/hicolor/${res}x${res}/apps
  mkdir -p ${dir}
  install -pm0644 linux/icons/tyrian-${res}.png \
    ${dir}/%{name}.png
done

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
%license COPYING
%doc CREDITS README NEWS
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%dir %{_datadir}/tyrian
%{_mandir}/man6/%{name}.6*


%changelog
* Thu Jun 15 2017 Phantom X <megaphantomx at bol dot com dot br> - 2.1-1.20170414gitdb67cf6eb3ae
- New snapshot

* Sun Jan 29 2017 Phantom X <megaphantomx at bol dot com dot br> - 2.1-1.20170115gitf61ceced26a3
- Initial spec
