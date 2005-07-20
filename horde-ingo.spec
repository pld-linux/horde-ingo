%include	/usr/lib/rpm/macros.php
Summary:	Ingo - an email filter rules manager
Summary(pl):	Ingo - zarz±dca regu³ filtrowania poczty elektronicznej
Name:		ingo
Version:	1.0.1
Release:	1.1
License:	GPL v2
Group:		Applications/WWW
Source0:	http://ftp.horde.org/pub/ingo/%{name}-h3-%{version}.tar.gz
# Source0-md5:	7fce229d752e5b981621e215e4fc56e8
Source1:	%{name}.conf
Patch0:		%{name}-path.patch
URL:		http://www.horde.org/ingo/
BuildRequires:	rpmbuild(macros) >= 1.226
Requires:	apache >= 1.3.33-2
Requires:	apache(mod_access)
Requires:	horde >= 3.0
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# horde accesses it directly in help->about
%define		_noautocompressdoc  CREDITS
%define		_noautoreq	'pear(Horde.*)'

%define		hordedir	/usr/share/horde
%define		_appdir		%{hordedir}/%{name}
%define		_sysconfdir	/etc/horde.org

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
%setup -q -n %{name}-h3-%{version}
%patch0 -p1

# considered harmful (horde/docs/SECURITY)
rm -f test.php

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}/%{name} \
	$RPM_BUILD_ROOT%{_appdir}/{docs,lib,locale,templates,themes}

cp -pR	*.php			$RPM_BUILD_ROOT%{_appdir}
for i in config/*.dist; do
	cp -p $i $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/$(basename $i .dist)
done
cp -pR	config/*.xml		$RPM_BUILD_ROOT%{_sysconfdir}/%{name}

echo "<?php ?>" > 		$RPM_BUILD_ROOT%{_sysconfdir}/%{name}/conf.php
sed -e '
	s,dirname(__FILE__).*/cvsgraph.conf.,%{_sysconfdir}/%{name}/cvsgraph.conf,
' < config/conf.xml > $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/conf.xml
> $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/conf.php.bak

cp -pR  lib/*                   $RPM_BUILD_ROOT%{_appdir}/lib
cp -pR  locale/*                $RPM_BUILD_ROOT%{_appdir}/locale
cp -pR  templates/*             $RPM_BUILD_ROOT%{_appdir}/templates
cp -pR  themes/*                $RPM_BUILD_ROOT%{_appdir}/themes

ln -s %{_sysconfdir}/%{name} 	$RPM_BUILD_ROOT%{_appdir}/config
ln -s %{_defaultdocdir}/%{name}-%{version}/CREDITS $RPM_BUILD_ROOT%{_appdir}/docs

install %{SOURCE1} 		$RPM_BUILD_ROOT%{_sysconfdir}/apache-%{name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ ! -f %{_sysconfdir}/%{name}/conf.php.bak ]; then
	install /dev/null -o root -g http -m660 %{_sysconfdir}/%{name}/conf.php.bak
fi

%triggerin -- apache1 >= 1.3.33-2
%apache_config_install -v 1 -c %{_sysconfdir}/apache-%{name}.conf

%triggerun -- apache1 >= 1.3.33-2
%apache_config_uninstall -v 1

%triggerin -- apache >= 2.0.0
%apache_config_install -v 2 -c %{_sysconfdir}/apache-%{name}.conf

%triggerun -- apache >= 2.0.0
%apache_config_uninstall -v 2

%files
%defattr(644,root,root,755)
%doc README docs/*
%attr(750,root,http) %dir %{_sysconfdir}/%{name}
%attr(640,root,root) %config(noreplace) %{_sysconfdir}/apache-%{name}.conf
%attr(660,root,http) %config(noreplace) %{_sysconfdir}/%{name}/conf.php
%attr(660,root,http) %config(noreplace) %ghost %{_sysconfdir}/%{name}/conf.php.bak
%attr(640,root,http) %config(noreplace) %{_sysconfdir}/%{name}/[!c]*.php
%attr(640,root,http) %{_sysconfdir}/%{name}/*.xml

%dir %{_appdir}
%{_appdir}/*.php
%{_appdir}/config
%{_appdir}/docs
%{_appdir}/lib
%{_appdir}/locale
%{_appdir}/templates
%{_appdir}/themes
