# python lists - 
  Lists are "mutable", meaning they can be modified "in place".
  indexing and slicing : list[n] or list[0:n] or list[n:]
  list functions:
    len(list)
    sorted(list)
    sum(int list)
    max(list)
  The things an object carries around can also include functions. A function attached to an object is called a method. (Non-function things attached to an object,     such as imag, are called attributes).
    x.bit_length()
    list.append modifies a list by adding an item to the end: planets.append('Pluto')
    list.index() returns index #
  Tuples
    Tuples are almost exactly the same as lists. They differ in just two ways.
      1: The syntax for creating them uses parentheses instead of square brackets
      2: They cannot be modified (they are immutable).
    Tuples are often used for functions that have multiple return values.  For example, the as_integer_ratio() method of float objects returns a numerator and a         denominator in the form of a tuple:

# examples #
def select_second(L):
    """Return the second element of the given list. If the list has no second
    element, return None.
    """
    if len(L) < 2:
        return None
    return L[1]

def losing_team_captain(teams):
    """Given a list of teams, where each team is a list of names, return the 2nd player (captain)
    from the last listed team
    """
    return teams[-1][1]
    
