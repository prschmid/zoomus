# Contributing

## Setting Up Your Development Environment

You should use a virtualenv for working on this project, as that will keep all
installed packages isolated, without interfering with any global packages. To
create a virtualenv and install all necessary dependencies, simply run the
following commands:

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -r requirements-test.txt
```

## Branching

If you would like to contribute to this project, you will need to use
[git flow](https://github.com/nvie/gitflow). This way, any and all changes
happen on the development branch and not on the master branch. As such, after
you have git-flow-ified your `zoomus` git repo, create a pull request for your
branch, and we'll take it from there.

## Code Formatting

To make code formatting easy on developers, and to simplify the conversation
around pull request reviews, this project has adopted the
[black](https://pypi.org/project/black/) code formatter. This formatter must
be run against any new code written for this project. The advantage is, you
no longer have to think about how your code is styled; it's all handled for you!

To make this easier on you, you can [set up most editors][black-editors] to
auto-run `black` for you. You can also use `pre-commit` to automagically run
`black` for you before every commit! For this, you just need to run the following
once:

```sh
$ pipenv run pre-commit install
pre-commit installed at .git/hooks/pre-commit
```

## Running the Tests

Tests should be run using [tox](https://pypi.python.org/pypi/tox), so that we
can ensure they are run the same way, in a similar isolated environment, every
time. Running this is as simple as one single command:

```sh
tox
```

Assuming all goes well, you should see a result akin to

```sh
  py27: commands succeeded
  py35: commands succeeded
  py36: commands succeeded
  py37: commands succeeded
  pypy: commands succeeded
  pypy3: commands succeeded
  congratulations :)
```

### Multiple Python Versions

It is highly recommended, although not absolutely necessary, that you run the tests
against all of our configured Python versions. This will help ensure that no
unexpected errors come up in our CI process which might delay your changes from
being merged.

These versions are currently:

* 2.7
* 3.5
* 3.6
* 3.7
* pypy2
* pypy3

For an easy way to install and manage all of the Python versions, you may want
to look at using [pyenv](https://github.com/pyenv/pyenv).

**Note:** If you are using OS X and installed `pyenv` with brew, make sure to
follow [these instructions](https://github.com/pyenv/pyenv#homebrew-on-macos)
as well.

[black-editors]: https://github.com/psf/black#editor-integration
