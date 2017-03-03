## Debug builds?
%bcond_with debug
#

%if 0%{?rhel} && 0%{?rhel} < 7
%{!?__global_ldflags: %global __global_ldflags -Wl,-z,relro}
%endif

## Define if use openmpi or not
%ifarch s390x
%if 0%{?fedora} >= 26
%global with_mpich 1
%global with_openmpi 1
%else
%global with_mpich 0
%global with_openmpi 0
%endif
%endif

# No MPICH support on these arches
%if 0%{?rhel} || 0%{?rhel} < 7
%ifarch %{power64}
%global with_mpich 0
%endif
%endif
%if 0%{?rhel} || 0%{?rhel} < 7
%ifnarch %{power64}
%global with_mpich 1
%endif
%endif
%if 0%{?fedora} || 0%{?rhel} >= 7
%global with_mpich 1
%endif

%global with_parcheck 1
%global with_sercheck 1

Summary:    Suite of nonlinear solvers
Name:       sundials
Version:    2.7.0
Release:    9%{?dist}
# SUNDIALS is licensed under BSD with some additional (but unrestrictive) clauses.
# Check the file 'LICENSE' for details.
License:    BSD
Group:      Development/Libraries
URL:        http://www.llnl.gov/casc/sundials/
Source0:    http://www.llnl.gov/casc/sundials/download/code/%{name}-%{version}.tar.gz

# This patch rename superLUMT library
Patch0:     %{name}-%{version}-set_superlumt_name.patch

BuildRequires: gcc-gfortran
BuildRequires: suitesparse-devel
BuildRequires: cmake
BuildRequires: lapack-devel
BuildRequires: blas-devel

# SuperLUMT is unavailable on following architectures
%ifnarch %{power64} aarch64
BuildRequires: SuperLUMT-devel
%endif
BuildRequires: hypre-devel
%if 0%{?rhel}
BuildRequires: rsh
%endif

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
Requires:   %{name}%{?_isa} = %{version}-%{release}
Provides:   %{name}-static = %{version}-%{release}
%description devel
SUNDIALS is a SUite of Non-linear DIfferential/ALgebraic equation Solvers
for use in writing mathematical software.
This package contains the developer files (.so file, header files).

%package openmp
Summary:    Suite of nonlinear solvers with OpenMP
Group:      Development/Libraries
%description openmp
SUNDIALS is a SUite of Non-linear DIfferential/ALgebraic equation Solvers
for use in writing mathematical software.
This package contains Sundials libraries with OpenMP support.

%package openmp-devel
Summary:    Suite of nonlinear solvers with OpenMP (developer files)
Group:      Development/Libraries
Requires:   %{name}-openmp%{?_isa} = %{version}-%{release}
Requires:   %{name}-devel%{?_isa} = %{version}-%{release}
%description openmp-devel
SUNDIALS is a SUite of Non-linear DIfferential/ALgebraic equation Solvers
for use in writing mathematical software.
This package contains the developer files (.so file).

%package fortran-openmp
Summary:    Suite of nonlinear solvers with OpenMP
Group:      Development/Libraries
%description fortran-openmp
SUNDIALS is a SUite of Non-linear DIfferential/ALgebraic equation Solvers
for use in writing mathematical software.
This package contains Sundials fortran libraries with OpenMP support.

%package fortran-openmp-devel
Summary:    Suite of nonlinear solvers with OpenMP (developer files)
Group:      Development/Libraries
Requires:   %{name}-fortran-openmp%{?_isa} = %{version}-%{release}
Requires:   %{name}-devel%{?_isa} = %{version}-%{release}
%description fortran-openmp-devel
SUNDIALS is a SUite of Non-linear DIfferential/ALgebraic equation Solvers
for use in writing mathematical software.
This package contains the developer files (.so file).
#############################################################################
#########
%if 0%{?with_openmpi}
%package openmpi
Summary:    Suite of nonlinear solvers
Group:      Development/Libraries
BuildRequires: openmpi-devel
BuildRequires: hypre-openmpi-devel
Requires: openmpi
%description openmpi
SUNDIALS is a SUite of Non-linear DIfferential/ALgebraic equation Solvers
for use in writing mathematical software.
This package contains the Sundials Fortran parallel OpenMPI libraries.

%package openmpi-devel
Summary:    Suite of nonlinear solvers (static libraries)
Group:      Development/Libraries
Requires:   %{name}-openmpi%{?_isa} = %{version}-%{release}
%description openmpi-devel
SUNDIALS is a SUite of Non-linear DIfferential/ALgebraic equation Solvers
for use in writing mathematical software.
This package contains the Sundials parallel OpenMPI devel libraries and
header files.

%package fortran-openmpi
Summary:    Suite of nonlinear solvers
Group:      Development/Libraries
Requires:   gcc-gfortran%{?_isa}
Requires: openmpi
%description fortran-openmpi
SUNDIALS is a SUite of Non-linear DIfferential/ALgebraic equation Solvers
for use in writing mathematical software.
This package contains the Sundials Fortran parallel OpenMPI libraries.

%package fortran-openmpi-devel
Summary:    Suite of nonlinear solvers
Group:      Development/Libraries
Requires:   %{name}-fortran-openmpi%{?_isa} = %{version}-%{release}
%description fortran-openmpi-devel
SUNDIALS is a SUite of Non-linear DIfferential/ALgebraic equation Solvers
for use in writing mathematical software.
This package contains the Sundials Fortran parallel OpenMPI devel libraries and
header files.
%endif
######
###############################################################################
######
%if 0%{?with_mpich}
%package mpich
Summary:    Suite of nonlinear solvers
Group:      Development/Libraries
BuildRequires: mpich-devel
BuildRequires: hypre-mpich-devel
Requires: mpich
%description mpich
SUNDIALS is a SUite of Non-linear DIfferential/ALgebraic equation Solvers
for use in writing mathematical software.
This package contains the Sundials parallel MPICH libraries.

%package mpich-devel
Summary:    Suite of nonlinear solvers (static libraries)
Group:      Development/Libraries
Requires:   %{name}-mpich%{?_isa} = %{version}-%{release}
%description mpich-devel
SUNDIALS is a SUite of Non-linear DIfferential/ALgebraic equation Solvers
for use in writing mathematical software.
This package contains the Sundials parallel MPICH devel libraries and
header files.

%package fortran-mpich
Summary:    Suite of nonlinear solvers
Group:      Development/Libraries
Requires:   gcc-gfortran%{?_isa}
Requires:   mpich
%description fortran-mpich
SUNDIALS is a SUite of Non-linear DIfferential/ALgebraic equation Solvers
for use in writing mathematical software.
This package contains the Sundials Fortran parallel MPICH libraries.

%package fortran-mpich-devel
Summary:    Suite of nonlinear solvers
Group:      Development/Libraries
Requires:   %{name}-fortran-mpich%{?_isa} = %{version}-%{release}
%description fortran-mpich-devel
SUNDIALS is a SUite of Non-linear DIfferential/ALgebraic equation Solvers
for use in writing mathematical software.
This package contains the Sundials Fortran parallel MPICH devel libraries and
header files.
%endif
######
#############################################################################

%package fortran
Summary:    Suite of nonlinear solvers (static libraries)
Group:      Development/Libraries
Requires:   gcc-gfortran%{?_isa}
%description fortran
SUNDIALS is a SUite of Non-linear DIfferential/ALgebraic equation Solvers
for use in writing mathematical software.
This package contains the Sundials Fortran libraries.

## Cannot build shared libraries for the FCMIX (Fortran) interfaces 
## due to unresolved symbol errors 
## coming from inexistent user-provided functions.
## This package provides some static libraries
%package fortran-devel
Summary:    Suite of nonlinear solvers
Group:      Development/Libraries
Requires:   %{name}-fortran%{?_isa} = %{version}-%{release}
Provides:   %{name}-fortran-static = %{version}-%{release}
%description fortran-devel
SUNDIALS is a SUite of Non-linear DIfferential/ALgebraic equation Solvers
for use in writing mathematical software.
This package contains the Sundials Fortran devel libraries and
header files.

%package threads
Summary:    Suite of nonlinear solvers
Group:      Development/Libraries
%description threads
SUNDIALS is a SUite of Non-linear DIfferential/ALgebraic equation Solvers
for use in writing mathematical software.
This package contains the Sundials libraries (included the Fortran ones)
compiled with threading support.

%package threads-devel
Summary:    Suite of nonlinear solvers
Group:      Development/Libraries
Requires:   %{name}-threads%{?_isa} = %{version}-%{release}
%description threads-devel
SUNDIALS is a SUite of Non-linear DIfferential/ALgebraic equation Solvers
for use in writing mathematical software.
This package contains the Sundials devel library compiled with threading support
and relative header files.

%package doc
Summary:    Suite of nonlinear solvers (documentation)
Group:      Documentation
BuildArch: noarch
%description doc
SUNDIALS is a SUite of Non-linear DIfferential/ALgebraic equation Solvers
for use in writing mathematical software.
This package contains the documentation files.

%prep
%setup -qc

pushd sundials-%{version}
%ifnarch %{power64} aarch64
%patch0 -p0
%endif
##Set destination library's paths
sed -i 's/DESTINATION lib/DESTINATION %{_lib}/g' src/arkode/CMakeLists.txt
sed -i 's|DESTINATION lib|DESTINATION %{_lib}|g' src/arkode/fcmix/CMakeLists.txt
sed -i 's/DESTINATION lib/DESTINATION %{_lib}/g' src/cvode/CMakeLists.txt
sed -i 's|DESTINATION lib|DESTINATION %{_lib}|g' src/cvode/fcmix/CMakeLists.txt
sed -i 's/DESTINATION lib/DESTINATION %{_lib}/g' src/cvodes/CMakeLists.txt
sed -i 's/DESTINATION lib/DESTINATION %{_lib}/g' src/ida/CMakeLists.txt
sed -i 's|DESTINATION lib|DESTINATION %{_lib}|g' src/ida/fcmix/CMakeLists.txt
sed -i 's/DESTINATION lib/DESTINATION %{_lib}/g' src/idas/CMakeLists.txt
sed -i 's/DESTINATION lib/DESTINATION %{_lib}/g' src/kinsol/CMakeLists.txt
sed -i 's|DESTINATION lib|DESTINATION %{_lib}|g' src/kinsol/fcmix/CMakeLists.txt
sed -i 's|DESTINATION lib|DESTINATION %{_lib}|g' src/nvec_openmp/CMakeLists.txt

##Set pthread library's paths
sed -i \
 's|INSTALL(TARGETS sundials_nvecpthreads_shared DESTINATION lib)|INSTALL(TARGETS sundials_nvecpthreads_shared DESTINATION %{_libdir})|g' \
  src/nvec_pthreads/CMakeLists.txt
sed -i \
 's|INSTALL(TARGETS sundials_fnvecpthreads_shared DESTINATION lib)|INSTALL(TARGETS sundials_fnvecpthreads_shared DESTINATION %{_libdir})|g' \
  src/nvec_pthreads/CMakeLists.txt

##Set serial library's paths
sed -i \
 's|TARGETS sundials_nvecserial_shared DESTINATION lib|TARGETS sundials_nvecserial_shared DESTINATION %{_libdir}|g' \
  src/nvec_ser/CMakeLists.txt
sed -i 's|DESTINATION include/nvector|DESTINATION %{_includedir}/nvector|g' src/nvec_ser/CMakeLists.txt
sed -i \
 's|TARGETS sundials_fnvecserial_shared DESTINATION lib|TARGETS sundials_fnvecserial_shared DESTINATION %{_libdir}|g' \
  src/nvec_ser/CMakeLists.txt

## mpif77 test fails
## Hardened flags break cmake's MPI Fortran compiler test
sed -i 's|set(MPIF_PERFORM_TEST TRUE)|set(MPIF_PERFORM_TEST FALSE)|g' config/SundialsMPIF.cmake
sed -i 's|set(MPIF_FOUND FALSE)|set(MPIF_FOUND TRUE)|g' config/SundialsMPIF.cmake

mv src/arkode/README src/README-arkode
mv src/cvode/README src/README-cvode
mv src/cvodes/README src/README-cvodes
mv src/ida/README src/README-ida
mv src/idas/README src/README.idas
mv src/kinsol/README src/README-kinsol
mv src/nvec_ser/README src/README-nvec_ser
mv src/nvec_par/README src/README-nvec_par
mv src/nvec_pthreads/README src/README-nvec_pthreads
popd

%if 0%{?with_openmpi}
cp -a sundials-%{version} buildopenmpi_dir
%endif
%if 0%{?with_mpich}
cp -a sundials-%{version} buildmpich_dir
%endif

%build
pushd sundials-%{version}
mkdir -p build && cd build
%if %{with debug}
export CFLAGS=""
cmake \
 -DCMAKE_VERBOSE_MAKEFILE:BOOL=ON \
 -DCMAKE_BUILD_TYPE:STRING=Debug \
 -DCMAKE_C_FLAGS_DEBUG:STRING="-O0 -g -Wl,-z,relro -Wl,-z,now" \
 -DCMAKE_Fortran_FLAGS_DEBUG:STRING="-O0 -g -Wl,-z,relro -Wl,-z,now -lpthread -lgomp" \
%ifnarch %{power64} aarch64
 -DCMAKE_SHARED_LINKER_FLAGS_DEBUG:STRING="%{__global_ldflags} -Wl,-z,now -lklu -llapack -lblas -lgomp -lsuperlumt_d -lpthread -lm" \
%else
 -DCMAKE_SHARED_LINKER_FLAGS_DEBUG:STRING="%{__global_ldflags} -Wl,-z,now -lklu -llapack -lblas -lgomp -lpthread -lm" \
%endif
%else
%cmake \
 -DCMAKE_VERBOSE_MAKEFILE:BOOL=ON \
 -DCMAKE_BUILD_TYPE:STRING=Release \
 -DCMAKE_C_FLAGS_RELEASE:STRING="%{optflags} -Wl,-z,relro -Wl,-z,now" \
 -DCMAKE_Fortran_FLAGS_RELEASE:STRING="%{optflags} -Wl,-z,relro -Wl,-z,now -lpthread -lgomp" \
%ifnarch %{power64} aarch64
 -DCMAKE_SHARED_LINKER_FLAGS_RELEASE:STRING="%{__global_ldflags} -Wl,-z,now -lklu -llapack -lblas -lgomp -lsuperlumt_d -lpthread -lm" \
%else
 -DCMAKE_SHARED_LINKER_FLAGS_RELEASE:STRING="%{__global_ldflags} -Wl,-z,now -lklu -llapack -lblas -lgomp -lpthread -lm" \
%endif
%endif
 -DCMAKE_MODULE_LINKER_FLAGS:STRING="%{__global_ldflags} -Wl,-z,now" \
 -DCMAKE_INSTALL_PREFIX=%{_prefix} \
 -DEXAMPLES_ENABLE=ON -DEXAMPLES_INSTALL=OFF -DEXAMPLES_INSTALL_PATH:PATH=%{_datadir}/%{name}/serial_examples \
 -DCMAKE_SKIP_RPATH:BOOL=YES -DCMAKE_SKIP_INSTALL_RPATH:BOOL=YES \
 -DBUILD_SHARED_LIBS:BOOL=ON -DBUILD_STATIC_LIBS:BOOL=OFF \
 -DMPI_ENABLE:BOOL=OFF \
 -DCMAKE_Fortran_COMPILER:STRING=gfortran \
 -DFCMIX_ENABLE:BOOL=ON \
 -DF90_ENABLE:BOOL=ON \
 -DUSE_GENERIC_MATH:BOOL=ON \
 -DOPENMP_ENABLE:BOOL=ON \
 -DCXX_ENABLE:BOOL=ON \
 -DPTHREAD_ENABLE:BOOL=ON \
 -DLAPACK_ENABLE:BOOL=ON \
 -DSUNDIALS_PRECISION:STRING=double \
%ifnarch %{power64} aarch64
 -DSUPERLUMT_ENABLE:BOOL=ON \
 -DSUPERLUMT_INCLUDE_DIR:PATH=%{_includedir}/SuperLUMT \
 -DSUPERLUMT_LIBRARY_DIR:PATH=%{_libdir} \
 -DSUPERLUMT_THREAD_TYPE:STRING=OpenMP \
%endif
 -DHYPRE_ENABLE:BOOL=OFF \
 -DKLU_ENABLE=ON -DKLU_LIBRARY_DIR:PATH=%{_libdir} -DKLU_INCLUDE_DIR:PATH=%{_includedir}/suitesparse -Wno-dev ..
make V=1 %{?_smp_mflags}
cd ..
popd

#############################################################################
#######
%if 0%{?with_openmpi}
pushd buildopenmpi_dir
##Set openmpi library's paths
sed -i \
 's|TARGETS sundials_nvecparallel_shared DESTINATION lib|TARGETS sundials_nvecparallel_shared DESTINATION %{_libdir}/openmpi/lib|g' \
  src/nvec_par/CMakeLists.txt
sed -i 's|DESTINATION include/nvector|DESTINATION %{_includedir}/openmpi-%{_arch}/nvector|g' src/nvec_par/CMakeLists.txt
sed -i \
 's|TARGETS sundials_fnvecparallel_shared DESTINATION lib|TARGETS sundials_fnvecparallel_shared DESTINATION %{_libdir}/openmpi/lib|g' \
  src/nvec_par/CMakeLists.txt
sed -i \
 's|TARGETS sundials_nvecparhyp_shared DESTINATION lib|TARGETS sundials_nvecparhyp_shared DESTINATION %{_libdir}/openmpi/lib|g' \
  src/nvec_parhyp/CMakeLists.txt

mkdir -p build && cd build
%{_openmpi_load}
export CC=mpicc
export CXX=mpicxx
export FC=mpif77
%if %{with debug}
export CFLAGS=""
cmake \
 -DCMAKE_VERBOSE_MAKEFILE:BOOL=ON \
 -DCMAKE_BUILD_TYPE:STRING=Debug \
 -DCMAKE_C_FLAGS_DEBUG:STRING="-O0 -g -Wl,-z,relro -Wl,-z,now" \
 -DCMAKE_Fortran_FLAGS_DEBUG:STRING="-O0 -g -Wl,-z,relro -Wl,-z,now -lm -lpthread -lgomp" \
 -DCMAKE_SHARED_LINKER_FLAGS_DEBUG:STRING="%{__global_ldflags} -Wl,-z,now -lm -lpthread -lgomp -lklu -L%{_libdir}/openmpi/lib -lHYPRE" \
%else
%cmake \
 -DCMAKE_VERBOSE_MAKEFILE:BOOL=ON \
 -DCMAKE_BUILD_TYPE:STRING=Release \
 -DCMAKE_C_FLAGS_RELEASE:STRING="%{optflags} -Wl,-z,relro -Wl,-z,now" \
 -DCMAKE_Fortran_FLAGS_RELEASE:STRING="%{optflags} -Wl,-z,relro -Wl,-z,now -lm -lpthread -lgomp" \
 -DCMAKE_SHARED_LINKER_FLAGS_RELEASE:STRING="%{__global_ldflags} -Wl,-z,now -lm -lpthread -lgomp -lklu -L%{_libdir}/openmpi/lib -lHYPRE" \
%endif
 -DCMAKE_INSTALL_PREFIX=%{_prefix} \
 -DEXAMPLES_ENABLE=ON -DEXAMPLES_INSTALL=OFF -DEXAMPLES_INSTALL_PATH:PATH=%{_datadir}/%{name}/openmpi_examples \
 -DBUILD_SHARED_LIBS:BOOL=ON -DBUILD_STATIC_LIBS:BOOL=OFF \
 -DCMAKE_SKIP_RPATH:BOOL=YES -DCMAKE_SKIP_INSTALL_RPATH:BOOL=YES \
 -DMPI_ENABLE:BOOL=ON \
 -DMPI_MPICC:STRING=%{_libdir}/openmpi/bin/mpicc \
 -DMPI_RUN_COMMAND=mpirun \
 -DMPI_MPIF77:STRING=%{_libdir}/openmpi/bin/mpif77 \
 -DFCMIX_ENABLE:BOOL=ON \
 -DF90_ENABLE:BOOL=OFF \
 -DUSE_GENERIC_MATH:BOOL=ON \
 -DOPENMP_ENABLE:BOOL=ON \
 -DCXX_ENABLE:BOOL=ON \
 -DCMAKE_Fortran_COMPILER:STRING=%{_libdir}/openmpi/bin/mpif77 \
 -DPTHREAD_ENABLE:BOOL=ON \
 -DLAPACK_ENABLE:BOOL=ON \
 -DSUPERLUMT_ENABLE:BOOL=OFF \
 -DHYPRE_ENABLE:BOOL=ON \
 -DHYPRE_INCLUDE_DIR:PATH=%{_includedir}/openmpi-%{_arch}/hypre \
 -DHYPRE_LIBRARY_DIR:PATH=%{_libdir}/openmpi/lib \
 -DKLU_ENABLE=ON -DKLU_LIBRARY_DIR:PATH=%{_libdir} -DKLU_INCLUDE_DIR:PATH=%{_includedir}/suitesparse -Wno-dev ..
make V=1 %{?_smp_mflags}
%{_openmpi_unload}
cd ..
popd
%endif
######
#############################################################################
######
%if 0%{?with_mpich}
pushd buildmpich_dir
##Set mpich library's paths
sed -i \
 's|TARGETS sundials_nvecparallel_shared DESTINATION lib|TARGETS sundials_nvecparallel_shared DESTINATION %{_libdir}/mpich/lib|g' \
  src/nvec_par/CMakeLists.txt
sed -i 's|DESTINATION include/nvector|DESTINATION %{_includedir}/mpich-%{_arch}/nvector|g' src/nvec_par/CMakeLists.txt
sed -i \
 's|TARGETS sundials_fnvecparallel_shared DESTINATION lib|TARGETS sundials_fnvecparallel_shared DESTINATION %{_libdir}/mpich/lib|g' \
  src/nvec_par/CMakeLists.txt
sed -i \
 's|TARGETS sundials_nvecparhyp_shared DESTINATION lib|TARGETS sundials_nvecparhyp_shared DESTINATION %{_libdir}/mpich/lib|g' \
  src/nvec_parhyp/CMakeLists.txt

mkdir -p build && cd build
%{_mpich_load}
%if 0%{?rhel}
export CC=mpicc
export CXX=mpicxx
export F77=mpif77
export FC=mpif90
%endif
%if 0%{?fedora}
export CC=mpicc
export CXX=mpicxx
export F77=mpifort
export FC=mpifort
%endif
%if %{with debug}
export CFLAGS=""
cmake \
 -DCMAKE_VERBOSE_MAKEFILE:BOOL=ON \
 -DCMAKE_BUILD_TYPE:STRING=Debug \
 -DCMAKE_C_FLAGS_DEBUG:STRING="-O0 -g -Wl,-z,relro -Wl,-z,now" \
 -DCMAKE_Fortran_FLAGS_DEBUG:STRING="-O0 -g -Wl,-z,relro -Wl,-z,now -lm -lpthread -lgomp" \
 -DCMAKE_SHARED_LINKER_FLAGS_DEBUG:STRING="%{__global_ldflags} -Wl,-z,now -lm -lpthread -lgomp -lklu -L%{_libdir}/mpich/lib -lHYPRE" \
%else
%cmake \
 -DCMAKE_VERBOSE_MAKEFILE:BOOL=ON \
 -DCMAKE_BUILD_TYPE:STRING=Release \
 -DCMAKE_C_FLAGS_RELEASE:STRING="%{optflags} -Wl,-z,relro -Wl,-z,now" \
 -DCMAKE_Fortran_FLAGS_RELEASE:STRING="%{optflags} -Wl,-z,relro -Wl,-z,now -lm -lpthread -lgomp" \
 -DCMAKE_SHARED_LINKER_FLAGS_RELEASE:STRING="%{__global_ldflags} -Wl,-z,now -lm -lpthread -lgomp -lklu -L%{_libdir}/mpich/lib -lHYPRE" \
%endif
 -DCMAKE_INSTALL_PREFIX=%{_prefix} \
 -DEXAMPLES_ENABLE=ON -DEXAMPLES_INSTALL=OFF -DEXAMPLES_INSTALL_PATH:PATH=%{_datadir}/%{name}/mpich_examples \
 -DBUILD_SHARED_LIBS:BOOL=ON -DBUILD_STATIC_LIBS:BOOL=OFF \
 -DCMAKE_SKIP_RPATH:BOOL=YES -DCMAKE_SKIP_INSTALL_RPATH:BOOL=YES \
 -DMPI_ENABLE:BOOL=ON \
 -DMPI_MPICC:STRING=%{_libdir}/mpich/bin/mpicc \
 -DMPI_RUN_COMMAND=mpirun \
%if 0%{?fedora}
 -DMPI_MPIF77:STRING=%{_libdir}/mpich/bin/mpifort \
 -DMPI_MPIF90:STRING=%{_libdir}/mpich/bin/mpifort \
%else
 -DMPI_MPIF77:STRING=%{_libdir}/mpich/bin/mpif77 \
 -DMPI_MPIF90:STRING=%{_libdir}/mpich/bin/mpif90 \
%endif
 -DFCMIX_ENABLE:BOOL=ON \
 -DF90_ENABLE:BOOL=ON \
 -DUSE_GENERIC_MATH:BOOL=ON \
 -DOPENMP_ENABLE:BOOL=ON \
 -DCXX_ENABLE:BOOL=ON \
 -DCMAKE_Fortran_COMPILER:STRING=%{_libdir}/mpich/bin/mpif77 \
 -DPTHREAD_ENABLE:BOOL=ON \
 -DLAPACK_ENABLE:BOOL=ON \
 -DSUPERLUMT_ENABLE:BOOL=OFF \
 -DHYPRE_ENABLE:BOOL=ON \
 -DHYPRE_INCLUDE_DIR:PATH=%{_includedir}/mpich-%{_arch}/hypre \
 -DHYPRE_LIBRARY_DIR:PATH=%{_libdir}/mpich/lib \
 -DKLU_ENABLE=ON -DKLU_LIBRARY_DIR:PATH=%{_libdir} -DKLU_INCLUDE_DIR:PATH=%{_includedir}/suitesparse -Wno-dev ..
make V=1 %{?_smp_mflags}
%{_mpich_unload}
cd ..
popd
%endif
######
#############################################################################

%install
%if 0%{?with_openmpi}
%{_openmpi_load}
make install DESTDIR=%{buildroot} -C buildopenmpi_dir/build
%{_openmpi_unload}
%endif

%if 0%{?with_mpich}
%{_mpich_load}
make install DESTDIR=%{buildroot} -C buildmpich_dir/build
%{_mpich_unload}
%endif

make install DESTDIR=%{buildroot} -C sundials-%{version}/build

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post threads -p /sbin/ldconfig
%postun threads -p /sbin/ldconfig

%post fortran -p /sbin/ldconfig
%postun fortran -p /sbin/ldconfig

%check

%if 0%{?with_parcheck}
%if 0%{?with_openmpi}
%{_openmpi_load}
export LD_LIBRARY_PATH=%{buildroot}%{_libdir}/openmpi/lib:%{buildroot}%{_libdir}
##arkode
buildopenmpi_dir/build/examples/arkode/CXX_parallel/ark_heat2D
buildopenmpi_dir/build/examples/arkode/F77_parallel/fark_diag_kry_bbd_p

##cvode
buildopenmpi_dir/build/examples/cvode/fcmix_parallel/fcvDiag_kry_bbd_p
buildopenmpi_dir/build/examples/cvode/parallel/cvAdvDiff_diag_p

##cvodes
mpirun -np 2 buildopenmpi_dir/build/examples/cvodes/parallel/cvsAdvDiff_ASAp_non_p

#ida
mpirun -np 4 buildopenmpi_dir/build/examples/ida/fcmix_parallel/fidaHeat2D_kry_bbd_p
mpirun -np 4 buildopenmpi_dir/build/examples/ida/parallel/idaFoodWeb_kry_bbd_p

#idas
mpirun -np 4 buildopenmpi_dir/build/examples/idas/parallel/idasBruss_ASAp_kry_bbd_p

#kinsol
mpirun -np 4 buildopenmpi_dir/build/examples/kinsol/fcmix_parallel/fkinDiagon_kry_p
mpirun -np 4 buildopenmpi_dir/build/examples/kinsol/parallel/kinFoodWeb_kry_bbd_p

#nvector
mpirun buildopenmpi_dir/build/examples/nvector/parallel/test_nvector_mpi
%{_openmpi_unload}
%endif ##if openmpi

%if 0%{?with_mpich}
## Tests not perfomred due to 'gethostname' failure on koji
%endif ##if openmpi
%endif ## if with_parcheck

%if 0%{?with_sercheck}
pushd sundials-%{version}/build/examples
export LD_LIBRARY_PATH=%{buildroot}%{_libdir}
##arkode
cd arkode/C_serial
./ark_analytic
./ark_analytic_nonlin
./ark_brusselator
./ark_brusselator1D
./ark_brusselator_fp
./ark_heat1D
./ark_heat1D_adapt
./ark_KrylovDemo_prec
./ark_robertson
./ark_robertson_root

cd ../F77_serial
./fark_diurnal_kry_bp
%ifnarch s390 s390x ppc64 ppc64le
./fark_roberts_dnsL
%endif
cd ../..
##cvode
cd cvode/fcmix_serial
%ifnarch s390 s390x ppc64 ppc64le
./fcvAdvDiff_bnd
./fcvDiurnal_kry
./fcvDiurnal_kry_bp
./fcvRoberts_dns
./fcvRoberts_dnsL
%endif

cd ../serial
./cvAdvDiff_bnd
./cvAdvDiff_bndL
./cvDirectDemo_ls
./cvDiurnal_kry
./cvDiurnal_kry_bp
./cvKrylovDemo_ls
./cvKrylovDemo_prec
./cvRoberts_dns
./cvRoberts_dnsL
./cvRoberts_dns_uw
cd ../..
##cvodes
cd cvodes/serial
./cvsAdvDiff_ASAi_bnd
./cvsAdvDiff_bnd
./cvsAdvDiff_bndL
./cvsAdvDiff_FSA_non
./cvsDirectDemo_ls
./cvsDiurnal_FSA_kry
./cvsDiurnal_kry
./cvsDiurnal_kry_bp
./cvsFoodWeb_ASAi_kry
./cvsFoodWeb_ASAp_kry
./cvsHessian_ASA_FSA
./cvsKrylovDemo_ls
./cvsKrylovDemo_prec
./cvsRoberts_ASAi_dns
./cvsRoberts_dns
./cvsRoberts_dnsL
./cvsRoberts_dns_uw
./cvsRoberts_FSA_dns
cd ../..
##ida
cd ida/fcmix_pthreads
%ifnarch s390 s390x ppc64 ppc64le
./fidaRoberts_dns_pthreads
cd ../fcmix_serial
./fidaRoberts_dns
%endif
cd ../serial
./idaFoodWeb_bnd
./idaHeat2D_bnd
./idaHeat2D_kry
./idaKrylovDemo_ls
./idaRoberts_dns
./idaSlCrank_dns
cd ../..
##idas
cd idas/serial
./idasAkzoNob_ASAi_dns
./idasAkzoNob_dns
./idasFoodWeb_bnd
./idasHeat2D_bnd
./idasHeat2D_kry
./idasHessian_ASA_FSA
./idasKrylovDemo_ls
./idasRoberts_ASAi_dns
./idasRoberts_dns
./idasRoberts_FSA_dns
./idasSlCrank_dns
./idasSlCrank_FSA_dns
cd ../..
##kinsol
cd kinsol/fcmix_serial
%ifnarch s390 s390x ppc64 ppc64le
./fkinDiagon_kry
%endif
cd ../serial
./kinFerTron_dns
./kinFoodWeb_kry
##http://sundials.2283335.n4.nabble.com/kinKrylovDemo-ls-failed-on-aarch64-td4653553.html
%ifnarch aarch64 s390 s390x ppc64 ppc64le
./kinKrylovDemo_ls
%endif
./kinLaplace_bnd
./kinLaplace_picard_bnd
./kinRoberts_fp
./kinRoboKin_dns
cd ../..
##nvector
cd nvector/pthreads
./test_nvector_pthreads 5000 4 1
cd ../serial
./test_nvector_serial 5000 4 1
popd
%endif ##if with_sercheck

%files
%{!?_licensedir:%global license %doc}
%license sundials-%{version}/LICENSE
%doc sundials-%{version}/README sundials-%{version}/src/README-*
%{_libdir}/libsundials_nvecserial.so.*
%{_libdir}/libsundials_cvode.so.*
%{_libdir}/libsundials_cvodes.so.*
%{_libdir}/libsundials_arkode.so.* 
%{_libdir}/libsundials_ida.so.* 
%{_libdir}/libsundials_idas.so.* 
%{_libdir}/libsundials_kinsol.so.*

%files doc
%{!?_licensedir:%global license %doc}
%license sundials-%{version}/LICENSE
%doc sundials-%{version}/README
%doc sundials-%{version}/doc/cvode/cv_examples.pdf
%doc sundials-%{version}/doc/cvode/cv_guide.pdf
%doc sundials-%{version}/doc/kinsol/kin_examples.pdf
%doc sundials-%{version}/doc/kinsol/kin_guide.pdf
%doc sundials-%{version}/doc/cvodes/cvs_examples.pdf
%doc sundials-%{version}/doc/cvodes/cvs_guide.pdf
%doc sundials-%{version}/doc/ida/ida_examples.pdf
%doc sundials-%{version}/doc/ida/ida_guide.pdf
%doc sundials-%{version}/doc/arkode/*

%files devel
%{_libdir}/libsundials_nvecserial.so
%{_libdir}/libsundials_cvode.so
%{_libdir}/libsundials_cvodes.so
%{_libdir}/libsundials_arkode.so 
%{_libdir}/libsundials_ida.so 
%{_libdir}/libsundials_idas.so 
%{_libdir}/libsundials_kinsol.so
%{_includedir}/sundials/
%{_includedir}/cvode/
%{_includedir}/cvodes/
%{_includedir}/arkode/
%{_includedir}/ida/
%{_includedir}/idas/
%{_includedir}/kinsol/
%{_includedir}/nvector/

%files openmp
%{!?_licensedir:%global license %doc}
%license sundials-%{version}/LICENSE
%doc sundials-%{version}/README sundials-%{version}/src/README-*
%{_libdir}/libsundials_nvecopenmp.so.*

%files openmp-devel
%{_libdir}/libsundials_nvecopenmp.so

%files fortran-openmp
%{!?_licensedir:%global license %doc}
%license sundials-%{version}/LICENSE
%doc sundials-%{version}/README sundials-%{version}/src/README-*
%{_libdir}/libsundials_fnvecopenmp.so.*

%files fortran-openmp-devel
%{_libdir}/libsundials_fnvecopenmp.so

%if 0%{?with_openmpi}
%files openmpi
%license sundials-%{version}/LICENSE
%doc sundials-%{version}/README sundials-%{version}/src/README-nvec_par
%{_libdir}/openmpi/lib/libsundials_nvecparallel.so.*
%{_libdir}/openmpi/lib/libsundials_nvecparhyp.so.*

%files openmpi-devel
%{_includedir}/openmpi-%{_arch}/nvector/nvector_parallel.h
%{_libdir}/openmpi/lib/libsundials_nvecparallel.so
%{_libdir}/openmpi/lib/libsundials_nvecparhyp.so

%files fortran-openmpi
%{!?_licensedir:%global license %doc}
%license sundials-%{version}/LICENSE
%doc sundials-%{version}/README sundials-%{version}/src/README-nvec_par
%{_libdir}/openmpi/lib/libsundials_fnvecparallel.so.*

%files fortran-openmpi-devel
%{_includedir}/openmpi-%{_arch}/nvector/nvector_parallel.h
%{_libdir}/openmpi/lib/libsundials_fnvecparallel.so
%endif

%if 0%{?with_mpich}
%files mpich
%{!?_licensedir:%global license %doc}
%license sundials-%{version}/LICENSE
%doc sundials-%{version}/README sundials-%{version}/src/README-nvec_par
%{_libdir}/mpich/lib/libsundials_nvecparallel.so.*
%{_libdir}/mpich/lib/libsundials_nvecparhyp.so.*

%files mpich-devel
%{_includedir}/mpich-%{_arch}/nvector/nvector_parallel.h
%{_libdir}/mpich/lib/libsundials_nvecparallel.so
%{_libdir}/mpich/lib/libsundials_nvecparhyp.so

%files fortran-mpich
%{!?_licensedir:%global license %doc}
%license sundials-%{version}/LICENSE
%doc sundials-%{version}/README sundials-%{version}/src/README-nvec_par
%{_libdir}/mpich/lib/libsundials_fnvecparallel.so.*

%files fortran-mpich-devel
%{_includedir}/mpich-%{_arch}/nvector/nvector_parallel.h
%{_libdir}/mpich/lib/libsundials_fnvecparallel.so
%endif

%files fortran
%{!?_licensedir:%global license %doc}
%license sundials-%{version}/LICENSE
%doc sundials-%{version}/README
%{_libdir}/libsundials_fnvecserial.so.*

%files fortran-devel
%{_includedir}/sundials/sundials_fnvector.h
%{_libdir}/libsundials_fnvecserial.so
%{_libdir}/libsundials_*.a

%files threads
%{!?_licensedir:%global license %doc}
%license sundials-%{version}/LICENSE
%doc sundials-%{version}/README sundials-%{version}/src/README-nvec_pthreads
%{_libdir}/libsundials_nvecpthreads.so.*
%{_libdir}/libsundials_fnvecpthreads.so.*

%files threads-devel
%{_libdir}/libsundials_fnvecpthreads.so
%{_libdir}/libsundials_nvecpthreads.so
%{_includedir}/nvector/nvector_pthreads.h

%changelog
* Fri Mar 03 2017 Antonio Trande <sagitterATfedoraproject.org> - 2.7.0-9
- Add KLU support

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Nov 01 2016 Antonio Trande <sagitterATfedoraproject.org> - 2.7.0-7
- New architectures

* Mon Oct 24 2016 Antonio Trande <sagitterATfedoraproject.org> - 2.7.0-6
- Fix builds of MPICH libraries

* Fri Oct 21 2016 Orion Poplawski <orion@cora.nwra.com> - 2.7.0-5
- Rebuild for openmpi 2.0

* Mon Oct 17 2016 Antonio Trande <sagitterATfedoraproject.org> - 2.7.0-4
- Set debug builds

* Thu Oct 06 2016 Antonio Trande <sagitterATfedoraproject.org> - 2.7.0-3
- SuperLUMT support condizionalized
- Removed pkgconfig files

* Tue Oct 04 2016 Antonio Trande <sagitterATfedoraproject.org> - 2.7.0-2
- Enabled SuperLUMT and HYPRE support

* Thu Sep 29 2016 Antonio Trande <sagitterATfedoraproject.org> - 2.7.0-1
- Update to 2.7.0

* Sun Mar 27 2016 Antonio Trande <sagitterATfedoraproject.org> - 2.6.2-19
- Typos fixed

* Sat Mar 26 2016 Antonio Trande <sagitterATfedoraproject.org> - 2.6.2-18
- Enabled OpenMP support

* Sun Mar 20 2016 Mukundan Ragavan <nonamedotc@fedoraproject.org> - 2.6.2-17
- Add lapack-devel requires to -devel package

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.2-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jan 25 2016 Antonio Trande <sagitterATfedoraproject.org> - 2.6.2-15
- Fixed pthread flags

* Sun Jan 17 2016 Antonio Trande <sagitterATfedoraproject.org> - 2.6.2-14
- Fix OpenMPI compilers
- MPICH libraries enabled
- Cmake's MPI Fortran compiler test disabled
- Included pkgconfig files for MPICH libraries

* Thu Dec 31 2015 Antonio Trande <sagitterATfedoraproject.org> - 2.6.2-13
- Exclude pkgconfig for OpenMPI libs on s390

* Sat Dec 26 2015 Antonio Trande <sagitterATfedoraproject.org> - 2.6.2-12
- Fixed pkgconfig files
- Added pkgconfig files for OpenMPI libraries
- All Fortran libraries moved to default library paths

* Thu Nov 12 2015 Antonio Trande <sagitterATfedoraproject.org> - 2.6.2-11
- Fixes for EPEL7
- Set mpif77 only for OpenMPI < 1.17 (EPEL7)
- Set mpifort for OpenMPI > 1.17 (Fedora)
- Set LDFLAGS for EPEL7

* Wed Nov 11 2015 Antonio Trande <sagitterATfedoraproject.org> - 2.6.2-10
- OpenMPI Fortran lib tests not compiled on F<23

* Wed Nov 11 2015 Antonio Trande <sagitterATfedoraproject.org> - 2.6.2-9
- Hardened builds on <F23
- openmpi tests still crash/hang on i686 (Fedora 21)
- Rebuilt on Fedora 21

* Thu Oct 15 2015 Antonio Trande <sagitterATfedoraproject.org> - 2.6.2-8
- Rebuilt for cmake 3.4.0

* Sun Sep 20 2015 Antonio Trande <sagitterATfedoraproject.org> - 2.6.2-7
- Performed even tests of the parallel-libraries on ix86 arches

* Tue Sep 15 2015 Orion Poplawski <orion@cora.nwra.com> - 2.6.2-6
- Rebuild for openmpi 1.10.0

* Fri Aug 28 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.6.2-5
- Rebuild for rpm-mpi-hooks-3-2

* Sat Aug 15 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.6.2-4
- Rebuild for MPI provides

* Mon Aug 10 2015 Sandro Mani <manisandro@gmail.com> - 2.6.2-3
- Rebuild for RPM MPI Requires Provides Change

* Tue Aug 04 2015 Antonio Trande <sagitterATfedoraproject.org> - 2.6.2-2
- Added rsh as BR for EPEL7

* Tue Aug 04 2015 Antonio Trande <sagitterATfedoraproject.org> - 2.6.2-1
- Update to 2.6.2

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 03 2015 Antonio Trande <sagitterATfedoraproject.org> - 2.6.1-8
- Excluded some tests for s390 s390x
- openmpi tests disabled on ix86 %%{arm} (BZ#1201901)

* Sat May 09 2015 Antonio Trande <sagitterATfedoraproject.org> - 2.6.1-7
- Excluded kinKrylovDemo_ls test for aarch64

* Fri Apr 17 2015 Antonio Trande <sagitterATfedoraproject.org> - 2.6.1-6
- Performed parallel/serial tests

* Thu Apr 16 2015 Antonio Trande <sagitterATfedoraproject.org> - 2.6.1-5
- Fixed ldconfig scriptlets

* Sat Apr 04 2015 Antonio Trande <sagitterATfedoraproject.org> - 2.6.1-4
- Packaged static Fortran libraries

* Fri Apr 03 2015 Antonio Trande <sagitterATfedoraproject.org> - 2.6.1-3
- Packaged pkg-config files of Serial libraries

* Wed Apr 01 2015 Antonio Trande <sagitterATfedoraproject.org> - 2.6.1-2
- Built OpenMPI, libraries with threading support, Fortran libraries

* Mon Mar 30 2015 Mukundan Ragavan <nonamedotc@fedoraproject.org> - 2.6.1-1
- Update to version 2.6.1 
- Minor bugfixes

* Sun Mar 29 2015 Mukundan Ragavan <nonamedotc@fedoraproject.org> - 2.6.0-2
- Ensure the shared libraries are linked correctly

* Sun Mar 22 2015 Mukundan Ragavan <nonamedotc@fedoraproject.org> - 2.6.0-1
- Update to 2.6.0
- Drop patches that are not needed anymore

* Wed Dec 03 2014 Mukundan Ragavan <nonamedotc@fedoraproject.org> - 2.5.0-7
- Initial build for EPEL-7

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

* Sat Jan 26 2013 Rahul Sundaram <sundaram@fedoraproject.org> - 2.5.0-1
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

