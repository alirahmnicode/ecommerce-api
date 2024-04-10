if IN_DOCKER: # type: ignore
    assert MIDDLEWARE[:] == [
        "django.middleware.security.SecurityMiddleware",
    ]