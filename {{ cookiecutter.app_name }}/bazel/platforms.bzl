"""Centralised list of (goos, goarch) platforms {{ cookiecutter.app_name }} is cross-built for.

Used by cmd/{{ cookiecutter.app_name }} to emit one `go_cross_binary`
target per platform plus a `:all_platforms` filegroup that ties them
together. The list intentionally favours the platforms our users
actually run on (and that GitHub release assets typically ship for) to
keep `bazel build //...` fast.
"""

# Each entry becomes a target suffix and resolves to
# @rules_go//go/toolchain:<entry>.
PLATFORMS = [
    "darwin_amd64",
    "darwin_arm64",
    "linux_amd64",
    "linux_arm64",
    "windows_amd64",
    "windows_arm64",
]

def go_toolchain_platform(name):
    """Return the @rules_go//go/toolchain label for `name`."""
    return "@rules_go//go/toolchain:" + name

def cross_binary_basename(binary_name, platform):
    """Stable filename used by go_cross_binary's `basename` attr.

    Encodes the OS / arch in the output so prebuilt artefacts can be
    distinguished after they leave the bazel-bin tree (CI uploads,
    GitHub releases, manual scp, ...). Windows targets get a `.exe`
    suffix because Go demands it.
    """
    suffix = ".exe" if platform.startswith("windows_") else ""
    return "%s-%s%s" % (binary_name, platform.replace("_", "-"), suffix)
