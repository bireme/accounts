# Coding pattern preferences

- Always prefer simple solutions
- Avoid duplication of code whenever possible, which means checking for other areas of the codebase that might already have similar code and functionality
- You are careful to only make changes that are requested or you are confident are well understood and related to the change being requested
- When fixing an issue or bug, do not introduce a new pattern or technology without first exhausting all options for the existing implementation. And - if you
  finally do this, make sure to remove the old implementation afterwards so we don’t have duplicate logic
- Avoid having files over 300 lines of code. Refactor at that point.
- Never overwrite my .env file without asking and confirming

# General Code Style & Formatting

- Use English for all code and documentation.
- Use PascalCase for classes.
- Use snake_case for variables, functions, and methods.
- Use kebab-case for directory names.
- Use UPPERCASE for environment variables.
- Avoid magic numbers and define constants.

# Python and Django Code Style

- Use Django's built-in features and tools wherever possible to leverage its full capabilities.
- Prioritize readability and maintainability; follow Django's coding style guide (PEP 8 compliance).
- Leverage Django’s ORM for database interactions; avoid raw SQL queries unless necessary for performance.


# Techinical stack

- Django 5.2
- Python 3.12
- uv for package management


## Libraries documentation and examples

- Always use the Context7 MCP server to reference documentation for all libraries used in the project
- For the tokens, start with 5000, but increase to 20000 if your first search didn’t give relevant documents
- Only search 3 times maximum for any specific documentation. If you don’t get what you need use web search to perform the search
