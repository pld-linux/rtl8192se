
# PLEASE READ FOLLOWING MESSAGES:
# http://lists.pld-linux.org/mailman/pipermail/pld-devel-en/2010-August/021751.html
# http://lists.pld-linux.org/mailman/pipermail/pld-devel-en/2010-August/021752.html
# http://lists.pld-linux.org/mailman/pipermail/pld-devel-en/2010-August/021753.html

# Besides that, please:
# 1) subscribe to at least one of developers mailing lists
# 2) don't use interia for @pld-linux.org forward. interia checks SPF, so it
#    will rejected most forwarded e-mails. Use gmail or some other mail
#    service that does not check SPF.

%define         jadro 2.6.33.5-1
Summary:	Firmware for the RTL8192SE chipset
%define         pname rtl8192se
Name:		rtl8192se
Version:	0017.0507.2010
%define         ver %{version}
Release:	0
License:	GPL
Group:		Base/Kernel

#rtl8192se_linux_2.6.0017.0507.2010.tar.gzProblems in TW local tar.gz 
#Source0:	ftp://WebUser:pGL7E6v@202.134.71.21/cn/wlan/rtl8192se_linux_2.6.%{version}.tar.gz
Source0:	rtl8192se_linux_2.6.%{version}.tar.gz
# Source0-md5:	0c904bb2433699bc0e2f1d86c45a6b22

#kernel scripts for %{jadro}
Source1:  	kernel_compile.tar.gz
# Source1-md5:	30f890430a2220151cf2d439546a7db1


URL:		http://www.realtek.com/products/productsView.aspx?Langid=1&PNid=21&PFid=48&Level=5&Conn=4&ProdID=226
#BuildArch:	noarch
BuildRequires:  rpmbuild(macros) >= 1.153
BuildRequires:  kernel%{_alt_kernel}-module-build >= 3:2.6.33.0}

Patch0:         %{pname}-install.patch

BuildRoot:	%{tmpdir}/%{pname}-root-%(id -u -n)

%description
This package contains the driver + firmware for the rtl8192se pci driver.

%description -l pl.UTF-8
Ten pakiet zawiera modul + firmware dla sterownika rtl8192se pci.

%prep
%setup -qc
cp %{SOURCE1} .
tar -zxf kernel_compile.tar.gz -C /usr/src --overwrite-dir

mv rtl8192se_linux_2.6.%{ver} mod
cd mod
%patch0 -p1
make all
#cd ..

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/lib/firmware/%{jadro}/

cp -a mod/firmware/* $RPM_BUILD_ROOT/lib/firmware/%{jadro}/
rm -v $RPM_BUILD_ROOT/lib/firmware/%{jadro}/RTL8192SE/*.txt

install -d $RPM_BUILD_ROOT/lib/modules/%{jadro}/kernel/drivers/net/wireless
cp -a mod/HAL/rtl8192/r8192se_pci.ko $RPM_BUILD_ROOT/lib/modules/%{jadro}/kernel/drivers/net/wireless/

install -d $RPM_BUILD_ROOT/etc/realtek
cp -a mod/realtek/* $RPM_BUILD_ROOT/etc/realtek/
 
#install -d $RPM_BUILD_ROOT/etc/realtek/events
%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc mod/firmware/RTL8192SE/Realtek-Firmware-License.txt
%doc mod/readme.txt
/lib/firmware/%{jadro}/*
/lib/modules/%{jadro}/kernel/drivers/net/wireless/*
/etc/realtek/*
%post 
%depmod %{jadro}

%postun 
%depmod %{jadro}
