%define major 5
%define libname %mklibname KF5Auth %{major}
%define devname %mklibname KF5Auth -d
%define stable %([ "`echo %{version} |cut -d. -f3`" -ge 80 ] && echo -n un; echo -n stable)

%define __requires_exclude cmake.*PolkitQt

Name: kauth
Version: 5.105.0
Release: 1
Source0: http://download.kde.org/%{stable}/frameworks/%(echo %{version} |cut -d. -f1-2)/%{name}-%{version}.tar.xz
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
Obsoletes: python-%{name} < %{EVRD}
# For QCH format docs
BuildRequires: doxygen
BuildRequires: qt5-assistant
BuildRequires: kcoreaddons-devel-docs
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

%package -n %{name}-devel-docs
Summary: Developer documentation for %{name} for use with Qt Assistant
Group: Documentation
Suggests: %{devname} = %{EVRD}

%description -n %{name}-devel-docs
Developer documentation for %{name} for use with Qt Assistant

%prep
%autosetup -p1
%cmake_kde5 \
	-DKDE_INSTALL_LIBEXECDIR=%{_kde5_libexecdir}

if grep -qE '^KAUTH_BACKEND_NAME:STRING=FAKE' CMakeCache.txt; then
    echo "Not building any valid backends. Double-check cmake parameters,"
    echo "in particular KAUTH_BACKEND_NAME"
    exit 1
fi

%build
%ninja -C build

%install
%ninja_install -C build

L="$(pwd)/%{name}.lang"
cd %{buildroot}
for i in .%{_datadir}/locale/*/LC_MESSAGES/*.qm; do
    LNG=$(echo $i |cut -d/ -f5)
    echo -n "%lang($LNG) " >>$L
    echo $i |cut -b2- >>$L
done

# Fix polkit-1 install directory -- /share is a bad idea.
sed -i -e 's,POLICY_FILES_INSTALL_DIR "/share,POLICY_FILES_INSTALL_DIR "share,' %{buildroot}%{_libdir}/cmake/KF5Auth/KF5AuthConfig.cmake

%files -f %{name}.lang
%{_libdir}/qt5/plugins/kauth
%{_datadir}/qlogging-categories5/kauth.categories
%{_datadir}/qlogging-categories5/kauth.renamecategories
%{_datadir}/dbus-1/system.d/org.kde.kf5auth.conf
%{_datadir}/kf5/kauth
%dir %{_kde5_libexecdir}/kauth
%{_kde5_libexecdir}/kauth/kauth-policy-gen

%files -n %{libname}
%{_libdir}/*.so.%{major}
%{_libdir}/*.so.%{version}

%files -n %{devname}
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/cmake/KF5Auth
%{_libdir}/qt5/mkspecs/modules/*

%files -n %{name}-devel-docs
%{_docdir}/qt5/*.{tags,qch}
