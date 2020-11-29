%define major 5
%define libname %mklibname KF5Auth %{major}
%define devname %mklibname KF5Auth -d
%define stable %([ "`echo %{version} |cut -d. -f3`" -ge 80 ] && echo -n un; echo -n stable)
%define debug_package %{nil}

Name: kauth
Version: 5.76.0
Release: 3
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
# For Python bindings
BuildRequires: cmake(PythonModuleGeneration)
BuildRequires: pkgconfig(python3)
BuildRequires: python-qt5-core
BuildRequires: python-qt5-gui
BuildRequires: python-qt5-widgets
BuildRequires: python-kcoreaddons
BuildRequires: python-sip4
BuildRequires: python-sip4-qt5
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

%package -n python-%{name}
Summary: Python bindings for %{name}
Group: System/Libraries
Requires: %{libname} = %{EVRD}

%description -n python-%{name}
Python bindings for %{name}

%prep
%autosetup -p1
%cmake_kde5 \
	-DLIBEXEC_INSTALL_DIR=%{_kde5_libexecdir}

if grep -qE '^KAUTH_BACKEND_NAME:STRING=FAKE' CMakeCache.txt; then
	echo "Not building any valid backends. Double-check cmake parameters,"
	echo "in particular KAUTH_BACKEND_NAME"
	exit 1
fi

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

# Let's not ship py2 crap unless and until something still needs it...
rm -rf %{buildroot}%{_libdir}/python2*

[ -s %{buildroot}%{python_sitearch}/PyKF5/__init__.py ] || rm -f %{buildroot}%{python_sitearch}/PyKF5/__init__.py

%files -f %{name}.lang
%{_libdir}/qt5/plugins/kauth
%{_datadir}/qlogging-categories5/kauth.categories
%{_datadir}/qlogging-categories5/kauth.renamecategories
%{_datadir}/dbus-1/system.d/org.kde.kf5auth.conf
%{_datadir}/kf5/kauth

%files -n %{libname}
%{_libdir}/*.so.%{major}
%{_libdir}/*.so.%{version}

%files -n %{devname}
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/cmake/KF5Auth
%{_libdir}/qt5/mkspecs/modules/*
%{_libdir}/libexec/kauth/kauth-policy-gen

%files -n %{name}-devel-docs
%{_docdir}/qt5/*.{tags,qch}

%files -n python-%{name}
%dir %{python_sitearch}/PyKF5
%{python_sitearch}/PyKF5/KAuth.so
%dir %{_datadir}/sip/PyKF5
%{_datadir}/sip/PyKF5/KAuth
