![Build](https://github.com/basicwolf/sphinx-testify/actions/workflows/ci.yml/badge.svg)

# Sphinx-testify

sphinx-testify is an extension to the Sphinx documentation generator,
that enables building [testified documentation][] and, ultimately
[living documentation][].

[testified documentation]: https://sphinx-testify.readthedocs.io/en/latest/testified-documentation.html
[living documentation]: https://gojko.net/books/specification-by-example/

## Testified documentation in a nutshell

Testified documentation means that the documentation source references test
results, and these references are verified during the build process.
As a result, we can keep every paragraph even every sentence of
the documentation aligned with the code, as long as there is a test
that "testifies" the described behaviour.


## A simple example

Imagine you're working on a system access module.
Even *before* writing any tests or code, you can briefly document
the expected behavior and reference the (to-be-created) tests.
Proceed with a TDD cycle, and once all the tests and implementation
are ready, you’ll have testified and living documentation.

Here's how it looks like in a reStructuredText document:

```rst

   System access
   =============

   Only a user with valid credentials: a username and a password can access
   the system. If credentials are wrong, the system returns "Authentication failed"
   error message.

   .. testify::
      test_a_user_can_access_system_with_username_and_password
      test_system_returns_authentication_failed_error_when_username_is_not_found
      test_system_returns_authentication_failed_error_when_password_is_wrong
```

## A full example

You practice what you preach. It would be hypocritical to develop sphinx-testify
in a way different from what is described above.
What it means is that the documentation to the library is testified!
Everything you need for a real-world example is in the same repository.

## Installation

```shell
pip install sphinx-testify
```

## Links

Code: https://github.com/BasicWolf/sphinx-testify
<br>
Docs: https://sphinx-testify.readthedocs.io/en/latest/

## License

GPLv3
