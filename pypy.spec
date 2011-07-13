#
# Conditional build:
%bcond_with	tests		# do perform tests
%bcond_without	bootstrap	# use PyPi

%if %{without bootstrap}
%define	__python pypy
%endif

Summary:	PyPy - a fast, alternative implementation of the Python language
Name:		pypy
Version:	1.5
Release:	0.1
License:	distributable
Group:		Development/Languages/Python
Source0:	http://cdn.bitbucket.org/pypy/pypy/downloads/%{name}-%{version}-src.tar.bz2
# Source0-md5:	cb9ada2c50666318c3a2863da1fbe487
Patch0:		%{name}-curses.patch
URL:		http://pypy.org
BuildRequires:	rpm-pythonprov
BuildRequires:	libffi-static
%if %{with bootstrap}
BuildRequires:	python-modules
%else
BuildRequires:	pypy-modules
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define pypy_libdir %{_libdir}/%{name}-%{version}

%description
PyPy is a fast, compliant alternative implementation of the Python
language (2.7.1). It has several advantages and distinct features:

- Speed: thanks to its Just-in-Time compiler, Python programs often
  run faster on PyPy. (What is a JIT compiler?)
- Memory usage: large, memory-hungry Python programs might end up
  taking less space than they do in CPython.
- Compatibility: PyPy is highly compatible with existing python code.
  It supports ctypes and can run popular python libraries like twisted
  and django.
- Sandboxing: PyPy provides the ability to run untrusted code in a
  fully secure way.
- Stackless: PyPy can be configured to run in stackless mode,
  providing micro-threads for massive concurrency.
- As well as other features.

%prep
%setup -q -n %{name}-%{version}-src
%patch0 -p1

%build
cd pypy/translator/goal
CC="%{__cc}" \
CFLAGS="%{rpmcflags}" \
%{__python} translate.py -Ojit
cd ../../..

%if %{with tests}
pypy/translator/goal/pypy-c ./pytest.py
%endif

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{pypy_libdir},%{_bindir}}

cp -R ctypes_configure demo dotviewer include lib_pypy lib-python py pypy \
	site-packages $RPM_BUILD_ROOT%{pypy_libdir}

rm -rf 	$RPM_BUILD_ROOT%{pypy_libdir}/pypy/doc \
	$RPM_BUILD_ROOT%{pypy_libdir}/pypy/translator/goal/*.bat \
	$RPM_BUILD_ROOT%{pypy_libdir}/pypy/translator/goal/test2 \
	$RPM_BUILD_ROOT%{pypy_libdir}/pypy/translator/goal/win32 \
	$RPM_BUILD_ROOT%{pypy_libdir}/site-packages/README

# do not require other python in installed scripts
find $RPM_BUILD_ROOT%{pypy_libdir} -name '*.py' | xargs \
	sed -i -r -e'1s@^#! ?(/usr/bin/env python|/usr(/local)?/bin/python)@#!%{_bindir}/pypy@'

ln -s %{pypy_libdir}/pypy/translator/goal/pypy-c $RPM_BUILD_ROOT%{_bindir}/pypy

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README LICENSE pypy/doc
%attr(755,root,root) %{_bindir}/pypy
%dir %{pypy_libdir}
%{pypy_libdir}/ctypes_configure
%{pypy_libdir}/demo
%{pypy_libdir}/dotviewer
%{pypy_libdir}/include
%{pypy_libdir}/lib-python
%{pypy_libdir}/lib_pypy
%{pypy_libdir}/py
%dir %{pypy_libdir}/pypy
%{pypy_libdir}/pypy/_cache
%{pypy_libdir}/pypy/annotation
%{pypy_libdir}/pypy/bin
%{pypy_libdir}/pypy/config
%{pypy_libdir}/pypy/interpreter
%{pypy_libdir}/pypy/jit
%{pypy_libdir}/pypy/module
%{pypy_libdir}/pypy/objspace
%{pypy_libdir}/pypy/rlib
%{pypy_libdir}/pypy/rpython
%{pypy_libdir}/pypy/tool
%dir %{pypy_libdir}/pypy/translator
%{pypy_libdir}/pypy/translator/backendopt
%{pypy_libdir}/pypy/translator/c
%{pypy_libdir}/pypy/translator/cli
%dir %{pypy_libdir}/pypy/translator/goal
%{pypy_libdir}/pypy/translator/goal/*.py
%{pypy_libdir}/pypy/translator/goal/*.pyc
%{pypy_libdir}/pypy/translator/goal/pypy-c
%{pypy_libdir}/pypy/translator/jvm
%{pypy_libdir}/pypy/translator/llsupport
%{pypy_libdir}/pypy/translator/microbench
%{pypy_libdir}/pypy/translator/oosupport
%{pypy_libdir}/pypy/translator/platform
%{pypy_libdir}/pypy/translator/sandbox
%{pypy_libdir}/pypy/translator/stackless
%{pypy_libdir}/pypy/translator/test
%{pypy_libdir}/pypy/translator/tool
%{pypy_libdir}/pypy/translator/*.py
%{pypy_libdir}/pypy/translator/*.pyc
%{pypy_libdir}/pypy/translator/goal/launch-bench-cronjob.sh
%{pypy_libdir}/pypy/*.py
%{pypy_libdir}/pypy/*.pyc
%{pypy_libdir}/pypy/*.cfg
%dir %{pypy_libdir}/site-packages
