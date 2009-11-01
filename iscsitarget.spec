Name:           iscsitarget
Version:        1.4.18
Release:        1%{?dist}
Epoch:          1
Summary:        Utilities for iSCSI Enterprise Target 

Group:          System Environment/Daemons
License:        GPLv2
URL:            http://sourceforge.net/projects/iscsitarget/
Source0:        http://dl.sf.net/iscsitarget/%{name}-%{version}.tar.gz
Patch1:         iscsitarget-1.4.18-initscript.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:       %{name}-kmod >= %{epoch}:%{version}
Provides:       %{name}-kmod-common = %{epoch}:%{version}
BuildRequires:  openssl-devel

Requires(post): /sbin/chkconfig
Requires(preun): /sbin/chkconfig
Requires(preun): /sbin/service

%description
An open source iSCSI target with professional features,
works well in enterprise environment under real workload,
and is scalable and versatile enough to meet the challenge
of future storage needs.


%prep
%setup -q
%patch1 -p1 -b .initscript


%build
make CFLAGS="%{optflags} -I../include -D_GNU_SOURCE" -C usr %{?_smp_flags}


%install
rm -rf $RPM_BUILD_ROOT
make DISTDIR=$RPM_BUILD_ROOT install-usr install-etc install-man
install -d $RPM_BUILD_ROOT%{_sysconfdir}/rc.d
mv $RPM_BUILD_ROOT%{_sysconfdir}/init.d $RPM_BUILD_ROOT%{_sysconfdir}/rc.d


%clean
rm -rf $RPM_BUILD_ROOT


%post
# This adds the proper /etc/rc*.d links for the script
/sbin/chkconfig --add iscsi-target


%preun
if [ $1 = 0 ]; then
        /sbin/service iscsi-target stop >/dev/null 2>&1
        /sbin/chkconfig --del iscsi-target
fi


%files
%defattr(-,root,root,-)
%doc COPYING README README.vmware ChangeLog
%{_sbindir}/ietd
%{_sbindir}/ietadm
%attr(600,root,root) %config(noreplace) %{_sysconfdir}/ietd.conf
%config(noreplace) %{_sysconfdir}/initiators.allow
%config(noreplace) %{_sysconfdir}/initiators.deny
%{_initrddir}/iscsi-target
%{_mandir}/man5/ietd.conf.5*
%{_mandir}/man8/ietadm.8*
%{_mandir}/man8/ietd.8*


%changelog
* Sun Nov 01 2009 Lubomir Rintel <lkundrak@v3.sk> - 1:1.4.18-1
- Update to new upstream release

* Sun Sep 13 2009 Hans de Goede <j.w.r.degoede@hhs.nl> - 1:0.4.17-5
- silence crc32c_intel loading failure on amd machines

* Sun Sep 13 2009 Hans de Goede <j.w.r.degoede@hhs.nl> - 1:0.4.17-4
- rebuild for new ssl

* Sun Mar 29 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1:0.4.17-3
- rebuild for new F11 features

* Wed Feb 04 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1:0.4.17-2
- rebuild for new ssl

* Mon Jan 05 2009 Lubomir Rintel <lkundrak@v3.sk> - 1:0.4.17-1
- Latest upstream
- Drop unneeded patches
- Fix ietd.conf mode (#170)

* Wed Oct 15 2008 Hans de Goede <j.w.r.degoede@hhs.nl> - 1:0.4.15-11.svn142
- Fix building with latest glibc (needs _GNU_SOURCE to be defined)

* Fri Oct 03 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info - 1:0.4.15-10.svn142
- rebuild for rpm fusion

* Fri Jan 25 2008 Lubomir Kundrak <lkundrak@redhat.com> - 1:0.4.15-9.svn142
- Init script needs bash to run (Thanks to Rolf Fokkens)

* Sun Dec 23 2007 Lubomir Kundrak <lkundrak@redhat.com> - 1:0.4.15-8.svn142
- Corrected dependencies to take Epoch into account (Thanks Ville Skyttä)

* Sun Dec 09 2007 Lubomir Kundrak <lkundrak@redhat.com> - 1:0.4.15-7.svn142
- No need to try to patch the kernel module, we build userland

* Sun Dec 09 2007 Lubomir Kundrak <lkundrak@redhat.com> - 1:0.4.15-6.svn142
- Require the proper name of the kernel module
- Correct the versioning
- Stop the daemon upon package removal
- Describe how the patch was generated

* Thu Nov 08 2007 Lubomir Kundrak <lkundrak@redhat.com> - 0.4.15.svn142-5
- Fixed the init script to comply with Fedora guidelines

* Thu Nov 08 2007 Lubomir Kundrak <lkundrak@redhat.com> - 0.4.15.svn142-4
- Adjusted for kmodtool

* Thu Oct 18 2007 Tom G. Christensen <swpkg@statsbiblioteket.dk> - 0.4.15-3
- Build for kernel pointed to by kmdl_kernelsrcdir instead
  of running kernel

* Fri Oct  5 2007 Tom G. Christensen <swpkg@statsbiblioteket.dk> - 0.4.15-2
- Initial build.
