%global pypi_name oslo.policy
%global pkg_name oslo-policy

%if 0%{?fedora} >=24
%global with_python3 1
%endif

Name:           python-%{pkg_name}
Version:        XXX
Release:        XXX
Summary:        OpenStack oslo.policy library

License:        ASL 2.0
URL:            https://launchpad.net/oslo
Source0:        https://pypi.python.org/packages/source/o/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch

%description
An OpenStack library for policy.

%package -n python2-%{pkg_name}
Summary:        OpenStack oslo.policy library
%{?python_provide:%python_provide python2-%{pkg_name}}

BuildRequires:  python2-devel
BuildRequires:  python-pbr
# test dependencies
BuildRequires:  python-hacking
BuildRequires:  python-oslotest
BuildRequires:  python-requests-mock
BuildRequires:  python-coverage
BuildRequires:  python-fixtures
BuildRequires:  python-mock

Requires:       python-oslo-config >= 2.3.0
Requires:       python-oslo-i18n >= 1.5.0
Requires:       python-oslo-serialization >= 1.4.0
Requires:       python-oslo-utils >= 2.0.0
Requires:       python-six >= 1.9.0

%description -n python2-%{pkg_name}
An OpenStack library for policy.

%package -n python-%{pkg_name}-doc
Summary:    Documentation for the Oslo policy library

BuildRequires:  python-sphinx
BuildRequires:  python-oslo-sphinx
BuildRequires:  python-oslo-config
BuildRequires:  python-oslo-serialization
BuildRequires:  python-oslo-i18n

%description -n python-%{pkg_name}-doc
Documentation for the Oslo policy library.

%package -n python-%{pkg_name}-tests
Summary:    Test subpackage for the Oslo policy library

Requires:  python-%{pkg_name} = %{version}-%{release}
Requires:  python-hacking
Requires:  python-oslotest
Requires:  python-requests-mock
Requires:  python-coverage
Requires:  python-fixtures
Requires:  python-mock

%description -n python-%{pkg_name}-tests
Test subpackage for the Oslo policy library

%if 0%{?with_python3}
%package -n python3-%{pkg_name}
Summary:        OpenStack oslo.policy library
%{?python_provide:%python_provide python3-%{pkg_name}}

BuildRequires:  python3-devel
BuildRequires:  python3-pbr
# test dependencies
BuildRequires:  python3-hacking
BuildRequires:  python3-oslotest
BuildRequires:  python3-requests-mock
BuildRequires:  python3-coverage
BuildRequires:  python3-fixtures
BuildRequires:  python3-mock

Requires:       python3-oslo-config >= 2.3.0
Requires:       python3-oslo-i18n >= 1.5.0
Requires:       python3-oslo-serialization >= 1.4.0
Requires:       python3-oslo-utils >= 2.0.0
Requires:       python3-six >= 1.9.0

%description -n python3-%{pkg_name}
An OpenStack library for policy.
%endif

%prep
%setup -q -n %{pypi_name}-%{upstream_version}
# Let RPM handle the dependencies
rm -f requirements.txt

%build
%py2_build

# generate html docs
sphinx-build doc/source html
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}

%if 0%{?with_python3}
%py3_build
%endif

%install
%py2_install

%if 0%{?with_python3}
%py3_install
%endif

%check
# Due to old version of python-fixtures, one test is failing
# so we are skipping the tests
%{__python2} setup.py test ||
%if 0%{?with_python3}
rm -rf .testrepository
%{__python3} setup.py test ||
%endif

%files -n python2-%{pkg_name}
%doc README.rst
%license LICENSE
%{python2_sitelib}/oslo_policy
%{python2_sitelib}/*.egg-info
%exclude %{python2_sitelib}/oslo_policy/tests

%files -n python-%{pkg_name}-doc
%doc html
%license LICENSE

%files -n python-%{pkg_name}-tests
%{python2_sitelib}/oslo_policy/tests

%if 0%{?with_python3}
%files -n python3-%{pkg_name}
%doc README.rst
%license LICENSE
%{python3_sitelib}/oslo_policy
%{python3_sitelib}/*.egg-info
%exclude %{python3_sitelib}/oslo_policy/tests
%endif

%changelog
