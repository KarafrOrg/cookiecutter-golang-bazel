module {{  cookiecutter.github_host }}/{{ cookiecutter.owner  }}/{{ cookiecutter.app_name }}

go {{ cookiecutter.go_version }}

require ()

tool (
	github.com/google/keep-sorted
	github.com/katexochen/sh/v3/cmd/shfmt
	github.com/rhysd/actionlint/cmd/actionlint
	golang.org/x/tools/cmd/stringer
	golang.org/x/vuln
	golang.org/x/vuln/cmd/govulncheck
	mvdan.cc/gofumpt
	mvdan.cc/sh/v3/cmd/gosh
)
