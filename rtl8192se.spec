#
# TODO:
# - cleanups, scripts?, kernel package name/version
#
# Conditional build:
%bcond_without  dist_kernel     # allow non-distribution kernel
%bcond_without  kernel          # don't build kernel modules
%bcond_without  userspace       # don't build userspace module
%bcond_with     verbose         # verbose build (V=1)

%if %{without kernel}
%undefine       with_dist_kernel
%endif

%define         pname rtl8192se
%define         ver %{version}
Summary:	Firmware for the RTL8192SE chipset
Name:		rtl8192se
Version:	0017.0507.2010
Release:	0.2
License:	GPL
Group:		Base/Kernel
#rtl8192se_linux_2.6.0017.0507.2010.tar.gzProblems in TW local tar.gz
#Source0:	ftp://WebUser:pGL7E6v@202.134.71.21/cn/wlan/rtl8192se_linux_2.6.%{version}.tar.gz
Source0:	http://pld.skibi.eu/%{name}_linux_2.6.%{version}.tar.gz
# Source0-md5:	0c904bb2433699bc0e2f1d86c45a6b22
URL:		http://www.realtek.com/products/productsView.aspx?Langid=1&PNid=21&PFid=48&Level=5&Conn=4&ProdID=226
Patch0:         rtl8192se-install.patch 
BuildRequires:	kernel%{_alt_kernel}-module-build >= 3:2.6.20
BuildRequires:	rpmbuild(macros) >= 1.153
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package contains the driver + firmware for the rtl8192se pci
driver.

%description -l pl.UTF-8
Ten pakiet zawiera modul + firmware dla sterownika rtl8192se pci.

%prep
%setup -q -n %{name}_linux_2.6.%{version}
%patch0 -p0

%build
cd HAL/rtl8192
%build_kernel_modules -m r8192se_pci

%install
rm -rf $RPM_BUILD_ROOT

%install_kernel_modules -m HAL/rtl8192/r8192se_pci -d kernel/drivers/net/wireless
 

install -d $RPM_BUILD_ROOT/lib/firmware/%{_kernel_ver}/RTL8192SE
install firmware/RTL8192SE/*bin $RPM_BUILD_ROOT/lib/firmware/%{_kernel_ver}/RTL8192SE

#install -d $RPM_BUILD_ROOT/lib/firmware
#install firmware/RTL8192SE/*bin $RPM_BUILD_ROOT/lib/firmware

#install -d $RPM_BUILD_ROOT%{_sysconfdir}/realtek
#cp -a mod/realtek/* $RPM_BUILD_ROOT%{_sysconfdir}/realtek/

#install -d $RPM_BUILD_ROOT%{_sysconfdir}/realtek/events
%clean
rm -rf $RPM_BUILD_ROOT

%post
%depmod %{_kernel_ver}

%postun
%depmod %{_kernel_ver}

%files
%defattr(644,root,root,755)
%doc firmware/RTL8192SE/Realtek-Firmware-License.txt readme.txt
/lib/firmware/%{_kernel_ver}/RTL8192SE/*bin
/lib/modules/%{_kernel_ver}/kernel/drivers/net/wireless/*ko*
#{_sysconfdir}/realtek/*
