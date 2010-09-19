#
# TODO:
# - cleanups, scripts?, kernel package name/version
#
# Conditional build:
%bcond_without  dist_kernel     # allow non-distribution kernel
%bcond_without  kernel          # don't build kernel modules
%bcond_without  userspace       # don't build userspace module
%bcond_with     verbose         # verbose build (V=1)
%bcond_without  nolps           # DENABLE_LPS 

%if %{without kernel}
%undefine       with_dist_kernel
%endif


# nothing to be placed to debuginfo package
%define		_enable_debug_packages	0

%define		pname	rtl8192se
%define		rel		2
Summary:	Firmware for the RTL8192SE chipset
Name:		rtl8192se
Version:	0017.0705.2010
Release:	%{rel}
License:	GPL
Group:		Base/Kernel
Source0:	http://pld.skibi.eu/%{name}_linux_2.6.%{version}.tar.gz
# Source0-md5:	b3ea880c34114560adeafa228b2f0735
URL:		http://www.realtek.com/products/productsView.aspx?Langid=1&PNid=21&PFid=48&Level=5&Conn=4&ProdID=226
Patch0:		%{name}-install.patch
Patch1:		%{name}-nolps.patch
BuildRequires:	kernel%{_alt_kernel}-module-build >= 3:2.6.20
BuildRequires:	rpmbuild(macros) >= 1.153
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package contains the driver + firmware for the rtl8192se pci
driver.

%description -l pl.UTF-8
Ten pakiet zawiera modul + firmware dla sterownika rtl8192se pci.

%package -n kernel%{_alt_kernel}-net-rtl8192se
Summary:	Linux driver for rtl8192se
Summary(pl.UTF-8):	Sterownik dla Linuksa do rtl8192se
Release:	%{rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel
Requires(postun):	%releq_kernel
%endif

%description -n kernel%{_alt_kernel}-net-rtl8192se
This is driver for rtl8192se for Linux.

This package contains Linux module.

%description -n kernel%{_alt_kernel}-net-rtl8192se -l pl.UTF-8
Sterownik dla Linuksa do rtl8192se.

Ten pakiet zawiera moduł jądra Linuksa.

%prep
%setup -q -n %{name}_linux_2.6.%{version}
%patch0 -p0

%if %{without nolps}
%patch1 -p0
%endif

%build
cd HAL/rtl8192
%build_kernel_modules -m r8192se_pci

%install
rm -rf $RPM_BUILD_ROOT
%install_kernel_modules -m HAL/rtl8192/r8192se_pci -d kernel/drivers/net/wireless

install -d $RPM_BUILD_ROOT/lib/firmware/%{_kernel_ver}/RTL8192SE
cp -a firmware/RTL8192SE/*bin $RPM_BUILD_ROOT/lib/firmware/%{_kernel_ver}/RTL8192SE

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n kernel%{_alt_kernel}-net-rtl8192se
%depmod %{_kernel_ver}

%postun	-n kernel%{_alt_kernel}-net-rtl8192se
%depmod %{_kernel_ver}

%files -n kernel%{_alt_kernel}-net-rtl8192se
%defattr(644,root,root,755)
%doc firmware/RTL8192SE/Realtek-Firmware-License.txt readme.txt
/lib/firmware/%{_kernel_ver}/RTL8192SE/*bin
/lib/modules/%{_kernel_ver}/kernel/drivers/net/wireless/*ko*
