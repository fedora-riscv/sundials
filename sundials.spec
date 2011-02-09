Summary:    Suite of nonlinear solvers
Name:       sundials
Version:    2.3.0
Release:    10%{?dist}

# SUNDIALS is licensed under BSD with some additional (but unrestrictive) clauses.
# Check the file 'LICENSE' for details.
License:    BSD

Group:      Development/Libraries
URL:        http://www.llnl.gov/casc/sundials/

Source0:    http://www.llnl.gov/casc/sundials/download/code/%{name}-%{version}.tar.gz

# patch replaces config/ltmain.sh with a newer one.
Patch0:     %{name}-ltmain.patch

BuildRoot:  %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

#Parallel build seems to require some fixes from upstream
# BuildRequires: openmpi-devel
BuildRequires: gcc-gfortran

%description
SUNDIALS is a SUite of Non-linear DIfferential/ALgebraic equation Solvers
for use in writing mathematical software.

SUNDIALS was implemented with the goal of providing robust time integrators
and nonlinear solvers that can easily be incorporated into existing simulation
codes. The primary design goals were to require minimal information from the
user, allow users to easily supply their own data structures underneath the
solvers, and allow for easy incorporation of user-supplied linear solvers and
preconditioners. 

%package devel
Summary:    Suite of nonlinear solvers (developer files)
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}
%description devel
SUNDIALS is a SUite of Non-linear DIfferential/ALgebraic equation Solvers
for use in writing mathematical software.

This package contains the developer files (.so file, header files)

%package static
Summary:    Suite of nonlinear solvers (static libraries)
Group:      Development/Libraries
Requires:   %{name}-devel = %{version}-%{release}
%description static
SUNDIALS is a SUite of Non-linear DIfferential/ALgebraic equation Solvers
for use in writing mathematical software.

This package contains the static library files (.a files). These libraries
provide support for using SUNDIALS from Fortran.

%package doc
Summary:    Suite of nonlinear solvers (documentation)
Group:      Documentation
%description doc
SUNDIALS is a SUite of Non-linear DIfferential/ALgebraic equation Solvers
for use in writing mathematical software.

This package contains the documentation files

%prep
%setup -q 
%patch0 -p1

%build
%configure \
  F77=gfortran \
  --enable-static=no \
  --enable-shared=yes \
  --disable-mpi
#  --with-mpi-root=%{_datadir}/openmpi

make %{?_smp_mflags}

%install
rm -rf ${RPM_BUILD_ROOT}
# SUNDIALS does not support the 'DESTDIR' method, hence:
%makeinstall

# spot says better no .la files in RPMs
rm ${RPM_BUILD_ROOT}%{_libdir}/*.la

%clean
rm -rf ${RPM_BUILD_ROOT}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc LICENSE README
%{_libdir}/*.so.[0-9].*
%{_libdir}/*.so.[0-9]

%files doc
%defattr(-,root,root,-)
%doc doc/cvode/cv_examples.pdf
%doc doc/cvode/cv_guide.pdf
%doc doc/kinsol/kin_examples.pdf
%doc doc/kinsol/kin_guide.pdf
%doc doc/cvodes/cvs_examples.pdf
%doc doc/cvodes/cvs_guide.pdf
%doc doc/ida/ida_examples.pdf
%doc doc/ida/ida_guide.pdf

%files devel
%defattr(-,root,root,-)
%{_libdir}/*.so
%{_includedir}/*
%{_bindir}/sundials-config

%files static
%defattr(-,root,root,-)
%{_libdir}/*.a

%changelog
* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Sep 21 2008 Ville Skyttä <ville.skytta at iki.fi> - 2.3.0-7
- Fix Patch0:/%%patch mismatch (#463065).

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.3.0-6
- Autorebuild for GCC 4.3

* Sat Aug 04 2007 John Pye <john@curioussymbols.com> 2.3.0-5
- Final corrections from Debarshi Ray:
- Changed all file-location macros to the curly-bracket format.
- License field changed to BSD and comments added regarding special conditions.

* Wed Aug 01 2007 John Pye <john@curioussymbols.com> 2.3.0-4
- Corrections from Mamoru Tasaka:
- Removed /sbin/ldconfig call for -devel package (not required).
- Moved *.a libraries to a -static package.
- Corrected sub/main package dependencies (added release num).
- Corrected and added extra 'defattr' statements in files sections.

* Tue Jul 31 2007 John Pye <john@curioussymbols.com> 2.3.0-3
- Removed INSTALL_NOTES.
- Added /sbin/ldconfig call for -devel package.
- Remove automake dependency.
- Changed --with-mpi-root location (currently commented out).
- Added /sbin/ldconfig call for -devel package.

* Mon Jul 30 2007 John Pye <john@curioussymbols.com> 2.3.0-2
- Removed OpenMPI dependencies (providing serial-only package at the moment).
- Fixing for Debarshi Ray's feedback:
- changed post/postun to use -p style,
- added comments for why 'makeinstall' is required,
- using macro instead of direct call to ./configure,
- replaced spaces with tabs,
- re-tagged -doc package as group Documentation,
- removed CC=... and CXX=... from %%configure command, and
- changed download location.

* Sun Jul 29 2007 John Pye <john@curioussymbols.com> 2.3.0-1
- Converting to Fedora RPM by removing distro-specific stuff.

* Wed Jun 27 2007 John Pye <john@curioussymbols.com> 2.3.0
- Creating separate devel, doc and library packages.

* Sun Jun 24 2007 John Pye <john@curioussymbols.com> 2.3.0
- Fixed problem with creation of shared libraries (correction thanks to Andrey Romanenko in Debian).

* Sat Jun 23 2007 John Pye <john@curioussymbols.com> 2.3.0
- Ported to OpenSUSE Build Service, working on support for openSUSE alongside FC6, FC7.

* Thu Jul 27 2006 John Pye <john.pye@student.unsw.edu.au> 2.3.0-0
- First RPM spec created.

