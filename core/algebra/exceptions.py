# This Exception is raised when the answer is not a number
# "Any value is a solution" for instance so formatting doesn't
# look like {"answer": {"x1" : "Any value..."}}
class ProblemMessageException(Exception):
    pass

class NoRealRootsException(ProblemMessageException):
    def __str__(self):
        return 'No real roots'


class InvalidFormatException(Exception):
    def __str__(self):
        return 'Invalid format'



class AnyValueIsASolutionException(ProblemMessageException):
    def __str__(self):
        return 'Any value is a solution'

