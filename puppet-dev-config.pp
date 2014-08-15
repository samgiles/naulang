class pypydev {
  package {[
    "gcc",
    "make",
    "python-dev",
    "python-pygame",
    "libffi-dev",
    "libsqlite3-dev",
    "pkg-config",
    "libz-dev",
    "libbz2-dev",
    "libncurses-dev",
    "libexpat1-dev",
    "libssl-dev",
    "libgc-dev",
    "python-sphinx",
    "python-greenlet",
    "pypy",
    "python-pip",
    "libffi-devel",
  ]:
    ensure => present
  }
}

node default {
  include pypydev
}
