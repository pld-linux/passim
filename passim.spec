#
# Conditional build:
%bcond_without	static_libs	# static library
#
Summary:	A local caching server
Summary(pl.UTF-8):	Lokalny serwer cache'ujący
Name:		passim
Version:	0.1.8
Release:	1
License:	LGPL v2.1+
Group:		Libraries
#Source0Download: https://github.com/hughsie/passim/releases
Source0:	https://github.com/hughsie/passim/releases/download/%{version}/%{name}-%{version}.tar.xz
# Source0-md5:	73926d0fe41f290ba185dcdf8f40c758
URL:		https://github.com/hughsie/passim
BuildRequires:	gcc >= 6:4.7
BuildRequires:	glib2-devel >= 1:2.68.0
BuildRequires:	gnutls-devel >= 3.6.0
BuildRequires:	gobject-introspection-devel
BuildRequires:	libsoup3-devel >= 3.4.0
BuildRequires:	meson >= 0.61.0
BuildRequires:	ninja >= 1.5
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	systemd-units >= 1:211
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires:	%{name}-libs = %{version}-%{release}
Provides:	group(passim)
Provides:	user(passim)
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Passim is a daemon that allows software to share files on your local
network.

%description -l pl.UTF-8
Passim to demon pozwalający programom współdzielić pliki w sieci
lokalnej.

%package libs
Summary:	Passim shared library
Summary(pl.UTF-8):	Biblioteka współdzielona Passim
Group:		Libraries
Requires:	glib2 >= 1:2.68.0

%description libs
Passim shared library.

%description libs -l pl.UTF-8
Biblioteka współdzielona Passim.

%package devel
Summary:	Header files for Passim library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki Passim
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	glib2-devel >= 1:2.68.0

%description devel
Header files for Passim library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki Passim.

%package static
Summary:	Static Passim library
Summary(pl.UTF-8):	Statyczna biblioteka Passim
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static Passim library.

%description static -l pl.UTF-8
Statyczna biblioteka Passim.

%prep
%setup -q

%build
%meson build \
	%{!?with_static_libs:--default-library=shared}

%ninja_build -C build

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

# unify locale dir
%{__mv} $RPM_BUILD_ROOT%{_localedir}/{nb_NO,nb}

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g X passim
%useradd -u X -g X -d /usr/share/empty -s /bin/false -c "Local Caching Server" passim

%postun
if [ "$1" = "0" ]; then
	%userremove passim
	%groupremove passim
fi

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc README.md SECURITY.md
%attr(755,root,root) %{_bindir}/passim
%attr(755,root,root) %{_libexecdir}/passimd
%{_datadir}/dbus-1/interfaces/org.freedesktop.Passim.xml
%{_datadir}/dbus-1/system-services/org.freedesktop.Passim.service
%{_datadir}/dbus-1/system.d/org.freedesktop.Passim.conf
%{_datadir}/metainfo/org.freedesktop.Passim.metainfo.xml
%{_datadir}/passim
%{_iconsdir}/hicolor/scalable/apps/org.freedesktop.Passim.png
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/passim.conf
%{systemdunitdir}/passim.service
/usr/lib/sysusers.d/passim.conf
%dir /var/lib/passim
%dir /var/lib/passim/data
/var/lib/passim/data/a948904f2f0f479b8f8197694b30184b0d2ed1c1cd2a1ec0fb85d299a192a447-HELLO.md
%{_mandir}/man1/passim.1*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libpassim.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libpassim.so.1
%{_libdir}/girepository-1.0/Passim-1.0.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libpassim.so
%{_includedir}/passim-1
%{_datadir}/gir-1.0/Passim-1.0.gir
%{_pkgconfigdir}/passim.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libpassim.a
%endif
