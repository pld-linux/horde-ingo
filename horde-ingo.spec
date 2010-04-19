%define		hordeapp ingo
#
%include	/usr/lib/rpm/macros.php
Summary:	Ingo - an email filter rules manager
Summary(pl.UTF-8):	Ingo - zarządca reguł filtrowania poczty elektronicznej
Name:		horde-%{hordeapp}
Version:	1.2.3
Release:	1
License:	GPL v2
Group:		Applications/WWW
Source0:	ftp://ftp.horde.org/pub/ingo/%{hordeapp}-h3-%{version}.tar.gz
# Source0-md5:	f17547019c9db2e47b393724be67197c
Source1:	%{hordeapp}.conf
Patch0:		%{hordeapp}-path.patch
URL:		http://www.horde.org/ingo/
BuildRequires:	rpm-php-pearprov >= 4.0.2-98
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	horde >= 3.0
Requires:	php(imap)
Requires:	webapps
Suggests:	php-pear-Net_Sieve >= 1.0.1
Suggests:	php-pear-Net_Socket
Obsoletes:	ingo
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_noautoreq	'pear(/usr/share/horde.*)' 'pear(Horde.*)'

%define		hordedir	/usr/share/horde
%define		_appdir		%{hordedir}/%{hordeapp}
%define		_webapps	/etc/webapps
%define		_webapp		horde-%{hordeapp}
%define		_sysconfdir	%{_webapps}/%{_webapp}

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

%description -l pl.UTF-8
Ingo aktualnie obsługuje następujące sterowniki filtrowania:
- Sieve (przy użyciu timsieved)
- procmail (przy użyciu sterownika VFS FTP)
- filtrowanie po stronie klienta IMAP

Ingo zastąpił wewnętrzny kod filtrujący IMP-a i jest domyślnym agentem
filtrowania w IMP-ie H3 (4.0).

Projekt Horde pisze aplikacje WWW w PHP i wydaje je na Powszechnej
Licencji Publicznej GNU (General Public License). Więcej informacji
(wraz z pomocą do Ingo) można znaleźć na stronie
<http://www.horde.org/>.

%prep
%setup -q -n %{hordeapp}-h3-%{version}
%patch0 -p1

rm */.htaccess
for i in config/*.dist; do
	mv $i config/$(basename $i .dist)
done
# considered harmful (horde/docs/SECURITY)
rm test.php

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_appdir}/docs}

cp -a *.php $RPM_BUILD_ROOT%{_appdir}
cp -a config/* $RPM_BUILD_ROOT%{_sysconfdir}
echo '<?php ?>' > $RPM_BUILD_ROOT%{_sysconfdir}/conf.php
touch $RPM_BUILD_ROOT%{_sysconfdir}/conf.php.bak
cp -a js lib locale templates themes $RPM_BUILD_ROOT%{_appdir}
cp -a docs/CREDITS $RPM_BUILD_ROOT%{_appdir}/docs

ln -s %{_sysconfdir} $RPM_BUILD_ROOT%{_appdir}/config
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ ! -f %{_sysconfdir}/conf.php.bak ]; then
	install /dev/null -o root -g http -m660 %{_sysconfdir}/conf.php.bak
fi

%triggerin -- apache1 < 1.3.37-3, apache1-base
%webapp_register apache %{_webapp}

%triggerun -- apache1 < 1.3.37-3, apache1-base
%webapp_unregister apache %{_webapp}

%triggerin -- apache < 2.2.0, apache-base
%webapp_register httpd %{_webapp}

%triggerun -- apache < 2.2.0, apache-base
%webapp_unregister httpd %{_webapp}

%files
%defattr(644,root,root,755)
%doc README docs/*
%dir %attr(750,root,http) %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%attr(660,root,http) %config(noreplace) %{_sysconfdir}/conf.php
%attr(660,root,http) %config(noreplace) %ghost %{_sysconfdir}/conf.php.bak
%attr(640,root,http) %config(noreplace) %{_sysconfdir}/[!c]*.php
%attr(640,root,http) %{_sysconfdir}/conf.xml

%dir %{_appdir}
%{_appdir}/*.php
%{_appdir}/config
%{_appdir}/docs
%{_appdir}/js
%{_appdir}/lib
%{_appdir}/locale
%{_appdir}/templates
%{_appdir}/themes
