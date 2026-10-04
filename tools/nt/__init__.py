"""NashikTourism.com content layer.

The site is static HTML, built by the generators in tools/. This package is the
shared, dependency-free library they sit on: it loads and validates the
editorial data in /data, applies the verification and risk policy, computes the
Kumbh lifecycle phase, and renders the small pieces of HTML (status badges,
verification blocks, update and event cards) that every generated page reuses.

Nothing here fetches the network. Network access lives in tools/monitor-sources.py.
"""
