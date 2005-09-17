%define	_hordeapp ingo
#define	_snap	2005-08-26
%define	_rc		rc1
%define	_rel	1
#
%include	/usr/lib/rpm/macros.php
Summary:	Ingo - an email filter rules manager
Summary(pl):	Ingo - zarz±dca regu³ filtrowania poczty elektronicznej
Name:		%{_hordeapp}
Version:	1.0.2
Release:	%{?_rc:0.%{_rc}.}%{?_snap:0.%(echo %{_snap} | tr -d -).}%{_rel}
License:	GPL v2
Group:		Applications/WWW
Source0:	ftp://ftp.horde.org/pub/ingo/%{_hordeapp}-h3-%{version}-%{_rc}.tar.gz
# Source0-md5:	3350a61407259492e11319251ae4ab7c
Source1:	%{_hordeapp}.conf
Patch0:		%{_hordeapp}-path.patch
URL:		http://www.horde.org/ingo/
BuildRequires:	rpm-php-pearprov >= 4.0.2-98
BuildRequires:	rpmbuild(macros) >= 1.226
BuildRequires:	tar >= 1:1.15.1
Requires:	apache >= 1.3.33-2
Requires:	apache(mod_access)
Requires:	horde >= 3.0
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# horde accesses it directly in help->about
%define		_noautocompressdoc  CREDITS
%define		_noautoreq	'pear(Horde.*)'

%define		hordedir	/usr/share/horde
%define		_sysconfdir	/etc/horde.org
%define		_appdir		%{hordedir}/%{_hordeapp}

%description
Ingo currently supports the following filtering drivers:
- Sieve (using timsieved)
- procmail (using VFS FTP driver)
- IMAP client-side filtering

Ingo has replaced IMP's internal filtering code and is the default
filtering agent in IMP H3 (4.0).

The Horde Project writes web applications in PHP and releases them
under the GNU General Public License. For more information (including
help with Ingo) please visit <http://www.horde.org/>.

%description -l pl
Ingo aktualnie obs³uguje nastêpuj±ce sterowniki filtrowania:
- Sieve (przy u¿yciu timsieved)
- procmail (przy u¿yciu sterownika VFS FTP)
- filtrowanie po stronie klienta IMAP

Ingo zast±pi³ wewnêtrzny kod filtruj±cy IMP-a i jest domy¶lnym agentem
filtrowania w IMP-ie H3 (4.0).

Projekt Horde pisze aplikacje WWW w PHP i wydaje je na Powszechnej
Licencji Publicznej GNU (General Public License). Wiêcej informacji
(wraz z pomoc± do Ingo) mo¿na znale¼æ na stronie
<http://www.horde.org/>.

%prep
%setup -q -c -T -n %{?_snap:%{_hordeapp}-%{_snap}}%{!?_snap:%{_hordeapp}-%{version}%{?_rc:-%{_rc}}}
tar zxf %{SOURCE0} --strip-components=1
%patch0 -p1

# considered harmful (horde/docs/SECURITY)
rm -f test.php

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}/%{_hordeapp} \
	$RPM_BUILD_ROOT%{_appdir}/{docs,lib,locale,templates,themes}

cp -a *.php			$RPM_BUILD_ROOT%{_appdir}
for i in config/*.dist; do
	cp -a $i $RPM_BUILD_ROOT%{_sysconfdir}/%{_hordeapp}/$(basename $i .dist)
done
echo '<?php ?>' >		$RPM_BUILD_ROOT%{_sysconfdir}/%{_hordeapp}/conf.php
cp -p config/conf.xml	$RPM_BUILD_ROOT%{_sysconfdir}/%{_hordeapp}/conf.xml
touch					$RPM_BUILD_ROOT%{_sysconfdir}/%{_hordeapp}/conf.php.bak

cp -pR  lib/*                   $RPM_BUILD_ROOT%{_appdir}/lib
cp -pR  locale/*                $RPM_BUILD_ROOT%{_appdir}/locale
cp -pR  templates/*             $RPM_BUILD_ROOT%{_appdir}/templates
cp -pR  themes/*                $RPM_BUILD_ROOT%{_appdir}/themes

ln -s %{_sysconfdir}/%{_hordeapp} $RPM_BUILD_ROOT%{_appdir}/config
ln -s %{_docdir}/%{name}-%{version}/CREDITS $RPM_BUILD_ROOT%{_appdir}/docs
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/apache-%{_hordeapp}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ ! -f %{_sysconfdir}/%{_hordeapp}/conf.php.bak ]; then
	install /dev/null -o root -g http -m660 %{_sysconfdir}/%{_hordeapp}/conf.php.bak
fi

%triggerin -- apache1 >= 1.3.33-2
%apache_config_install -v 1 -c %{_sysconfdir}/apache-%{_hordeapp}.conf

%triggerun -- apache1 >= 1.3.33-2
%apache_config_uninstall -v 1

%triggerin -- apache >= 2.0.0
%apache_config_install -v 2 -c %{_sysconfdir}/apache-%{_hordeapp}.conf

%triggerun -- apache >= 2.0.0
%apache_config_uninstall -v 2

%files
%defattr(644,root,root,755)
%doc README docs/*
%attr(750,root,http) %dir %{_sysconfdir}/%{_hordeapp}
%attr(640,root,root) %config(noreplace) %{_sysconfdir}/apache-%{_hordeapp}.conf
%attr(660,root,http) %config(noreplace) %{_sysconfdir}/%{_hordeapp}/conf.php
%attr(660,root,http) %config(noreplace) %ghost %{_sysconfdir}/%{_hordeapp}/conf.php.bak
%attr(640,root,http) %config(noreplace) %{_sysconfdir}/%{_hordeapp}/[!c]*.php
%attr(640,root,http) %{_sysconfdir}/%{_hordeapp}/conf.xml

%dir %{_appdir}
%{_appdir}/*.php
%{_appdir}/config
%{_appdir}/docs
%{_appdir}/lib
%{_appdir}/locale
%{_appdir}/templates
%{_appdir}/themes
