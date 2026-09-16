# Product Requirements Document: Django 2.2 to 5.2 Migration

## 1. Introduction/Overview

This document outlines the requirements for migrating the existing Django application from version 2.2 to 5.2. The primary driver for this migration is to enhance security, ensure long-term maintainability, and modernize the technology stack. The project involves refactoring and moving the legacy codebase from the `/bireme` directory to the new `/app` directory, which will house the updated Django 5.2 application.

## 2. Goals

*   Upgrade the Django framework from version 2.2 to 5.2.
*   Update all project dependencies to versions compatible with Django 5.2.
*   Refactor the existing codebase to be compatible with the new Django version and its best practices.
*   Ensure the application's functionality remains identical to the legacy version.
*   Maintain the existing database schema and user interface.
*   Isolate the new application code in the `/app` directory, while the legacy code remains in `/bireme` for reference during the migration.

## 3. User Stories

*   As a developer, I want to work with a modern and secure codebase to ensure the long-term stability of the application.
*   As a user, I want to be able to use the application without any change in functionality or user experience after the migration.
*   As an administrator, I want to manage users (Create, Read, Update, Delete) in the same way as in the legacy application.

## 4. Functional Requirements

1.  The application must be upgraded to Django 5.2.
2.  All dependencies listed in `requirements.txt` must be updated to their latest versions compatible with Django 5.2.
3.  The legacy code from the `/bireme` directory must be refactored and moved to the `/app` directory.
4.  All existing features, including the Users CRUD, must be fully functional after the migration.
5.  The application must connect to the existing database and use the current schema without any modifications.
6.  The user interface and user experience must remain unchanged.
7.  The new application must be runnable from the `/app` directory.

## 5. Non-Goals (Out of Scope)

*   No new features will be added during this migration.
*   The database schema will not be altered.
*   The user interface will not be redesigned.
*   The legacy application in `/bireme` will not be maintained after the migration is complete.

## 6. Design Considerations

The existing UI/UX must be preserved. All templates and static files should be migrated and rendered correctly in the new application.

## 7. Technical Considerations

*   The project uses `mysqlclient`. The updated version must be compatible with Django 5.2 and the existing database.
*   The `django-tastypie` library is used. It needs to be checked for compatibility with Django 5.2. If it's not compatible, a modern alternative like Django REST Framework should be considered, but the functionality must remain the same.
*   The `django-rosetta` library needs to be checked for compatibility.
*   The project structure will be changed. The new application will live in `/app`, and the legacy code in `/bireme` will be used as a reference.
*   URL routing, middleware, and settings will need to be updated to comply with Django 5.2 conventions.

## 8. Success Metrics

*   The application runs successfully on Django 5.2.
*   All automated tests (if any) pass.
*   Manual testing confirms that all features of the legacy application are working as expected in the new version.
*   The Users CRUD functionality is fully operational.
*   The application is demonstrably more secure and easier to maintain.

## 9. Open Questions

*   Are there any existing automated tests for the legacy application? If so, where are they located?
*   What is the current test coverage of the application?
