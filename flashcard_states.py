"""Classes defining the states for the state machine of the flashcards application.

"""
__all__ = ['State', 'MainMenu', 'AddCard', 'Practice', 'End']


class State:
    """General state.

    """
    pass


class MainMenu(State):
    """Main menu, asking the user what to do.

    """
    pass


class AddCard(State):
    """Menu for adding new flashcards.

    """
    pass


class Practice(State):
    """State for practicing the existing flashcards.

    """
    pass


class End(State):
    """State for exiting the application.

    """
    pass
