%global smoothver 0.8.74

Name:           freac
Version:        1.1~alpha_20181201a
Release:        1%{?dist}
Summary:        A free audio converter and CD ripper

License:        GPLv2
URL:            http://www.freac.org/

%global ver     %(echo %{version} | tr '~' '-' | tr '_' '-')
Source0:        https://downloads.sourceforge.net/bonkenc/%{name}-%{ver}.tar.gz

BuildRequires:  desktop-file-utils
BuildRequires:  gcc-c++
BuildRequires:  ImageMagick
BuildRequires:  freac-cdk-devel
BuildRequires:  smooth-devel >= %{smoothver}
BuildRequires:  pkgconfig(libudev)
Requires:       hicolor-icon-theme
Requires:       flac
Requires:       lame
Requires:       libsamplerate
Requires:       opus-tools
Requires:       shntool
Requires:       speex
Requires:       timidity++
Requires:       twolame
Requires:       vorbis-tools
Requires:       wavpack
Requires:       xmp
#Suggests:       aften
Suggests:       ffmpeg


%description
fre:ac is a free audio converter and CD ripper with support for various
popular formats and encoders. It currently converts between MP3, MP4/M4A,
WMA, Ogg Vorbis, FLAC, AAC, WAV and Bonk formats.


%prep
%autosetup -n %{name}-%{ver}

sed -e 's/\r//' -i COPYING Readme

sed -e 's|/lib/|/%{_lib}/|g' -i src/loader/console.cpp src/loader/gui.cpp

%build
%set_build_flags

%make_build prefix=/usr libdir=%{_libdir}


%install

%make_install prefix=/usr libdir=%{_libdir}

chmod +x %{buildroot}%{_libdir}/%{name}/*.so*

mv %{buildroot}%{_datadir}/doc _docs

mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/%{name}.desktop <<EOF
[Desktop Entry]
Name=fre:ac
GenericName=Audio Converter
GenericName[pt_BR]=Conversor de Áudio
Type=Application
Comment=Audio converter and CD ripper
Exec=%{name} --scale:1.2
Icon=%{name}
Terminal=false
Categories=GTK;AudioVideo;
EOF

mkdir -p %{buildroot}%{_datadir}/icons/hicolor/128x128/apps
ln -s ../../../../%{name}/icons/%{name}.png \
  %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/%{name}.png

for res in 16 22 24 32 36 48 64 72 96 ;do
  dir=%{buildroot}%{_datadir}/icons/hicolor/${res}x${res}/apps
  mkdir -p ${dir}
  convert %{buildroot}%{_datadir}/%{name}/icons/%{name}.png -filter Lanczos -resize ${res}x${res} \
    ${dir}/%{name}.png
done

desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop


%files
%license COPYING
%doc _docs/*
%{_bindir}/%{name}*
%{_libdir}/%{name}/
%{_datadir}/%{name}/
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/*/apps/*.png


%changelog
* Tue Dec 04 2018 Phantom X <megaphantomx at bol dot com dot br> - 1.1~alpha_20181201a-1
- 1.1-alpha-20181201a

* Sun Sep 23 2018 Phantom X <megaphantomx at bol dot com dot br> - 1.1-0.4.alpha.20180913
- 1.1-20180913

* Fri Jul 13 2018 Phantom X <megaphantomx at bol dot com dot br> - 1.1-0.3.alpha.20180710
- 1.1-20180710

* Wed May 23 2018 Phantom X <megaphantomx at bol dot com dot br> - 1.1-0.2.alpha.20180306
- Fix dangling icon link

* Tue May 22 2018 Phantom X <megaphantomx at bol dot com dot br> - 1.1-0.1.alpha.20180306
- Initial spec
