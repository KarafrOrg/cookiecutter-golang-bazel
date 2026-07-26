"""Tests for the cookiecutter-golang-bazel template."""

import pytest

BASE_CONTEXT = {
    "app_name": "my-app",
    "app_description": "A simple hello world application",
    "owner": "testowner",
    "github_host": "github.com",
    "go_version": "1.22.0",
    "use_git": "n",
    "init_go_mod": "n",
    "init_bzl_mod": "n",
}


def test_bake_with_defaults(cookies):
    result = cookies.bake(extra_context=BASE_CONTEXT)
    assert result.exit_code == 0
    assert result.exception is None
    assert result.project_path.is_dir()


def test_project_directory_name_matches_app_name(cookies):
    result = cookies.bake(extra_context=BASE_CONTEXT)
    assert result.project_path.name == "my-app"


def test_custom_app_name(cookies):
    result = cookies.bake(extra_context={**BASE_CONTEXT, "app_name": "awesome-svc"})
    assert result.exit_code == 0
    assert result.project_path.name == "awesome-svc"


def test_go_mod_module_path(cookies):
    result = cookies.bake(extra_context=BASE_CONTEXT)
    content = (result.project_path / "go.mod").read_text()
    assert "module github.com/testowner/my-app" in content


def test_go_mod_go_version(cookies):
    result = cookies.bake(extra_context=BASE_CONTEXT)
    content = (result.project_path / "go.mod").read_text()
    assert "go 1.22.0" in content


def test_go_mod_custom_owner_and_host(cookies):
    ctx = {**BASE_CONTEXT, "owner": "acme", "github_host": "gitlab.com"}
    result = cookies.bake(extra_context=ctx)
    content = (result.project_path / "go.mod").read_text()
    assert "module gitlab.com/acme/my-app" in content


def test_module_bazel_name(cookies):
    result = cookies.bake(extra_context=BASE_CONTEXT)
    content = (result.project_path / "MODULE.bazel").read_text()
    assert 'name = "my-app"' in content


def test_module_bazel_custom_name(cookies):
    ctx = {**BASE_CONTEXT, "app_name": "cool-tool"}
    result = cookies.bake(extra_context=ctx)
    content = (result.project_path / "MODULE.bazel").read_text()
    assert 'name = "cool-tool"' in content


def test_cmd_directory_uses_app_name(cookies):
    result = cookies.bake(extra_context=BASE_CONTEXT)
    cmd_dir = result.project_path / "cmd" / "my-app"
    assert cmd_dir.is_dir()


def test_cmd_main_go_exists(cookies):
    result = cookies.bake(extra_context=BASE_CONTEXT)
    assert (result.project_path / "cmd" / "my-app" / "main.go").is_file()


def test_cmd_main_go_references_app_name(cookies):
    result = cookies.bake(extra_context=BASE_CONTEXT)
    content = (result.project_path / "cmd" / "my-app" / "main.go").read_text()
    assert "my-app" in content


def test_gitignore_absent_when_use_git_n(cookies):
    result = cookies.bake(extra_context=BASE_CONTEXT)
    assert not (result.project_path / ".gitignore").exists()


def test_gitignore_present_when_use_git_y(cookies):
    ctx = {**BASE_CONTEXT, "use_git": "y"}
    result = cookies.bake(extra_context=ctx)
    assert result.exit_code == 0
    assert (result.project_path / ".gitignore").exists()


@pytest.mark.parametrize(
    "filepath",
    [
        "go.mod",
        "go.work",
        "MODULE.bazel",
        "BUILD.bazel",
        ".bazelrc",
        ".bazelversion",
        ".golangci.yml",
        ".shellcheckrc",
        ".editorconfig",
        ".gitattributes",
        "scripts/BUILD.bazel",
        "scripts/govulncheck.sh.in",
        "scripts/go_generate.sh.in",
        "scripts/go_tidy.sh.in",
        "scripts/buildifier_check.sh.in",
        "scripts/unused_gh_actions.sh.in",
        "bazel/shell/lib.bash",
        "bazel/shell/repo_command.sh.in",
        "bazel/shell/def.bzl",
        "bazel/version.bzl",
        "bazel/platforms.bzl",
        "docs/README.md",
    ],
)
def test_required_file_present(cookies, filepath):
    result = cookies.bake(extra_context=BASE_CONTEXT)
    assert (result.project_path / filepath).exists(), f"Missing: {filepath}"


def test_repo_command_bash_array_syntax_preserved(cookies):
    """${#args[@]} must not be mangled by Jinja2 raw-block handling."""
    result = cookies.bake(extra_context=BASE_CONTEXT)
    content = (
            result.project_path / "bazel" / "shell" / "repo_command.sh.in"
    ).read_text()
    assert "${#args[@]}" in content
    assert "{% raw %}" not in content
    assert "{% endraw %}" not in content


def test_govulncheck_bash_array_syntax_preserved(cookies):
    """${#binaries[@]} must survive generation intact."""
    result = cookies.bake(extra_context=BASE_CONTEXT)
    content = (result.project_path / "scripts" / "govulncheck.sh.in").read_text()
    assert "${#binaries[@]}" in content
    assert "{% raw %}" not in content
    assert "{% endraw %}" not in content


def test_buildifier_bash_array_syntax_preserved(cookies):
    result = cookies.bake(extra_context=BASE_CONTEXT)
    content = (result.project_path / "scripts" / "buildifier_check.sh.in").read_text()
    assert "${#files[@]}" in content


def test_unused_gh_actions_bash_array_syntax_preserved(cookies):
    result = cookies.bake(extra_context=BASE_CONTEXT)
    content = (result.project_path / "scripts" / "unused_gh_actions.sh.in").read_text()
    assert "${#unusedActions[@]}" in content


def test_go_generate_go_template_syntax_preserved(cookies):
    """{{.Dir}} is a Go template literal that must survive Jinja2 rendering."""
    result = cookies.bake(extra_context=BASE_CONTEXT)
    content = (result.project_path / "scripts" / "go_generate.sh.in").read_text()
    assert "{{.Dir}}" in content


def test_go_tidy_go_template_syntax_preserved(cookies):
    result = cookies.bake(extra_context=BASE_CONTEXT)
    content = (result.project_path / "scripts" / "go_tidy.sh.in").read_text()
    assert "{{.Dir}}" in content
