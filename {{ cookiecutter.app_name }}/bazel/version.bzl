"""Single source of truth for the {{ cookiecutter.app_name }} module version.

Bazel's MODULE.bazel cannot load .bzl files, so the version literal in
MODULE.bazel must be kept in sync with VERSION below by hand. Anything
that needs to embed the version at build time (e.g. go_binary x_defs)
loads it from here instead of duplicating the string.
"""

VERSION = "0.1.0"
