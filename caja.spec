%define url_ver	%(echo %{version}|cut -d. -f1,2)
%define oname    mate-file-manager

%define api 2.0
%define major 1
%define libname %mklibname %{name}-extension %{major}
%define girname %mklibname %{name}-gir %{api}
%define devname %mklibname -d %{name}-extension

Summary:            File manager for the MATE desktop environment
Name:               caja
Version:            1.14.1
Release:            1
Group:              File tools
License:            GPLv2+ and LGPLv2+
Url:                http://www.mate-desktop.org/
Source0:            http://pub.mate-desktop.org/releases/%{url_ver}/%{name}-%{version}.tar.xz
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
BuildRequires:      gtk-doc
BuildRequires:      intltool
BuildRequires:      mate-common
BuildRequires:      pkgconfig(cairo-gobject)
BuildRequires:      pkgconfig(dbus-glib-1)
BuildRequires:      pkgconfig(exempi-2.0)
BuildRequires:      pkgconfig(gail-3.0)
BuildRequires:      pkgconfig(glib-2.0)
BuildRequires:      pkgconfig(gobject-introspection-1.0)
BuildRequires:      pkgconfig(gsettings-desktop-schemas)
BuildRequires:      pkgconfig(gtk+-3.0)
BuildRequires:      pkgconfig(libexif)
BuildRequires:      pkgconfig(librsvg-2.0)
BuildRequires:      pkgconfig(libxml-2.0)
BuildRequires:      pkgconfig(mate-desktop-2.0)
BuildRequires:      pkgconfig(pangox)
BuildRequires:      pkgconfig(sm)
BuildRequires:      pkgconfig(unique-3.0)
Requires:           gvfs
# Whitout these, caja can not connect to a secure network or WebDav
Suggests:           glib-networking
Suggests:           davfs2 
Suggests:           ffmpegthumbnailer
%rename %{oname}

%description
Caja is a file manager for the MATE desktop environment.

%package -n %{libname}
Summary:             Libraries for Mate file manager
Group:               System/Libraries

%description -n %{libname}
Caja is a  file manager for the MATE desktop environment.
This package contains libraries used by Caja.

%package -n %{girname}
Summary:        GObject Introspection interface description for %{name}
Group:          System/Libraries

%description -n %{girname}
GObject Introspection interface description for %{name}

%package -n %{devname}
Summary:        Libraries and include files for developing caja components
Group:          Development/C
Requires:       %{libname} = %{version}-%{release}
Requires:       %{girname} = %{version}-%{release}
Provides:       %{name}-devel = %{version}-%{release}
%rename %{_lib}%{oname}-devel

%description -n %{devname}
This package provides the necessary development libraries and include 
files to allow you to develop caja components.

%prep
%setup -q
%apply_patches

%build
%configure \
        --disable-update-mimedb \
	--with-gtk=3.0

%make

%install
%makeinstall_std

# remove unneeded converters
rm -fr %{buildroot}%{_datadir}/MateConf

mkdir -p %{buildroot}%{_datadir}/thumbnailers
install -m755 %{SOURCE4} %{buildroot}%{_datadir}/thumbnailers/caja-ffmpegthumbnailer.thumbnailer

mkdir -p %{buildroot}%{_localstatedir}/lib/mate/desktop \
	%{buildroot}%{_datadir}/%{name}/default-desktop \
	%{buildroot}%{_libdir}/%{name}/extensions-2.0

%find_lang %{name} --with-gnome --all-name

%files -f %{name}.lang
%doc README NEWS HACKING AUTHORS MAINTAINERS
%dir %{_localstatedir}/lib/mate/desktop
%dir %{_localstatedir}/lib/mate/
%{_bindir}/*
%{_datadir}/applications/*
%{_datadir}/caja
%{_datadir}/glib-2.0/schemas/org.mate.*.gschema.xml
%{_datadir}/dbus-1/services/org.mate.freedesktop.FileManager1.service
%{_datadir}/mime/packages/caja.xml
%{_datadir}/pixmaps/*
%{_datadir}/thumbnailers/caja-ffmpegthumbnailer.thumbnailer
%{_libexecdir}/caja-convert-metadata
%{_mandir}/man1/*
%{_iconsdir}/hicolor/*/apps/caja.*
%{_iconsdir}/hicolor/*/emblems/emblem-note.png
%dir %{_libdir}/caja
%dir %{_libdir}/caja/extensions-2.0
%{_datadir}/appdata/caja.appdata.xml

%files -n %{libname}
%{_libdir}/libcaja-extension.so.%{major}*

%files -n %{girname}
%{_libdir}/girepository-1.0/Caja-%{api}.typelib

%files -n %{devname}
%doc ChangeLog
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
%{_datadir}/gtk-doc/html/libcaja-extension
%{_datadir}/gir-1.0/Caja-%{api}.gir

