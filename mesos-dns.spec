# To Build:
#
# sudo yum -y install rpm-build gcc git
#
# wget https://github.com/bigstepinc/mesos-dns-rpm/blob/master/mesos-dns.spec  build_root/SPECS/mesos-dns.spec
# wget https://github.com/bigstepinc/mesos-dns-rpm/blob/master/mesos-dns-init-wrapper  build_root/SOURCES/mesos-dns-init-wrapper
# wget https://github.com/bigstepinc/mesos-dns-rpm/blob/master/mesos-dns.service build_root/SOURCES/mesos-dns.service
# wget https://github.com/bigstepinc/mesos-dns-rpm/blob/master/config.json build_root/SOURCES/config.json.template
#
# wget https://github.com/mesosphere/%{name}/archive/v%{version}.tar.gz -O build_root/SOURCES/v%{version}.tar.gz
# wget https://storage.googleapis.com/golang/go%{golang_version}.linux-amd64.tar.gz -O build_root/SOURCES/go%{golang_version}.linux-amd64.tar.gz
#
# rpmbuild -bb build_root/SPECS/mesos-dns.spec


%define golang_version		1.6.2


Name:			mesos-dns
Version:		0.5.2
Release:		0%{?dist}
Summary:		Apache Mesos DNS

Group:			Applications/System
License:		Apache 2.0
URL:			https://mesosphere.github.io/mesos-dns/

Source0:		https://github.com/mesosphere/mesos-dns/archive/v%{version}.tar.gz
Source1:		https://storage.googleapis.com/golang/go%{golang_version}.linux-amd64.tar.gz
Source2:		%{name}-init-wrapper
Source3:		%{name}.service
Source4:		config.json.template

BuildRequires:		git
BuildRequires:		gcc
BuildRequires:		systemd-units

Packager:		Cristian Pop <cristian.pop@bigstep.com>


%description
Mesos-DNS supports service discovery in Apache Mesos clusters. It allows
applications and services running on Mesos to find each other through the
domain name system (DNS), similarly to how services discover each other
throughout the Internet.


%prep
%setup -b 0
%setup -b 1

mkdir -p %{_builddir}/go/pkgs


%build
export GOPATH=%{_builddir}/go/pkgs
export GOROOT=%{_builddir}/go
export PATH=$PATH:$GOROOT/bin

go get github.com/tools/godep

go get github.com/mesosphere/mesos-dns/logging
go get github.com/mesosphere/mesos-dns/records
go get github.com/mesosphere/mesos-dns/resolver

go build -a -ldflags "-B 0x$(head -c20 /dev/urandom | od -An -tx1 | tr -d ' \n')"


%install
install -d -m 755 %{buildroot}/%{_sbindir}
install    -m 755 %{_builddir}/%{name}-%{version}/%{name}-%{version} 	%{buildroot}/%{_sbindir}/%{name}

install -d -m 755 %{buildroot}/%{_bindir}
install    -m 755 %{_sourcedir}/%{name}-init-wrapper 			%{buildroot}/%{_bindir}/%{name}-init-wrapper

install -d -m 755 %{buildroot}/usr/lib/systemd/system
install    -m 755 %{_sourcedir}/%{name}.service 			%{buildroot}/%{_unitdir}/%{name}.service

install -d -m 755 %{buildroot}/%{_sysconfdir}/%{name}
install    -m 755 %{_sourcedir}/config.json.template			%{buildroot}/%{_sysconfdir}/%{name}/config.json.template


%post
%systemd_post %{name}.service


%preun
%systemd_preun %{name}.service


%postun
%systemd_postun_with_restart %{name}.service


%clean
rm -rf %{buildrootdir}


%files
%defattr(-, root, root, -)

%{_sbindir}/%{name}
%{_bindir}/%{name}-init-wrapper

%{_unitdir}/%{name}.service

%config(noreplace) %{_sysconfdir}/%{name}/config.json.template


%changelog
* Tue Apr 26 2016 Cristian Pop <cristian.pop@bgistep.com> 0.5.2-0%{?dist}
- Mesos DNS.
