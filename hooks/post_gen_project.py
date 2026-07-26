"""
Does the following:

1. Inits git if used
2. Deletes dockerfiles if not going to be used
3. Deletes config utils if not needed
"""

import os
from subprocess import Popen

# Get the root project directory
PROJECT_DIRECTORY = os.path.realpath(os.path.curdir)


def remove_file(filename):
    """
    generic remove file from project dir
    """
    fullpath = os.path.join(PROJECT_DIRECTORY, filename)
    if os.path.exists(fullpath):
        os.remove(fullpath)


def init_git() -> None:
    """
    Initialize git on the new project folder
    :return None
    """
    commands = [
        ["git", "init"],
        ["git", "add", "."],
        [
            "git",
            "remote",
            "add",
            "origin",
            "git@{{ cookiecutter.github_host }}:{{ cookiecutter.owner }}/{{ cookiecutter.app_name }}.git",
        ],
    ]

    for command in commands:
        git = Popen(command, cwd=PROJECT_DIRECTORY)
        git.wait()


def init_go_mod() -> None:
    """
    Initialize go mod dependendies
    :return: None
    """
    commands = [["go", "mod", "tidy"]]

    for command in commands:
        go_mod = Popen(command, cwd=PROJECT_DIRECTORY)
        go_mod.wait()


def init_bzl_mod() -> None:
    """
    Initialize bazel module
    :return: None
    """
    commands = [["bazel", "run", "@//:tidy"], ["bazel", "mod", "tidy"]]
    for command in commands:
        bzl_mod = Popen(command, cwd=PROJECT_DIRECTORY)
        bzl_mod.wait()


if "{{ cookiecutter.init_go_mod }}".lower() == "y":
    init_go_mod()
if "{{ cookiecutter.init_bzl_mod }}".lower() == "y":
    init_bzl_mod()
if "{{ cookiecutter.use_git }}".lower() == "y":
    init_git()
else:
    remove_file(".gitignore")
