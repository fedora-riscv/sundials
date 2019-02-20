## Debug builds?
%bcond_with debug
#

%if 0%{?rhel} && 0%{?rhel} < 7
%{!?__global_ldflags: %global __global_ldflags -Wl,-z,relro}
%endif

%if 0%{?fedora}
%global with_mpich 1
%global with_openmpi 1
%endif

# No MPICH support on these arches
%if 0%{?rhel} && 0%{?rhel} < 7
%ifarch %{power64}
%global with_openmpi 1
%global with_mpich 0
%endif
%endif
%if 0%{?rhel} && 0%{?rhel} < 7
%ifnarch %{power64}
%global with_openmpi 1
%global with_mpich 1
%endif
%endif
%if 0%{?rhel} && 0%{?rhel} >= 7
%global with_openmpi 1
%global with_mpich 1
%endif

%global with_hypre 1

## PETSc ##
%if 0%{?fedora} && 0%{?fedora} < 29
## Exclude MPI builds on s390x
%ifarch s390x
%global with_petsc 0
%endif
%ifnarch s390x
%global with_petsc 1
%endif
%endif

%if 0%{?fedora} && 0%{?fedora} >= 29
%global with_petsc 1
%endif
%if 0%{?rhel} && 0%{?rhel} >= 7
%global with_petsc 1
%endif
###########

# Disable tests of MPI libraries for
# "not enough slots available" errors
%if 0%{?fedora} && 0%{?fedora} < 30
%global with_openmpicheck 1
%global with_mpichcheck 1
%global with_sercheck 1
%endif

Summary:    Suite of nonlinear solvers
Name:       sundials
Version:    3.2.1
Release:    4%{?dist}
# SUNDIALS is licensed under BSD with some additional (but unrestrictive) clauses.
# Check the file 'LICENSE' for details.
License:    BSD
URL:        http://www.llnl.gov/casc/sundials/
Source0:    https://computation.llnl.gov/projects/sundials/download/sundials-%{version}.tar.gz

# This patch rename superLUMT library
Patch0:     %{name}-3.1.1-set_superlumt_name.patch

# This patch rename superLUMT64 library
Patch1:     %{name}-3.1.1-set_superlumt64_name.patch

BuildRequires: gcc-gfortran
# Tests work under python2 only
BuildRequires: python2-devel
BuildRequires: gcc, gcc-c++
BuildRequires: suitesparse-devel
%if 0%{?rhel}
BuildRequires: epel-rpm-macros
%endif
BuildRequires: cmake3
BuildRequires: openblas-devel, openblas-srpm-macros
%ifarch s390x x86_64
BuildRequires: SuperLUMT64-devel
%endif
%ifarch %{arm} %{ix86}
BuildRequires: SuperLUMT-devel
%endif
%if 0%{?rhel}
BuildRequires: rsh
%endif
Requires: gcc-gfortran%{?_isa}
Obsoletes: %{name}-samples%{?_isa} < 3.1.1-2

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
Requires:   %{name}%{?_isa} = %{version}-%{release}
%description devel
SUNDIALS is a SUite of Non-linear DIfferential/ALgebraic equation Solvers
for use in writing mathematical software.
This package contains the developer files (.so file, header files).
#############################################################################
#########
%if 0%{?with_openmpi}
%package openmpi
Summary:    Suite of nonlinear solvers
BuildRequires: openmpi-devel
%if 0%{?rhel} || 0%{?fedora} > 28
BuildRequires: hypre-openmpi-devel
%else
%ifnarch s390x
BuildRequires: hypre-openmpi-devel
%endif
%endif
%if 0%{?with_petsc}
BuildRequires: petsc-openmpi-devel
%endif

Requires: openmpi%{?_isa}
Requires: gcc-gfortran%{?_isa}
Obsoletes: %{name}-openmpi-samples%{?_isa} < 3.1.1-2

%description openmpi
SUNDIALS is a SUite of Non-linear DIfferential/ALgebraic equation Solvers
for use in writing mathematical software.
This package contains the Sundials Fortran parallel OpenMPI libraries.

%package openmpi-devel
Summary:    Suite of nonlinear solvers
Requires:   %{name}-openmpi%{?_isa} = %{version}-%{release}
%description openmpi-devel
SUNDIALS is a SUite of Non-linear DIfferential/ALgebraic equation Solvers
for use in writing mathematical software.
This package contains the Sundials parallel OpenMPI devel libraries and
header files.
%endif
######
###############################################################################
######
%if 0%{?with_mpich}
%package mpich
Summary:    Suite of nonlinear solvers
BuildRequires: mpich-devel
%if 0%{?rhel} || 0%{?fedora} > 28
BuildRequires: hypre-mpich-devel
%else
%ifnarch s390x
BuildRequires: hypre-mpich-devel
%endif
%endif
%if 0%{?with_petsc}
BuildRequires: petsc-mpich-devel
%endif
Requires: mpich%{?_isa}
Requires: gcc-gfortran%{?_isa}
Obsoletes: %{name}-mpich-samples%{?_isa} < 3.1.1-2

%description mpich
SUNDIALS is a SUite of Non-linear DIfferential/ALgebraic equation Solvers
for use in writing mathematical software.
This package contains the Sundials parallel MPICH libraries.

%package mpich-devel
Summary:    Suite of nonlinear solvers
Requires:   %{name}-mpich%{?_isa} = %{version}-%{release}
%description mpich-devel
SUNDIALS is a SUite of Non-linear DIfferential/ALgebraic equation Solvers
for use in writing mathematical software.
This package contains the Sundials parallel MPICH devel libraries and
header files.
%endif
######
#############################################################################

%package doc
Summary:    Suite of nonlinear solvers (documentation)
BuildArch: noarch
%description doc
SUNDIALS is a SUite of Non-linear DIfferential/ALgebraic equation Solvers
for use in writing mathematical software.
This package contains the documentation files.

%prep
%setup -qc

pushd sundials-%{version}

%ifarch s390x x86_64
%patch1 -p0
%endif
%ifarch %{arm} %{ix86}
%patch0 -p0
%endif

##Set destination library's paths
sed -i 's| SOVERSION | %{version} |g' src/sunlinsol_*/CMakeLists.txt
sed -i 's| SOVERSION | %{version} |g' src/sunmat_*/CMakeLists.txt

##Set serial library's paths
sed -i 's|DESTINATION include/nvector|DESTINATION %{_includedir}/nvector|g' src/nvec_ser/CMakeLists.txt

mv src/arkode/README src/README-arkode
mv src/cvode/README src/README-cvode
mv src/cvodes/README src/README-cvodes
mv src/ida/README src/README-ida
mv src/idas/README src/README.idas
mv src/kinsol/README src/README-kinsol
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

export LIBBLASLINK=-lopenblas
export LIBBLAS=libopenblas
export INCBLAS=-I%{_includedir}/openblas

%ifarch s390x x86_64
export LIBSUPERLUMTLINK=-lsuperlumt64_d
%endif
%ifarch %{arm} %{ix86}
export LIBSUPERLUMTLINK=-lsuperlumt_d
%endif
%ifnarch s390x x86_64 %{arm} %{ix86}
export LIBSUPERLUMTLINK=
%endif

%if %{with debug}
%undefine _hardened_build
export CFLAGS=""
%if 0%{?rhel}
%global cmake cmake3
%endif
%cmake \
 -DCMAKE_VERBOSE_MAKEFILE:BOOL=ON \
 -DCMAKE_BUILD_TYPE:STRING=Debug \
 -DCMAKE_C_FLAGS_DEBUG:STRING="-O0 -g -Wl,-z,relro -Wl,-z,now -Wl,--as-needed -I$INCBLAS" \
 -DCMAKE_Fortran_FLAGS_DEBUG:STRING="-O0 -g -Wl,-z,relro -Wl,-z,now -Wl,--as-needed -I$INCBLAS" \
 -DCMAKE_SHARED_LINKER_FLAGS_DEBUG:STRING="%{__global_ldflags} -lklu $LIBBLASLINK $LIBSUPERLUMTLINK" \
%else
%cmake3 \
%if %{?__isa_bits:%{__isa_bits}}%{!?__isa_bits:32} == 64
 -DSUNDIALS_INDEX_SIZE:STRING=64 \
%else
 -DSUNDIALS_INDEX_SIZE:STRING=32 \
%endif
 -DCMAKE_VERBOSE_MAKEFILE:BOOL=ON \
 -DCMAKE_BUILD_TYPE:STRING=Release \
 -DCMAKE_C_FLAGS_RELEASE:STRING="%{optflags} -I$INCBLAS" \
 -DCMAKE_Fortran_FLAGS_RELEASE:STRING="%{optflags} -I$INCBLAS" \
 -DCMAKE_SHARED_LINKER_FLAGS_RELEASE:STRING="%{__global_ldflags} -lklu $LIBBLASLINK $LIBSUPERLUMTLINK" \
%endif
 -DLAPACK_ENABLE:BOOL=OFF \
 -DBLAS_ENABLE:BOOL=ON \
 -DBLAS_LIBRARIES:STRING=%{_libdir}/$LIBBLAS.so \
 -DCMAKE_MODULE_LINKER_FLAGS:STRING="%{__global_ldflags}" \
 -DCMAKE_INSTALL_PREFIX:PATH=%{_prefix} -DCMAKE_INSTALL_LIBDIR:PATH=%{_lib} \
 -DPYTHON_EXECUTABLE:FILEPATH=%{__python2} \
 -DEXAMPLES_ENABLE_CXX:BOOL=ON -DEXAMPLES_ENABLE_C:BOOL=ON -DEXAMPLES_ENABLE_F77:BOOL=ON \
 -DCMAKE_SKIP_RPATH:BOOL=YES -DCMAKE_SKIP_INSTALL_RPATH:BOOL=YES \
 -DBUILD_SHARED_LIBS:BOOL=ON -DBUILD_STATIC_LIBS:BOOL=OFF \
 -DMPI_ENABLE:BOOL=OFF \
 -DCMAKE_Fortran_COMPILER:STRING=gfortran \
 -DFCMIX_ENABLE:BOOL=ON \
 -DUSE_GENERIC_MATH:BOOL=ON \
 -DOPENMP_ENABLE:BOOL=ON \
 -DPTHREAD_ENABLE:BOOL=ON \
 -DSUNDIALS_PRECISION:STRING=double \
%ifnarch %{power64} aarch64
 -DSUPERLUMT_ENABLE:BOOL=ON \
 -DSUPERLUMT_INCLUDE_DIR:PATH=%{_includedir}/SuperLUMT \
 -DSUPERLUMT_LIBRARY_DIR:PATH=%{_libdir} \
 -DSUPERLUMT_THREAD_TYPE:STRING=OpenMP \
%endif
 -DHYPRE_ENABLE:BOOL=OFF \
 -DKLU_ENABLE=ON -DKLU_LIBRARY_DIR:PATH=%{_libdir} -DKLU_INCLUDE_DIR:PATH=%{_includedir}/suitesparse \
 -DEXAMPLES_INSTALL:BOOL=OFF -Wno-dev ..

%make_build V=1
cd ..
popd

#############################################################################
#######
%if 0%{?with_openmpi}
pushd buildopenmpi_dir
##Set openmpi library's paths
sed -i 's|DESTINATION include/nvector|DESTINATION %{_includedir}/openmpi-%{_arch}/nvector|g' src/nvec_par/CMakeLists.txt
sed -i 's|CMAKE_INSTALL_LIBDIR}|CMAKE_INSTALL_LIBDIR}/openmpi/lib|g' src/nvec_par/CMakeLists.txt
sed -i 's|DESTINATION include/nvector|DESTINATION %{_includedir}/openmpi-%{_arch}/nvector|g' src/nvec_parhyp/CMakeLists.txt
sed -i 's|CMAKE_INSTALL_LIBDIR}|CMAKE_INSTALL_LIBDIR}/openmpi/lib|g' src/nvec_parhyp/CMakeLists.txt
%if 0%{?with_petsc}
sed -i 's|DESTINATION include/nvector|DESTINATION %{_includedir}/openmpi-%{_arch}/nvector|g' src/nvec_petsc/CMakeLists.txt
sed -i 's|CMAKE_INSTALL_LIBDIR}|CMAKE_INSTALL_LIBDIR}/openmpi/lib|g' src/nvec_petsc/CMakeLists.txt
%endif

mkdir -p build && cd build
%{_openmpi_load}
export CC=mpicc
export CXX=mpicxx
export FC=mpif77

## Blas
export LIBBLASLINK=-lopenblas
export LIBBLAS=libopenblas
export INCBLAS=-I%{_includedir}/openblas
##
## SuperLUMT
%ifarch s390x x86_64
export LIBSUPERLUMTLINK=-lsuperlumt64_d
%endif
%ifarch %{arm} %{ix86}
export LIBSUPERLUMTLINK=-lsuperlumt_d
%endif
%ifnarch s390x x86_64 %{arm} %{ix86}
export LIBSUPERLUMTLINK=
%endif
## Hypre
%if 0%{?with_hypre}
export LIBHYPRELINK="-L$MPI_LIB -lHYPRE"
%endif
##

%if %{with debug}
%undefine _hardened_build
export CFLAGS=""
%if 0%{?rhel}
%global cmake cmake3
%endif
%cmake \
 -DCMAKE_VERBOSE_MAKEFILE:BOOL=ON \
 -DCMAKE_BUILD_TYPE:STRING=Debug \
 -DCMAKE_C_FLAGS_DEBUG:STRING="-O0 -g -Wl,-z,relro -Wl,-z,now -Wl,--as-needed -I$INCBLAS" \
 -DCMAKE_Fortran_FLAGS_DEBUG:STRING="-O0 -g -Wl,-z,relro -Wl,-z,now -Wl,--as-needed -I$INCBLAS" \
 -DCMAKE_SHARED_LINKER_FLAGS_DEBUG:STRING="%{__global_ldflags} -lklu $LIBBLASLINK $LIBSUPERLUMTLINK $LIBHYPRELINK" \
%else
%cmake3 \
%if %{?__isa_bits:%{__isa_bits}}%{!?__isa_bits:32} == 64
 -DSUNDIALS_INDEX_SIZE:STRING=64 \
%else
 -DSUNDIALS_INDEX_SIZE:STRING=32 \
%endif
 -DCMAKE_VERBOSE_MAKEFILE:BOOL=ON \
 -DCMAKE_BUILD_TYPE:STRING=Release \
 -DCMAKE_C_FLAGS_RELEASE:STRING="%{optflags} -I$INCBLAS" \
 -DCMAKE_Fortran_FLAGS_RELEASE:STRING="%{optflags} -I$INCBLAS" \
 -DCMAKE_SHARED_LINKER_FLAGS_RELEASE:STRING="%{__global_ldflags} -lklu $LIBBLASLINK $LIBSUPERLUMTLINK $LIBHYPRELINK" \
%endif
 -DLAPACK_ENABLE:BOOL=OFF \
 -DBLAS_ENABLE:BOOL=ON \
 -DBLAS_LIBRARIES:STRING=%{_libdir}/$LIBBLAS.so \
%if 0%{?with_petsc}
 -DPETSC_ENABLE:BOOL=ON \
 -DPETSC_INCLUDE_DIR:PATH=$MPI_INCLUDE/petsc \
 -DPETSC_LIBRARY_DIR:PATH=$MPI_LIB \
%endif
 -DCMAKE_INSTALL_PREFIX:PATH=%{_prefix} -DCMAKE_INSTALL_LIBDIR:PATH=%{_lib} \
 -DPYTHON_EXECUTABLE:FILEPATH=%{__python2} \
 -DEXAMPLES_ENABLE_CXX:BOOL=ON -DEXAMPLES_ENABLE_C:BOOL=ON -DEXAMPLES_ENABLE_F77:BOOL=ON \
 -DBUILD_SHARED_LIBS:BOOL=ON -DBUILD_STATIC_LIBS:BOOL=OFF \
 -DCMAKE_SKIP_RPATH:BOOL=YES -DCMAKE_SKIP_INSTALL_RPATH:BOOL=YES \
 -DMPI_ENABLE:BOOL=ON \
 -DMPI_C_COMPILER:STRING=$MPI_BIN/mpicc \
 -DMPIEXEC_EXECUTABLE=$MPI_BIN/mpirun \
%if 0%{?fedora}
 -DMPI_Fortran_COMPILER:STRING=$MPI_BIN/mpifort \
%else
 -DMPI_Fortran_COMPILER:STRING=$MPI_BIN/mpif77 \
%endif
 -DFCMIX_ENABLE:BOOL=ON \
 -DUSE_GENERIC_MATH:BOOL=ON \
 -DOPENMP_ENABLE:BOOL=ON \
 -DPTHREAD_ENABLE:BOOL=ON \
%ifnarch %{power64} aarch64
 -DSUPERLUMT_ENABLE:BOOL=ON \
 -DSUPERLUMT_INCLUDE_DIR:PATH=%{_includedir}/SuperLUMT \
 -DSUPERLUMT_LIBRARY_DIR:PATH=%{_libdir} \
 -DSUPERLUMT_THREAD_TYPE:STRING=OpenMP \
%endif
%if 0%{?with_hypre}
 -DHYPRE_ENABLE:BOOL=ON \
 -DHYPRE_INCLUDE_DIR:PATH=$MPI_INCLUDE/hypre \
 -DHYPRE_LIBRARY_DIR:PATH=$MPI_LIB \
%endif
 -DKLU_ENABLE=ON -DKLU_LIBRARY_DIR:PATH=%{_libdir} -DKLU_INCLUDE_DIR:PATH=%{_includedir}/suitesparse \
 -DEXAMPLES_INSTALL:BOOL=OFF -Wno-dev ..

%make_build V=1
%{_openmpi_unload}
cd ..
popd
%endif
######
###########################################################################

%if 0%{?with_mpich}
pushd buildmpich_dir
##Set mpich library's paths
sed -i 's|DESTINATION include/nvector|DESTINATION %{_includedir}/mpich-%{_arch}/nvector|g' src/nvec_par/CMakeLists.txt
sed -i 's|CMAKE_INSTALL_LIBDIR}|CMAKE_INSTALL_LIBDIR}/mpich/lib|g' src/nvec_par/CMakeLists.txt
sed -i 's|DESTINATION include/nvector|DESTINATION %{_includedir}/mpich-%{_arch}/nvector|g' src/nvec_parhyp/CMakeLists.txt
sed -i 's|CMAKE_INSTALL_LIBDIR}|CMAKE_INSTALL_LIBDIR}/mpich/lib|g' src/nvec_parhyp/CMakeLists.txt
%if 0%{?with_petsc}
sed -i 's|DESTINATION include/nvector|DESTINATION %{_includedir}/mpich-%{_arch}/nvector|g' src/nvec_petsc/CMakeLists.txt
sed -i 's|CMAKE_INSTALL_LIBDIR}|CMAKE_INSTALL_LIBDIR}/mpich/lib|g' src/nvec_petsc/CMakeLists.txt
%endif

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
## Blas
export LIBBLASLINK=-lopenblas
export LIBBLAS=libopenblas
export INCBLAS=-I%{_includedir}/openblas
##
## SuperLUMT
%ifarch s390x x86_64
export LIBSUPERLUMTLINK=-lsuperlumt64_d
%endif
%ifarch %{arm} %{ix86}
export LIBSUPERLUMTLINK=-lsuperlumt_d
%endif
%ifnarch s390x x86_64 %{arm} %{ix86}
export LIBSUPERLUMTLINK=
%endif
## Hypre
%if 0%{?with_hypre}
export LIBHYPRELINK="-L$MPI_LIB -lHYPRE"
%endif
##

%if %{with debug}
%undefine _hardened_build
export CFLAGS=""
%if 0%{?rhel}
%global cmake cmake3
%endif
%cmake \
 -DCMAKE_VERBOSE_MAKEFILE:BOOL=ON \
 -DCMAKE_BUILD_TYPE:STRING=Debug \
 -DCMAKE_C_FLAGS_DEBUG:STRING="-O0 -g -Wl,-z,relro -Wl,-z,now -Wl,--as-needed -I$INCBLAS" \
 -DCMAKE_Fortran_FLAGS_DEBUG:STRING="-O0 -g -Wl,-z,relro -Wl,-z,now -Wl,--as-needed -I$INCBLAS" \
 -DCMAKE_SHARED_LINKER_FLAGS_DEBUG:STRING="%{__global_ldflags} -lklu $LIBBLASLINK $LIBSUPERLUMTLINK $LIBHYPRELINK" \
%else
%cmake3 \
%if %{?__isa_bits:%{__isa_bits}}%{!?__isa_bits:32} == 64
 -DSUNDIALS_INDEX_SIZE:STRING=64 \
%else
 -DSUNDIALS_INDEX_SIZE:STRING=32 \
%endif
 -DCMAKE_VERBOSE_MAKEFILE:BOOL=ON \
 -DCMAKE_BUILD_TYPE:STRING=Release \
 -DCMAKE_C_FLAGS_RELEASE:STRING="%{optflags} -I$INCBLAS" \
 -DCMAKE_Fortran_FLAGS_RELEASE:STRING="%{optflags} -I$INCBLAS" \
 -DCMAKE_SHARED_LINKER_FLAGS_RELEASE:STRING="%{__global_ldflags} -lklu $LIBBLASLINK $LIBSUPERLUMTLINK $LIBHYPRELINK" \
%endif
 -DLAPACK_ENABLE:BOOL=OFF \
 -DBLAS_ENABLE:BOOL=ON \
 -DBLAS_LIBRARIES:STRING=%{_libdir}/$LIBBLAS.so \
%if 0%{?with_petsc}
 -DPETSC_ENABLE:BOOL=ON \
 -DPETSC_INCLUDE_DIR:PATH=$MPI_INCLUDE/petsc \
 -DPETSC_LIBRARY_DIR:PATH=$MPI_LIB \
%endif
 -DCMAKE_INSTALL_PREFIX:PATH=%{_prefix} -DCMAKE_INSTALL_LIBDIR:PATH=%{_lib} \
 -DPYTHON_EXECUTABLE:FILEPATH=%{__python2} \
 -DEXAMPLES_ENABLE_CXX:BOOL=ON -DEXAMPLES_ENABLE_C:BOOL=ON -DEXAMPLES_ENABLE_F77:BOOL=ON \
 -DBUILD_SHARED_LIBS:BOOL=ON -DBUILD_STATIC_LIBS:BOOL=OFF \
 -DCMAKE_SKIP_RPATH:BOOL=YES -DCMAKE_SKIP_INSTALL_RPATH:BOOL=YES \
 -DMPI_ENABLE:BOOL=ON \
 -DMPI_C_COMPILER:STRING=$MPI_BIN/mpicc \
 -DMPIEXEC_EXECUTABLE=$MPI_BIN/mpirun \
%if 0%{?fedora}
 -DMPI_Fortran_COMPILER:STRING=$MPI_BIN/mpifort \
%else
 -DMPI_Fortran_COMPILER:STRING=$MPI_BIN/mpif77 \
%endif
 -DFCMIX_ENABLE:BOOL=ON \
 -DUSE_GENERIC_MATH:BOOL=ON \
 -DOPENMP_ENABLE:BOOL=ON \
 -DPTHREAD_ENABLE:BOOL=ON \
%ifnarch %{power64} aarch64
 -DSUPERLUMT_ENABLE:BOOL=ON \
 -DSUPERLUMT_INCLUDE_DIR:PATH=%{_includedir}/SuperLUMT \
 -DSUPERLUMT_LIBRARY_DIR:PATH=%{_libdir} \
 -DSUPERLUMT_THREAD_TYPE:STRING=OpenMP \
%endif
%if 0%{?with_hypre}
 -DHYPRE_ENABLE:BOOL=ON \
 -DHYPRE_INCLUDE_DIR:PATH=$MPI_INCLUDE/hypre \
 -DHYPRE_LIBRARY_DIR:PATH=$MPI_LIB \
%endif
 -DKLU_ENABLE=ON -DKLU_LIBRARY_DIR:PATH=%{_libdir} -DKLU_INCLUDE_DIR:PATH=%{_includedir}/suitesparse \
 -DEXAMPLES_INSTALL:BOOL=OFF -Wno-dev ..

%make_build V=1
%{_mpich_unload}
cd ..
popd
%endif
######
#############################################################################

%install
%if 0%{?with_openmpi}
%{_openmpi_load}
%make_install -C buildopenmpi_dir/build

# Remove static libraries
rm -f %{buildroot}$MPI_LIB/*.a
%{_openmpi_unload}
%endif

%if 0%{?with_mpich}
%{_mpich_load}
%make_install -C buildmpich_dir/build

# Remove static libraries
rm -f %{buildroot}$MPI_LIB/*.a
%{_mpich_unload}
%endif

%make_install -C sundials-%{version}/build

# Remove static libraries
rm -f %{buildroot}%{_libdir}/*.a

# Remove files in bad position
rm -f %{buildroot}%{_prefix}/LICENSE
rm -f %{buildroot}%{_includedir}/sundials/LICENSE

%ldconfig_scriptlets

%check
%if 0%{?with_openmpi}
%if 0%{?with_openmpicheck}
pushd buildopenmpi_dir/build
%{_openmpi_load}
export LD_LIBRARY_PATH=%{buildroot}$MPI_LIB:%{buildroot}%{_libdir}
%if %{with debug}
ctest3 --force-new-ctest-process -VV %{?_smp_mflags} --output-on-failure --debug
%else
ctest3 --force-new-ctest-process %{?_smp_mflags}
%endif
%{_openmpi_unload}
popd
%endif ## if with_openmpicheck
%endif ## if with_openmpi

%if 0%{?with_mpich}
%if 0%{?with_mpichcheck}
pushd buildmpich_dir/build
%{_mpich_load}
export LD_LIBRARY_PATH=%{buildroot}$MPI_LIB:%{buildroot}%{_libdir}
%if %{with debug}
ctest3 --force-new-ctest-process -VV %{?_smp_mflags} --output-on-failure --debug
%else
ctest3 --force-new-ctest-process %{?_smp_mflags}
%endif
%{_mpich_unload}
popd
%endif ## if with_mpichcheck
%endif ## if with_mpich

%if 0%{?with_sercheck}
pushd sundials-%{version}/build
export LD_LIBRARY_PATH=%{buildroot}%{_libdir} 
%if %{with debug}
ctest3 --force-new-ctest-process -VV %{?_smp_mflags} --output-on-failure --debug
%else
ctest3 --force-new-ctest-process %{?_smp_mflags}
%endif
popd
%endif ## if with_sercheck

%files
%license sundials-%{version}/LICENSE
%doc sundials-%{version}/README.md sundials-%{version}/src/README-*
%{_libdir}/libsundials*.so.*

%files devel
%{_libdir}/libsundials*.so
%{_includedir}/sundials/
%{_includedir}/cvode/
%{_includedir}/cvodes/
%{_includedir}/arkode/
%{_includedir}/ida/
%{_includedir}/idas/
%{_includedir}/kinsol/
%{_includedir}/nvector/
%{_includedir}/sunlinsol/
%{_includedir}/sunmatrix/

%if 0%{?with_openmpi}
%files openmpi
%license sundials-%{version}/LICENSE
%doc sundials-%{version}/README.md sundials-%{version}/src/README-*
%{_libdir}/openmpi/lib/libsundials*.so.*

%files openmpi-devel
%{_includedir}/openmpi-%{_arch}/nvector/
%{_libdir}/openmpi/lib/libsundials*.so
%endif

%if 0%{?with_mpich}
%files mpich
%license sundials-%{version}/LICENSE
%doc sundials-%{version}/README.md sundials-%{version}/src/README-*
%{_libdir}/mpich/lib/libsundials*.so.*

%files mpich-devel
%{_includedir}/mpich-%{_arch}/nvector/
%{_libdir}/mpich/lib/libsundials*.so
%endif

%files doc
%license sundials-%{version}/LICENSE
%doc sundials-%{version}/README.md
%doc sundials-%{version}/doc/cvode/cv_guide.pdf
%doc sundials-%{version}/doc/kinsol/kin_guide.pdf
%doc sundials-%{version}/doc/cvodes/cvs_guide.pdf
%doc sundials-%{version}/doc/ida/ida_guide.pdf
%doc sundials-%{version}/doc/arkode/*

%changelog
* Thu Feb 14 2019 Orion Poplawski <orion@nwra.com> - 3.2.1-4
- Rebuild for openmpi 3.1.3
- Disable tests of MPI libraries for "not enough slots available" errors

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Dec 02 2018 Antonio Trande <sagitterATfedoraproject.org> - 3.2.1-2
- PETSc support is now re-enabled (rhbz#1639646)

* Sat Oct 20 2018 Antonio Trande <sagitterATfedoraproject.org> - 3.2.1-1
- Update to 3.2.1
- Disable PETSc support (rhbz#1639646)
- Disable OpenMPI tests (rhbz#1639646)

* Sat Oct 13 2018 Antonio Trande <sagitterATfedoraproject.org> - 3.2.0-1
- Update to 3.2.0

* Wed Sep 05 2018 Antonio Trande <sagitterATfedoraproject.org> - 3.1.2-2
- Forced to use python2 (tests work under python2 only)

* Wed Aug 01 2018 Antonio Trande <sagitterATfedoraproject.org> - 3.1.2-1
- Update to 3.1.2
- Enable PETSC support

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jun 06 2018 Antonio Trande <sagitterATfedoraproject.org> - 3.1.1-2
- Do not pack examples
- Use SuperLUMT64 on 64bit systems

* Sun May 13 2018 Antonio Trande <sagitterATfedoraproject.org> - 3.1.1-1
- Update to 3.1.1

* Fri May 04 2018 Antonio Trande <sagitterATfedoraproject.org> - 3.1.0-5
- Rebuild for hypre-2.14.0

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Feb 02 2018 Antonio Trande <sagitterATfedoraproject.org> - 3.1.0-3
- Use %%ldconfig_scriptlets

* Wed Jan 31 2018 Antonio Trande <sagitterATfedoraproject.org> - 3.1.0-2
- Rebuild for GCC-8

* Fri Dec 22 2017 Antonio Trande <sagitterATfedoraproject.org> - 3.1.0-1
- Update to 3.1.0

* Wed Nov 15 2017 Antonio Trande <sagitterATfedoraproject.org> - 3.0.0-3
- Use -Wl,--as-needed flag
- Fix shared-linker flags

* Thu Nov 09 2017 Antonio Trande <sagitterATfedoraproject.org> - 3.0.0-2
- Remove sub-packages
- Uninstall static libraries

* Mon Oct 30 2017 Antonio Trande <sagitterATfedoraproject.org> - 3.0.0-1
- Update to 3.0.0
- Use cmake3 on epel
- Install examples

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Mar 03 2017 Antonio Trande <sagitterATfedoraproject.org> - 2.7.0-10
- Build OpenMPI libraries on EPEL

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

