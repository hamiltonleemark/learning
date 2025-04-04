"""
This is the main module for the repository pattern.
"""
import abc
# No code should be inserted in main.py

# pylint: disable=too-few-public-methods
class Repository(abc.ABC):
    """
    This is the abstract base class for the repository pattern.
    """

    @abc.abstractmethod
    def save(self, data: dict) -> None:
        """
        This is the abstract method for the save method.
        """
        return
