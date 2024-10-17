%define	version 1.13.16
%define	qversion 1.40c
%define release	8

Summary:	TetriNET server
Name:		tetrinetx
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Games/Other
URL:		https://tetrinetx.sf.net/
Buildroot:	%{_tmppath}/%{name}-%{version}-buildroot
Source:		%{name}-%{version}+qirc-%{qversion}.tar.bz2
Source1:	%{name}.init.bz2
# (Abel) 1.3.16-1mdk don't search for all files under cwd
Patch0:		%{name}-1.13.16-filepath.patch.bz2
# (Abel) 1.3.16-1mdk more secure default config
Patch1:		%{name}-1.13.16-config.patch.bz2
BuildRequires:	libadns-devel
Requires(post,preun):	rpm-helper

%description
Tetrinet is a multiplayer tetris game with special blocks and supports
up to 6 players at once. You can choose either playing team with your
buddies or individually against all tetrinet addicts around the world.
You can also chat with other players during the game.

Tetrinet-x is an open source implementation of Tetrinet server.

%prep
%setup -q -n %{name}-%{version}+qirc-%{qversion}
%patch0 -p1 -b .filepath
%patch1 -p1

%build
cd src
%__cc $RPM_OPT_FLAGS -fno-omit-frame-pointer -Wall main.c -o tetrix -ladns

%install
rm -rf %{buildroot}
install -D -m 0755 src/tetrix %{buildroot}%{_gamesbindir}/tetrix

mkdir -p %{buildroot}%{_initrddir}
bzcat %{SOURCE1} > %{buildroot}%{_initrddir}/%{name}

mkdir -p %{buildroot}%{_sysconfdir}/%{name}
install -m 0644 bin/* %{buildroot}%{_sysconfdir}/%{name}/

mkdir -p %{buildroot}/var/log/%{name}
mkdir -p %{buildroot}%{_localstatedir}/lib/games/%{name}
touch %{buildroot}%{_localstatedir}/lib/games/%{name}/game.winlist{,2,3}

%clean
rm -rf %{buildroot}

%post
%_post_service %{name}

%preun
%_preun_service %{name}

%files
%defattr(0644,root,root,0755)
%doc AUTHORS ChangeLog COPYING README README.qirc.spectators
%attr(2555,root,games) %{_gamesbindir}/*
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/game.allow
%config(noreplace) %{_sysconfdir}/%{name}/game.ban
%config(noreplace) %{_sysconfdir}/%{name}/game.ban.compromise
%config(noreplace) %{_sysconfdir}/%{name}/game.conf
%config(noreplace) %{_sysconfdir}/%{name}/game.motd
%config(noreplace) %{_sysconfdir}/%{name}/game.pmotd
%attr(0755,root,root) %config(noreplace) %{_initrddir}/%{name}

%defattr(0640,root,games)
%config(noreplace) %{_sysconfdir}/%{name}/game.secure

%defattr(0660,root,games,0770)
%dir %{_localstatedir}/lib/games/tetrinetx
%ghost %{_localstatedir}/lib/games/tetrinetx/game.winlist
%ghost %{_localstatedir}/lib/games/tetrinetx/game.winlist2
%ghost %{_localstatedir}/lib/games/tetrinetx/game.winlist3
%dir /var/log/%{name}



%changelog
* Wed Sep 09 2009 Thierry Vignaud <tvignaud@mandriva.com> 1.13.16-7mdv2010.0
+ Revision: 434348
- rebuild

* Sat Aug 02 2008 Thierry Vignaud <tvignaud@mandriva.com> 1.13.16-6mdv2009.0
+ Revision: 261509
- rebuild

* Wed Jul 30 2008 Thierry Vignaud <tvignaud@mandriva.com> 1.13.16-5mdv2009.0
+ Revision: 254399
- rebuild

  + Pixel <pixel@mandriva.com>
    - adapt to %%_localstatedir now being /var instead of /var/lib (#22312)

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Tue Dec 18 2007 Thierry Vignaud <tvignaud@mandriva.com> 1.13.16-3mdv2008.1
+ Revision: 131800
- fix prereq on rpm-helper
- kill re-definition of %%buildroot on Pixel's request
- use %%mkrel
- import tetrinetx


* Sat Jun 11 2005 Abel Cheung <deaddog@mandrivalinux.org> 1.13.16-3mdk
- Rebuild


* Fri May 14 2004 Michael Scherer <misc@mandrake.org> 1.13.16-2mdk 
- correct unsatisfied Buildrequires
- correct various rpmlint error

* Wed Sep 24 2003 Abel Cheung <deaddog@deaddog.org> 1.13.16-1mdk
- First Mandrake package, tetrinetx-1.3.16+qirc-1.40c
- Patch0: Make tetrinet-x search for files in FHS compliant paths
- Patch1: More secure default config
