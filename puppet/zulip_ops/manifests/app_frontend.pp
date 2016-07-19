class zulip_ops::app_frontend {
  include zulip::app_frontend_base
  include zulip::memcached
  include zulip::rabbit
  include zulip::postfix_localmail
  include zulip::static_asset_compiler
  $app_packages = [# Needed for the ssh tunnel to the redis server
                   "autossh",
                   ]
  package { $app_packages: ensure => "installed" }

  file { "/etc/nginx/zulip-include/app.d/accept-loadbalancer.conf":
    require => Package["nginx-full"],
    owner  => "root",
    group  => "root",
    mode => 644,
    source => "puppet:///modules/zulip_ops/nginx/zulip-include-app.d/accept-loadbalancer.conf",
    notify => Service["nginx"],
  }

  file { '/etc/log2zulip.conf':
    ensure     => file,
    owner      => "zulip",
    group      => "zulip",
    mode       => 644,
    source     => 'puppet:///modules/zulip_ops/log2zulip.conf',
  }

  file { '/etc/cron.d/log2zulip':
    ensure     => file,
    owner      => "root",
    group      => "root",
    mode       => 644,
    source     => 'puppet:///modules/zulip_ops/cron.d/log2zulip',
  }

  file { '/etc/log2zulip.zuliprc':
    ensure     => file,
    owner      => "zulip",
    group      => "zulip",
    mode       => 600,
    source     => 'puppet:///modules/zulip_ops/log2zulip.zuliprc',
  }
  file { "/etc/cron.d/check-apns-tokens":
    ensure => file,
    owner  => "root",
    group  => "root",
    mode => 644,
    source => "puppet:///modules/zulip_ops/cron.d/check-apns-tokens",
  }
}
