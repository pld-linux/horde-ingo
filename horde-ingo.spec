%define	_hordeapp ingo
#define	_snap	2005-08-26
#define	_rc		rc2
%define	_rel	1
#
%include	/usr/lib/rpm/macros.php
Summary:	Ingo - an email filter rules manager
Summary(pl):	Ingo - zarz±dca regu³ filtrowania poczty elektronicznej
Name:		horde-%{_hordeapp}
Version:	1.1.1
Release:	%{?_rc:0.%{_rc}.}%{?_snap:0.%(echo %{_snap} | tr -d -).}%{_rel}
License:	GPL v2
Group:		Applications/WWW
Source0:	ftp://ftp.horde.org/pub/ingo/%{_hordeapp}-h3-%{version}.tar.gz
# Source0-md5:	be8dacd3f52784983c74808e116c4d3d
#Source0:	ftp://ftp.horde.org/pub/ingo/%{_hordeapp}-h3-%{version}-%{_rc}.tar.gz
Source1:	%{_hordeapp}.conf
Patch0:		%{_hordeapp}-path.patch
URL:		http://www.horde.org/ingo/
BuildRequires:	rpm-php-pearprov >= 4.0.2-98
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	tar >= 1:1.15.1
Requires:	horde >= 3.0
Requires:	webapps
Obsoletes:	%{_hordeapp}
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# horde accesses it directly in help->about
%define		_noautocompressdoc  CREDITS
%define		_noautoreq	'pear(Horde.*)'

%define		hordedir	/usr/share/horde
%define		_appdir		%{hordedir}/%{_hordeapp}
%define		_webapps	/etc/webapps
%define		_webapp		horde-%{_hordeapp}
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
%setup -qcT -n %{?_snap:%{_hordeapp}-%{_snap}}%{!?_snap:%{_hordeapp}-%{version}%{?_rc:-%{_rc}}}
tar zxf %{SOURCE0} --strip-components=1
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
cp -a lib locale templates themes $RPM_BUILD_ROOT%{_appdir}

ln -s %{_sysconfdir} $RPM_BUILD_ROOT%{_appdir}/config
ln -s %{_docdir}/%{name}-%{version}/CREDITS $RPM_BUILD_ROOT%{_appdir}/docs
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

%triggerpostun -- horde-%{_hordeapp} < 1.1-0.rc2.0.6, %{_hordeapp}
for i in backends.php conf.php fields.php prefs.php; do
	if [ -f /etc/horde.org/%{_hordeapp}/$i.rpmsave ]; then
		mv -f %{_sysconfdir}/$i{,.rpmnew}
		mv -f /etc/horde.org/%{_hordeapp}/$i.rpmsave %{_sysconfdir}/$i
	fi
done

if [ -f /etc/horde.org/apache-%{_hordeapp}.conf.rpmsave ]; then
	mv -f %{_sysconfdir}/apache.conf{,.rpmnew}
	mv -f %{_sysconfdir}/httpd.conf{,.rpmnew}
	cp -f /etc/horde.org/apache-%{_hordeapp}.conf.rpmsave %{_sysconfdir}/apache.conf
	cp -f /etc/horde.org/apache-%{_hordeapp}.conf.rpmsave %{_sysconfdir}/httpd.conf
fi

if [ -L /etc/apache/conf.d/99_horde-%{_hordeapp}.conf ]; then
	/usr/sbin/webapp register apache %{_webapp}
	rm -f /etc/apache/conf.d/99_horde-%{_hordeapp}.conf
	%service -q apache reload
fi
if [ -L /etc/httpd/httpd.conf/99_horde-%{_hordeapp}.conf ]; then
	/usr/sbin/webapp register httpd %{_webapp}
	rm -f /etc/httpd/httpd.conf/99_horde-%{_hordeapp}.conf
	%service -q httpd reload
fi

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
%{_appdir}/lib
%{_appdir}/locale
%{_appdir}/templates
%{_appdir}/themes
