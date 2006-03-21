#
# Conditional build:
%bcond_without	cddb		# build cd-info without CDDB lookups (for bootstrap)
%bcond_without	static_libs	# don't build static library
%bcond_without	vcd		# build cd-info without VCD support (for bootstrap)
#				  (affects only -utils, not libraries)
#
Summary:	GNU Compact Disc Input and Control Library
Summary(pl):	Biblioteka GNU do obs�ugi wej�cia i sterowania czytnikiem CD
Name:		libcdio
Version:	0.77
Release:	1
License:	GPL v2+
Group:		Libraries
Source0:	ftp://ftp.gnu.org/gnu/libcdio/%{name}-%{version}.tar.gz
# Source0-md5:	7ea25252009b49422055da97a96efe04
Patch0:		%{name}-info.patch
Patch1:		%{name}-link.patch
URL:		http://www.gnu.org/software/libcdio/
BuildRequires:	autoconf >= 2.52
BuildRequires:	automake >= 1:1.8.3
BuildRequires:	gettext-devel
BuildRequires:	help2man
%{?with_cddb:BuildRequires:	libcddb-devel >= 0.9.4}
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:1.5
%{?with_vcd:BuildRequires:	vcdimager-devel >= 0.7.21}
BuildRequires:	pkgconfig
BuildRequires:	sed >= 4.0
BuildRequires:	texinfo
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This library is to encapsulate CD-ROM reading and control.
Applications wishing to be oblivious of the OS- and device-dependent
properties of a CD-ROM can use this library.

Some support for disk image types like BIN/CUE and NRG is available,
so applications that use this library also have the ability to read
disc images as though they were CD's.

Immediate uses are VCDImager, a navigation-capable Video CD plugin
and CD-DA plugin for the media player xine.

A sample utility, cd-info which displayings CD info is included in
utils subpackage.

%description -l pl
Ta biblioteka obudowuje czynno�ci odczytu i sterowania czytnikami
CD-ROM. Aplikacje chc�ce zapomnie� o zale�nych od systemu lub
urz�dzenia w�asno�ciach CD-ROM-u mog� u�ywa� tej biblioteki.

Dost�pna jest pewna obs�uga obraz�w dysk�w typu BIN/CUE czy NRG, wi�c
aplikacje u�ywaj�ce tej biblioteki mog� czyta� tak�e takie obrazy
dysk�w tak jakby by�y p�ytami.

Biblioteka jest u�ywana bezpo�rednio w VCDImagerze, wtyczce z
nawigacj� do Video CD oraz wtyczce CD-DA dla odtwarzacza multimedi�w
xine.

W podpakiecie utils za��czone jest przyk�adowe narz�dzie cd-info
s�u��ce do wy�wietlania informacji o p�ytach kompaktowych.

%package devel
Summary:	Header files for libcdio libraries
Summary(pl):	Pliki nag��wkowe bibliotek libcdio
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for libcdio libraries.

%description devel -l pl
Pliki nag��wkowe bibliotek libcdio.

%package static
Summary:	Static libcdio libraries
Summary(pl):	Statyczne biblioteki libcdio
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libcdio libraries.

%description static -l pl
Statyczne biblioteki libcdio.

%package c++
Summary:	C++ libcdio libraries
Summary(pl):	Biblioteki C++ libcdio
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description c++
C++ libcdio libraries.

%description c++ -l pl
Biblioteki C++ libcdio.

%package c++-devel
Summary:	Header files for C++ libcdio libraries
Summary(pl):	Pliki nag��wkowe bibliotek C++ libcdio
Group:		Development/Libraries
Requires:	%{name}-c++ = %{version}-%{release}
Requires:	%{name}-devel = %{version}-%{release}
Requires:	libstdc++-devel

%description c++-devel
Header files for C++ libcdio libraries.

%description c++-devel -l pl
Pliki nag��wkowe bibliotek C++ libcdio.

%package c++-static
Summary:	Static C++ libcdio libraries
Summary(pl):	Statyczne biblioteki C++ libcdio
Group:		Development/Libraries
Requires:	%{name}-c++-devel = %{version}-%{release}

%description c++-static
Static C++ libcdio libraries.

%description c++-static -l pl
Statyczne biblioteki C++ libcdio.

%package utils
Summary:	libcdio utilities: cd-info, cd-read
Summary(pl):	Narz�dzia u�ywaj�ce libcdio: cd-info, cd-read
Group:		Applications
Requires:	%{name} = %{version}-%{release}

%description utils
libcdio utilities: cd-info, cd-read.

%description utils -l pl
Narz�dzia u�ywaj�ce libcdio: cd-info, cd-read.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%{__sed} -i 's, example$,,' Makefile.am

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--enable-cd-info-linux \
	--enable-maintainer-mode \
	%{!?with_cddb:--disable-cddb} \
	%{!?with_vcd:--disable-vcd-info} \
	%{!?with_static_libs:--disable-static}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	mansubdir=/ja/man1

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%post devel
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir %{_infodir} >/dev/null 2>&1

%postun devel
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir %{_infodir} >/dev/null 2>&1

%post	c++ -p /sbin/ldconfig
%postun	c++ -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README THANKS TODO
%attr(755,root,root) %{_libdir}/libcdio.so.*.*.*
%attr(755,root,root) %{_libdir}/libcdio_cdda.so.*.*.*
%attr(755,root,root) %{_libdir}/libcdio_paranoia.so.*.*.*
%attr(755,root,root) %{_libdir}/libiso9660.so.*.*.*
%attr(755,root,root) %{_libdir}/libudf.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcdio.so
%attr(755,root,root) %{_libdir}/libcdio_cdda.so
%attr(755,root,root) %{_libdir}/libcdio_paranoia.so
%attr(755,root,root) %{_libdir}/libiso9660.so
%attr(755,root,root) %{_libdir}/libudf.so
%{_libdir}/libcdio.la
%{_libdir}/libcdio_cdda.la
%{_libdir}/libcdio_paranoia.la
%{_libdir}/libiso9660.la
%{_libdir}/libudf.la
%{_includedir}/cdio
%{_pkgconfigdir}/libcdio.pc
%{_pkgconfigdir}/libcdio_cdda.pc
%{_pkgconfigdir}/libcdio_paranoia.pc
%{_pkgconfigdir}/libiso9660.pc
%{_infodir}/libcdio.info*

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libcdio.a
%{_libdir}/libcdio_cdda.a
%{_libdir}/libcdio_paranoia.a
%{_libdir}/libiso9660.a
%{_libdir}/libudf.a
%endif

%files c++
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcdio++.so.*.*.*
%attr(755,root,root) %{_libdir}/libiso9660++.so.*.*.*

%files c++-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcdio++.so
%attr(755,root,root) %{_libdir}/libiso9660++.so
%{_libdir}/libcdio++.la
%{_libdir}/libiso9660++.la
%{_includedir}/cdio++

%if %{with static_libs}
%files c++-static
%defattr(644,root,root,755)
%{_libdir}/libcdio++.a
%{_libdir}/libiso9660++.a
%endif

%files utils
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
%{_mandir}/man1/*.1*
%lang(ja) %{_mandir}/ja/man1/*.1*
