""" Pure virtual interfaces. """
import abc


class Producer(abc.ABC):
    """ All producers must support these methods."""

    @abc.abstractmethod
    def is_source(self):
        """ Return True if the producer is a source. """

    @abc.abstractmethod
    def is_producer(self, item):
        """ Return True if this producer produces this item. """

    @abc.abstractmethod
    def equations(self, outputs, filter_variables=[]):
        """ Return the equations for this producer. """
