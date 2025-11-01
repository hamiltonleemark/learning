""" Pure virtual interfaces. """
import abc


class Producer(abc.ABC):
    """ All producers must support these methods."""

    @abc.abstractmethod
    def produces(self, item):
        """ Return True if this producer produces this item. """
