Name:           I2util
Version:        1.2
Release:        2.1%{?dist}
Summary:        I2 Utility Library
License:        distributable, see LICENSE
Group:          Development/Libraries
Source0:        I2util-%{version}.tar.gz

%description
I2 Utility library. Currently contains:
	* error logging
	* command-line parsing
	* threading
	* random number support
	* hash table support

The error logging and command-line parsing are taken from a utility library
that is distributed with the "volsh" code from UCAR.

        http://www.scd.ucar.edu/vets/vg/Software/volsh

%prep
%setup -q

%build
%configure

%install
%makeinstall

%files
%defattr(-,root,root,-)
#%doc Changes LICENSE README
%doc README
%{_bindir}/*
%{_libdir}/libI2util.a
%{_mandir}/man1/*
%{_includedir}/*

%changelog
* Tue Jan 4 2018 efajardo@physics.ucsd.edu 1.2-2
- Adding the dist tag

* Fri Jan 11 2008 aaron@internet2.edu 1.0-1
- Initial RPM
