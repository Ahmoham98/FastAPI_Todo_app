from typing import Any
from fastapi_babel import _


def translate(
    message: str,
    **kwargs: Any,
) -> str:
    """
    Translate a message using the active request locale.

    Args:
        message:
            Translation key/message identifier.

        **kwargs:
            Optional values used for message interpolation.

    Returns:
        The translated message.
    """

    translated_message = _(message)

    if kwargs:
        return translated_message.format(**kwargs)

    return translated_message
