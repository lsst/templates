# Change log

## 2018-06-21

- Add `disableCc=True` argument to the `SConstruct` for Python-only packages.
  ([DM-14860](https://jira.lsstcorp.org/browse/DM-14860))

## 2018-06-04

- Remove version pinning from `ups/{{package_name}}.table`.
  Version pinning isn't used anymore since all packages are tagged together.
  ([DM-14668](https://jira.lsstcorp.org/browse/DM-14668))
