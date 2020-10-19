FROM debian:buster AS musl-builder
MAINTAINER iwamura

RUN mkdir -p /opt/musl
COPY pincette.patch /opt/musl/
RUN (echo deb-src http://deb.debian.org/debian buster main; \
  echo deb-src http://security.debian.org/debian-security buster/updates main; \
  echo deb-src http://deb.debian.org/debian buster-updates main) \
  >> /etc/apt/sources.list &&\
  apt-get update &&\
  apt-get --no-install-recommends -y install dpkg-dev quilt devscripts curl systemd &&\
  apt-get --no-install-recommends -y build-dep musl &&\
  cd /opt/musl &&\
  apt-get source musl &&\
  cd musl*/ &&\
  quilt import ../pincette.patch &&\
  dch --local pincette "Build for pincette challenge." &&\
  CFLAGS=-O0 dpkg-buildpackage -us -uc

CMD ["/bin/bash"]
