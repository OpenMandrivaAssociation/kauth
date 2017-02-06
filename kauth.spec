%define major 5
%define libname %mklibname KF5Auth %{major}
%define devname %mklibname KF5Auth -d
%define stable %([ "`echo %{version} |cut -d. -f3`" -ge 80 ] && echo -n un; echo -n stable)
%define debug_package %{nil}

Name: kauth
Version: 5.31.0
Release: 1
Source0: http://download.kde.org/%{stable}/frameworks/%(echo %{version} |cut -d. -f1-2)/%{name}-%{version}.tar.xz
Patch0: kauth-5.3.0-compile.patch
Summary: The KDE Frameworks 5 authentication library
URL: http://kde.org/
License: GPL
Group: System/Libraries
BuildRequires: cmake(ECM)
BuildRequires: pkgconfig(Qt5Core)
BuildRequires: pkgconfig(Qt5Widgets)
BuildRequires: pkgconfig(Qt5DBus)
BuildRequires: pkgconfig(Qt5Test)
BuildRequires: cmake(KF5CoreAddons)
BuildRequires: pkgconfig(polkit-qt5-1)
Requires: %{libname} = %{EVRD}

%description
KAuth is an abstraction to system policy and authentication features.

%package -n %{libname}
Summary: The KDE Frameworks 5 authentication library
Group: System/Libraries
Requires: %{name} = %{EVRD}

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
%apply_patches
%cmake_kde5 -DKAUTH_BACKEND=PolkitQt5-1 -DLIBEXEC_INSTALL_DIR=%{_kde5_libexecdir}

%build
%ninja -C build

%install
%ninja_install -C build

L="`pwd`/%{name}.lang"
cd %{buildroot}
for i in .%{_datadir}/locale/*/LC_MESSAGES/*.qm; do
	LNG=`echo $i |cut -d/ -f5`
	echo -n "%lang($LNG) " >>$L
	echo $i |cut -b2- >>$L
done

# Fix polkit-1 install directory -- /share is a bad idea.
sed -i -e 's,POLICY_FILES_INSTALL_DIR "/share,POLICY_FILES_INSTALL_DIR "share,' %{buildroot}%{_libdir}/cmake/KF5Auth/KF5AuthConfig.cmake

%files -f %{name}.lang
%{_libdir}/libexec/kauth
%{_libdir}/qt5/plugins/kauth
%{_sysconfdir}/dbus-1/system.d/org.kde.kf5auth.conf
%{_datadir}/kf5/kauth

%files -n %{libname}
%{_libdir}/*.so.%{major}
%{_libdir}/*.so.%{version}

%files -n %{devname}
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/cmake/KF5Auth
%{_libdir}/qt5/mkspecs/modules/*
