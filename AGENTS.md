# Agent Instructions

This project is a CookieCutter template used to generate new python projects. It is extremely dynamic, with many optional settings. Make sure to review the README.md to get more context, as well as the AGENTS.md file in the project template itself (`{{cookiecutter.__package_slug}}/AGENTS.md`).

Since this is a Cookiecutter template you should expect to encounter Jinja2 template blocks in various files.

When being asked to test functionality that requires you to create a new project from the template create them in the `workspaces` directory.

When creating new files for optional services make sure you include them in the post_gen_project.py configuration so that unneeded files are removed. For example, if the caching functionality is not enabled the system should remove all of the caching related files.
