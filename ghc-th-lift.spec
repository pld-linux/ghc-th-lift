#
# Conditional build:
%bcond_without	prof	# profiling library
#
%define		pkgname	th-lift
Summary:	Derive Template Haskell's Lift class for datatypes
Summary(pl.UTF-8):	Wywodzenie klasy Lift z Template Haskella dla typów danych
Name:		ghc-%{pkgname}
Version:	0.8.1
Release:	1
License:	GPL v2 or BSD
Group:		Development/Languages
#Source0Download: http://hackage.haskell.org/package/th-lift
Source0:	http://hackage.haskell.org/package/%{pkgname}-%{version}/%{pkgname}-%{version}.tar.gz
# Source0-md5:	fe5e2a759afd735dcb072cf9db0db8f6
URL:		http://hackage.haskell.org/package/th-lift
BuildRequires:	ghc >= 6.12.3
BuildRequires:	ghc-base >= 3
BuildRequires:	ghc-ghc-prim
BuildRequires:	ghc-template-haskell >= 2.5
BuildRequires:	ghc-th-abstraction >= 0.2.3
%if %{with prof}
BuildRequires:	ghc-prof >= 6.12.3
BuildRequires:	ghc-base-prof >= 3
BuildRequires:	ghc-ghc-prim-prof
BuildRequires:	ghc-template-haskell-prof >= 2.4
BuildRequires:	ghc-th-abstraction-prof >= 0.2.3
%endif
BuildRequires:	rpmbuild(macros) >= 1.608
Requires(post,postun):	/usr/bin/ghc-pkg
%requires_eq	ghc
Requires:	ghc-base >= 3
Requires:	ghc-ghc-prim
Requires:	ghc-template-haskell >= 2.4
Requires:	ghc-th-abstraction >= 0.2.3
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# debuginfo is not useful for ghc
%define		_enable_debug_packages	0

# don't compress haddock files
%define		_noautocompressdoc	*.haddock

%description
Derive Template Haskell's Lift class for datatypes.

%description -l pl.UTF-8
Wywodzenie klasy Lift z Template Haskella dla typów danych.

%package prof
Summary:	Profiling %{pkgname} library for GHC
Summary(pl.UTF-8):	Biblioteka profilująca %{pkgname} dla GHC.
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	ghc-base-prof >= 3
Requires:	ghc-ghc-prim-prof
Requires:	ghc-template-haskell-prof >= 2.4
Requires:	ghc-th-abstraction-prof >= 0.2.3

%description prof
Profiling %{pkgname} library for GHC. Should be installed when GHC's
profiling subsystem is needed.

%description prof -l pl.UTF-8
Biblioteka profilująca %{pkgname} dla GHC. Powinna być zainstalowana
kiedy potrzebujemy systemu profilującego z GHC.

%prep
%setup -q -n %{pkgname}-%{version}

%build
runhaskell Setup.hs configure -v2 \
	%{?with_prof:--enable-library-profiling} \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--docdir=%{_docdir}/%{name}-%{version}

runhaskell Setup.hs build
runhaskell Setup.hs haddock --executables

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d

runhaskell Setup.hs copy --destdir=$RPM_BUILD_ROOT

# work around automatic haddock docs installation
%{__rm} -rf %{name}-%{version}-doc
cp -a $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version} %{name}-%{version}-doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

runhaskell Setup.hs register \
	--gen-pkg-config=$RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%ghc_pkg_recache

%postun
%ghc_pkg_recache

%files
%defattr(644,root,root,755)
%doc BSD3 CHANGELOG.md %{name}-%{version}-doc/html
%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSth-lift-%{version}-*.so
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSth-lift-%{version}-*.a
%exclude %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSth-lift-%{version}-*_p.a
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Language
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Language/Haskell
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Language/Haskell/TH
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Language/Haskell/TH/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Language/Haskell/TH/*.dyn_hi

%files prof
%defattr(644,root,root,755)
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSth-lift-%{version}-*_p.a
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Language/Haskell/TH/*.p_hi
