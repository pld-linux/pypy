#
# Conditional build:
%bcond_without	tests		# do not perform "make test"
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
URL:		http://pypy.org
BuildRequires:	rpm-pythonprov
BuildRequires:	libffi-static
%if %{with bootstrap}
BuildRequires:	python-modules
%else
BuildRequires:	pypy-modules
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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

%build
cd pypy/translator/goal
CC="%{__cc}" \
CFLAGS="%{rpmcflags}" \
%{__python} translate.py -Ojit

%install
rm -rf $RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README LICENSE
