from fastapi import Request
from fastapi.responses import RedirectResponse


def require_login(request: Request):
    """
    Ensures the user is authenticated.

    Returns:
        RedirectResponse -> if user is not logged in
        None             -> if authenticated
    """

    if not request.session.get("logged_in"):

        return RedirectResponse(
            url="/auth/login?error=Please+login+to+continue",
            status_code=303
        )

    return None


def current_user_id(request: Request):
    """
    Returns the logged-in user's ID.
    """

    return request.session.get("user_id")


def current_user_name(request: Request):
    """
    Returns the logged-in user's name.
    """

    return request.session.get("user_name")


def is_logged_in(request: Request):
    """
    Returns True if user is authenticated.
    """

    return request.session.get("logged_in", False)