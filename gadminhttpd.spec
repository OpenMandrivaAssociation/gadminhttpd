Summary:	GADMINHTTPD -- GAdminHTTPD is an easy to use GTK+ frontend for the Apache httpd webserver.
Name:		gadminhttpd
Version:	0.0.5
Release:	%mkrel 1
License:	GPL
Group:		System/Configuration/Networking
URL:		http://www.gadmintools.org/
Source0:	http://mange.dynalias.org/linux/gadminhttpd/%{name}-%{version}.tar.bz2
BuildRequires:	gtk+2-devel
BuildRequires:	ImageMagick
Requires:	apache	
Requires:	usermode-consoleonly
Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
GAdminHTTPD is an easy to use GTK+ frontend for the Apache httpd webserver.

%prep

%setup -q

%build

%configure2_5x

%make

%install
rm -rf %{buildroot}

%makeinstall INSTALL_USER=`id -un` INSTALL_GROUP=`id -gn`

# locales
%find_lang %name

# Mandriva Icons
install -d %{buildroot}%{_iconsdir}
install -d %{buildroot}%{_miconsdir}
install -d %{buildroot}%{_liconsdir}
convert -geometry 48x48 pixmaps/gadminhttpd.png %{buildroot}%{_liconsdir}/%{name}.png
convert -geometry 32x32 pixmaps/gadminhttpd.png %{buildroot}%{_iconsdir}/%{name}.png
convert -geometry 16x16 pixmaps/gadminhttpd.png %{buildroot}%{_miconsdir}/%{name}.png

# Mandriva Menus
install -d %{buildroot}/%{_menudir}
cat > %{buildroot}%{_menudir}/%{name} <<EOF
?package(%{name}): \
 command="%{_sbindir}/%{name}" \
 title="GADMINHTTPD" \
 longtitle="Apache server administration tool" \
 needs="x11" \
 icon="%{name}.png" \
 section="Configuration/Networking" \
 xdg="true" 
EOF

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=GADMINHTTPD
Comment=%{summary}
Exec=%{_sbindir}/%{name}
Icon=%{name}
Terminal=false
Type=Application
Categories=X-MandrivaLinux-System-Configuration-Networking;Settings;Network;
EOF

# Prepare usermode entry
mv %{buildroot}%{_sbindir}/gadminhttpd %{buildroot}%{_sbindir}/gadminhttpd.real
ln -s %{_bindir}/consolehelper %{buildroot}%{_sbindir}/gadminhttpd

mkdir -p %{buildroot}%{_sysconfdir}/security/console.apps
cat > %{buildroot}%{_sysconfdir}/security/console.apps/%{name} <<_EOF_
USER=root
PROGRAM=%{_sbindir}/gadminhttpd.real
SESSION=true
FALLBACK=false
_EOF_

rm -rf %{buildroot}%{_datadir}/doc/%{name}

%post
%update_menus

%postun
%clean_menus

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root,0755)
%doc COPYING AUTHORS ChangeLog
%config(noreplace) %{_sysconfdir}/security/console.apps/%{name}
%{_sbindir}/%{name}
%{_sbindir}/%{name}.real
%{_datadir}/applications/mandriva-%{name}.desktop
%{_datadir}/pixmaps/*.png
%{_datadir}/pixmaps/%{name}/*.png
%{_datadir}/pixmaps/%{name}/%{name}.png
%{_menudir}/%{name}
%{_iconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_liconsdir}/%{name}.png


