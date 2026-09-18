"""Exceptions for the detailed player attribute/rating system.

See player_gen.txt section 15 (Validation and Missing Data): invalid raw
input values and missing-but-required attributes are distinct failure modes
and must be reported clearly rather than silently coerced or zero-filled.
"""


class ValidationError(Exception):
    """A stored attribute value (or a weight table) is invalid."""


class MissingAttributeError(Exception):
    """One or more attributes required by a calculation were not provided.

    Missing is not zero (section 15) - this is raised instead of treating an
    absent attribute as 0.
    """

    def __init__(self, missing_paths):
        self.missing_paths = list(missing_paths)
        super().__init__(f"Missing required attribute(s): {', '.join(self.missing_paths)}")
