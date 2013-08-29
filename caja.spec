%define url_ver     %(echo %{version}|cut -d. -f1,2)
%define realname    mate-file-manager
%define major       1
%define libname     %mklibname %{name}-extension %{major}
%define develname   %mklibname -d %{name}-extension
%define gi_major    2.0
%define girname     %mklibname %{name}-gir %{gi_major}
%define reallibname %mklibname %{realname} %{major}

Name:               caja
Version:            1.6.2
Release:            2
Summary:            File manager for the MATE desktop environment
Group:              File tools
License:            GPLv2+ and LGPLv2+
URL:                http://www.mate-desktop.org/
Source0:            http://pub.mate-desktop.org/releases/%{url_ver}/%{realname}-%{version}.tar.xz
Source1:            nautilus_16.png
Source2:            nautilus_32.png
Source3:            nautilus_48.png
Source4:            caja-ffmpegthumbnailer.thumbnailer
# (fc) put default launchers on desktop according to product.id (Mageia/Mandriva specific)
#Patch0:             nautilus-defaultdesktop.patch
# (fc) merge desktop with system launcher (used for dynamic, Mageia/Mandriva specific)
#Patch1:             nautilus-dynamic.patch
# gw from Fedora, fix crash on weird file infos
# http://bugzilla.mate.org/show_bug.cgi?id=519743
Patch2:             nautilus-filetype-symlink-fix.patch
# (fc) don't show KDE specific links (CVS + me) (Mdv bug #4844)
Patch3:             nautilus-kdedesktop.patch
# (fc) don't colourise selected icon
#Patch4:            nautilus-2.29.92-colour.patch
# (fc) fix RTL build when disabling self-check (Fedora)
#Patch5:            nautilus-2.26.0-rtlfix.patch
# (fc) auto-unmount ejected medias when mount points are in fstab (Mdv bug #39540)
Patch6:             nautilus-2.25.91-umountfstab.patch
# (fc) allow to lockdown context menu (Novell bug #363122) (SUSE)
#Patch36:            nautilus-bnc363122-lockdown-context-menus.diff
# (fc) add a search .desktop file (GNOME bug #350950) (SUSE)
Patch7:             nautilus-bgo350950-search-desktop.diff
# (fc) fix infinite startup when show_desktop is disabled (Fedora)
Patch8:             mate-file-manager_fix_privat-icons-dir.patch

BuildRequires:      pkgconfig(libxml-2.0)
BuildRequires:      pkgconfig(dbus-glib-1)
BuildRequires:      gtk-doc
BuildRequires:      intltool
BuildRequires:      mate-common
BuildRequires:      pkgconfig(gsettings-desktop-schemas)
BuildRequires:      pkgconfig(exempi-2.0)
BuildRequires:      pkgconfig(gobject-introspection-1.0)
BuildRequires:      pkgconfig(gtk+-2.0)
BuildRequires:      pkgconfig(glib-2.0)
BuildRequires:      pkgconfig(gsettings-desktop-schemas)
BuildRequires:      pkgconfig(cairo-gobject)
BuildRequires:      pkgconfig(gail)
BuildRequires:      pkgconfig(libexif)
BuildRequires:      pkgconfig(mate-desktop-2.0)
BuildRequires:      pkgconfig(pangox)
BuildRequires:      pkgconfig(sm)
BuildRequires:      pkgconfig(unique-1.0)
BuildRequires:      librsvg-devel

Requires:           gvfs
# Whitout these, caja can not connect to a secure network or WebDav
Suggests:           glib-networking
Suggests:           davfs2 
Suggests:           ffmpegthumbnailer

%rename %{realname}

%description
Caja is a file manager for the MATE desktop environment.

%package -n %{libname}
Summary:             Libraries for Mate file manager
Group:               System/Libraries
Provides:            %{reallibname} = %{version}-%{release}

%description -n %{libname}
Caja is a  file manager for the MATE desktop environment.
This package contains libraries used by Caja.

%package -n %{girname}
Summary:        GObject Introspection interface description for %{name}
Group:          System/Libraries
Requires:       %{libname} = %{version}

%description -n %{girname}
GObject Introspection interface description for %{name}

%package -n %{develname}
Summary:        Libraries and include files for developing caja components
Group:          Development/C
Requires:       %{libname} = %{version}
Requires:       %{girname} = %{version}
Provides:       %{name}-devel = %{version}-%{release}
Provides:       %{realname}-devel = %{version}-%{release}

%description -n %{develname}
This package provides the necessary development libraries and include 
files to allow you to develop caja components.

%prep
%setup -q -n %{realname}-%{version}
%apply_patches

%build
NOCONFIGURE=1 ./autogen.sh
 
%configure2_5x \
        --disable-static \
        --disable-update-mimedb \
        --disable-schemas-compile

%make LIBS='-lm -lgmodule-2.0'

%install
%makeinstall_std

find %{buildroot} -name "*.la" -exec rm -rf {} \;

mkdir -p  %{buildroot}%{_miconsdir} %{buildroot}%{_liconsdir}
cp %{SOURCE1} %{buildroot}%{_miconsdir}/caja.png
cp %{SOURCE2} %{buildroot}%{_iconsdir}/caja.png
cp %{SOURCE3} %{buildroot}%{_liconsdir}/caja.png

mkdir -p %{buildroot}%{_datadir}/thumbnailers
install -m755 %{SOURCE4} %{buildroot}%{_datadir}/thumbnailers/caja-ffmpegthumbnailer.thumbnailer

mkdir -p %{buildroot}%{_localstatedir}/lib/mate/desktop \
    %{buildroot}%{_datadir}/%{name}/default-desktop \
    %{buildroot}%{_libdir}/%{name}/extensions-2.0

%{find_lang} %{name} --with-gnome --all-name

%files -f %{name}.lang
%doc README NEWS HACKING AUTHORS MAINTAINERS
#config(noreplace) %{_sysconfdir}/xdg/autostart/caja-desktop.desktop
%dir %{_localstatedir}/lib/mate/desktop
%dir %{_localstatedir}/lib/mate/
%{_bindir}/*
%{_datadir}/caja
%{_datadir}/glib-2.0/schemas/org.mate.*.gschema.xml
%{_datadir}/MateConf/gsettings/caja.convert
%{_datadir}/dbus-1/services/org.mate.freedesktop.FileManager1.service
%{_datadir}/applications/*
%{_datadir}/pixmaps/*
%{_datadir}/mime/packages/caja.xml
%{_datadir}/thumbnailers/caja-ffmpegthumbnailer.thumbnailer
%{_libexecdir}/caja-convert-metadata
%{_mandir}/man1/*
%{_iconsdir}/hicolor/*/apps/caja.*
%{_datadir}/icons/hicolor/*/emblems/emblem-note.png
%{_iconsdir}/*.png
%{_miconsdir}/*.png
%{_liconsdir}/*.png
%dir %{_libdir}/caja
%dir %{_libdir}/caja/extensions-2.0


%files -n %{libname}
%{_libdir}/libcaja*.so.%{major}*

%files -n %{girname}
%{_libdir}/girepository-1.0/Caja-%{gi_major}.typelib

%files -n %{develname}
%doc ChangeLog
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
%{_datadir}/gtk-doc/html/libcaja-extension
%{_datadir}/gir-1.0/Caja-%{gi_major}.gir

