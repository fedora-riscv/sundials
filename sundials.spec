Summary:    Suite of nonlinear solvers
Name:       sundials
Version:    2.6.0
Release:    2%{?dist}
# SUNDIALS is licensed under BSD with some additional (but unrestrictive) clauses.
# Check the file 'LICENSE' for details.
License:    BSD
Group:      Development/Libraries
URL:        http://www.llnl.gov/casc/sundials/
Source0:    http://www.llnl.gov/casc/sundials/download/code/%{name}-%{version}.tar.gz

# downstream patches
# patch0 fixes bug #926583 (ARM 64-bit building)
#Patch0:     http://ausil.fedorapeople.org/aarch64/sundials/sundials-aarch64.patch

# patches1-4 fix 1037342; fix for -Werror=format-security
#Patch1:     %{name}-cvode.patch
#Patch2:     %{name}-cvodes.patch
#Patch3:     %{name}-ida.patch
#Patch4:     %{name}-idas.patch
#Patch5:     %{name}-kinsol.patch

%ifnarch s390 s390x
BuildRequires: openmpi-devel
%endif
BuildRequires: gcc-gfortran
BuildRequires: autoconf
BuildRequires: cmake
BuildRequires: lapack-devel

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

%ifarch x86_64
# fix lib installation destination
# this seems like a hack but I cannot think of a better way to do this
sed -i 's/DESTINATION lib/DESTINATION lib64/g' src/arkode/CMakeLists.txt
sed -i 's/DESTINATION lib/DESTINATION lib64/g' src/cvode/CMakeLists.txt
sed -i 's/DESTINATION lib/DESTINATION lib64/g' src/cvodes/CMakeLists.txt
sed -i 's/DESTINATION lib/DESTINATION lib64/g' src/ida/CMakeLists.txt
sed -i 's/DESTINATION lib/DESTINATION lib64/g' src/idas/CMakeLists.txt
sed -i 's/DESTINATION lib/DESTINATION lib64/g' src/kinsol/CMakeLists.txt
sed -i 's/DESTINATION lib/DESTINATION lib64/g' src/nvec_ser/CMakeLists.txt
%endif

%build
mkdir build_dir && cd build_dir

cmake \
 -DCMAKE_C_FLAGS=%{optflags} \
 -DCMAKE_Fortran_FLAGS=%{optflags} \
 -DCMAKE_SHARED_LINKER_FLAGS="%{optflags} -lblas -llapack" \
 -DCMAKE_INSTALL_PREFIX=%{buildroot}%{_prefix} \
 -DMPI_ENABLE=ON \
 -DEXAMPLES_ENABLE=OFF -DEXAMPLES_INSTALL=OFF \
 -DBUILD_SHARED_LIBS=ON \
 -DLAPACK_ENABLE=ON ..

make V=1 %{?_smp_mflags}

%install
# SUNDIALS does not support the 'DESTDIR' method, hence:
cd build_dir
%makeinstall

# spot says better no .la files in RPMs
# This is not needed in 2.6.0
# rm ${RPM_BUILD_ROOT}%{_libdir}/*.la

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%license LICENSE
%doc README
%{_libdir}/*so*

%files doc
%doc doc/cvode/cv_examples.pdf
%doc doc/cvode/cv_guide.pdf
%doc doc/kinsol/kin_examples.pdf
%doc doc/kinsol/kin_guide.pdf
%doc doc/cvodes/cvs_examples.pdf
%doc doc/cvodes/cvs_guide.pdf
%doc doc/ida/ida_examples.pdf
%doc doc/ida/ida_guide.pdf
%doc doc/arkode/*
%doc examples/*

%files devel
%{_libdir}/*.so
%{_includedir}/*
## %{_bindir}/sundials-config

%files static
%{_libdir}/*.a

%changelog
* Sun Mar 29 2015 Mukundan Ragavan <nonamedotc@fedoraproject.org> - 2.6.0-2
- Ensure the shared libraries are linked correctly

* Sun Mar 29 2015 Mukundan Ragavan <nonamedotc@fedoraproject.org> - 2.6.0-1
- Update to 2.6.0
- Drop patches that are not needed anymore

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Mukundan Ragavan <nonamedotc@fedoraproject.org> - 2.5.0-5
- Fixed patches used in the previous build
- Fixes bug #1105767

* Wed May 21 2014 Mukundan Ragavan <nonamedotc@fedoraproject.org> - 2.5.0-4
- added patches to fix bugs #926583 and #1037342

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Feb 18 2013 Dan Horák <dan[at]danny.cz> - 2.5.0-2
- openmpi not available s390(x)

* Sun Jan 26 2013 Rahul Sundaram <sundaram@fedoraproject.org> - 2.5.0-1
- upstream release 2.5.0
- enable parallel build
- drop obsolete patch

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

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

