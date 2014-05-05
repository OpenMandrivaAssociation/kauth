%define major 5
%define libname %mklibname KF5Auth %{major}
%define devname %mklibname KF5Auth -d
%define debug_package %{nil}

Name: kauth
Version: 4.98.0
Release: 1
Source0: http://ftp5.gwdg.de/pub/linux/kde/unstable/frameworks/%{version}/%{name}-%{version}.tar.xz
Summary: The KDE Frameworks 5 authentication library
URL: http://kde.org/
License: GPL
Group: System/Libraries
BuildRequires: cmake
BuildRequires: pkgconfig(Qt5Core)
BuildRequires: cmake(KF5CoreAddons)
BuildRequires: qmake5
BuildRequires: extra-cmake-modules5
Requires: %{libname} = %{EVRD}

%description
KAuth is an abstraction to system policy and authentication features.

%package -n %{libname}
Summary: The KDE Frameworks 5 authentication library
Group: System/Libraries

%description -n %{libname}
KAuth is an abstraction to system policy and authentication features.

%package -n %{devname}
Summary: Development files for %{name}
Group: Development/KDE and Qt
Requires: %{libname} = %{EVRD}

%description -n %{devname}
KAuth is an abstraction to system policy and authentication features.

%prep
%setup -q
%cmake

%build
%make -C build

%install
%makeinstall_std -C build
mkdir -p %{buildroot}%{_libdir}/qt5
mv %{buildroot}%{_prefix}/mkspecs %{buildroot}%{_libdir}/qt5

%files
%{_sysconfdir}/dbus-1/system.d/org.kde.kf5auth.conf
%{_libdir}/plugins/kf5/plugins/kauth/helper/kauth_helper_plugin.so
%{_datadir}/kauth

%files -n %{libname}
%{_libdir}/*.so.%{major}
%{_libdir}/*.so.%{version}

%files -n %{devname}
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/cmake/KF5Auth
%{_libdir}/qt5/mkspecs/modules/*
