# Contributing

Thank you for your interest in pushing Sphinx-testify boundaries further!
Contributions are very much welcome.

Let’s discuss your idea first - please open an issue in the project's
issue tracker at https://github.com/BasicWolf/sphinx-testify/issues,
and I’ll get back to you as soon as possible.

Let’s also aim to work in the spirit of Testified Documentation,
which means that:

* New or changed behaviour is documented.
* Code changes are tested.
* And the documentation is testified.

Looking forward to collaborating with you!


### Building locally

1. Create a virtual environment, e.g by
   ```python -m venv .venv```
2. Activate the virtual environment:
   ```source .venv/bin/activate```
3. Install the development-time requirements:
   ```pip install -r requirements.dev.txt```
4. Run the static checks, tests, build the testified documentation
   and the distribution package:
   ```make all```
