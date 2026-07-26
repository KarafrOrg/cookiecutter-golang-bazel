package main

import (
	"fmt"
	"os"
)

var commit, version, gitTreeState string

func main() {
	_, _ = fmt.Fprintf(os.Stderr, "{{ cookiecutter.app_name }} version %s-%s-%s", version, gitTreeState, commit)
}
