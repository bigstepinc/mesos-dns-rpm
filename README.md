# Mesos DNS RPM

An unofficial RPM spec file for the Mesos DNS (0.5.2) service discovery system.

## Building

```shell
$ build_root=~/rpmbuild/

$ sudo yum -y install rpm-build gcc git

$ wget https://github.com/bigstepinc/mesos-dns-rpm/blob/master/mesos-dns.spec  $build_root/SPECS/mesos-dns.spec
$ wget https://github.com/bigstepinc/mesos-dns-rpm/blob/master/mesos-dns-init-wrapper  $build_root/SOURCES/mesos-dns-init-wrapper
$ wget https://github.com/bigstepinc/mesos-dns-rpm/blob/master/mesos-dns.service $build_root/SOURCES/mesos-dns.service
$ wget https://github.com/bigstepinc/mesos-dns-rpm/blob/master/config.json $build_root/SOURCES/config.json.template

$ wget https://github.com/mesosphere/mesos-dns/archive/v0.5.2.tar.gz -O $build_root/SOURCES/v0.5.2.tar.gz
$ wget https://storage.googleapis.com/golang/go1.6.2.linux-amd64.tar.gz -O $build_root/SOURCES/go1.6.2.linux-amd64.tar.gz

rpmbuild -bb $build_root/SPECS/mesos-dns.spec
```
