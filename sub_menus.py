"""Module containing the user menus.

"""
__all__ = ['edit_flashcard_menu', 'learning_menu']

from sqlalchemy.orm.session import Session

from tool import FlashCard


def edit_flashcard_menu(flashcard: FlashCard, db_session: Session) -> None:
    """Display the menu for editing a flashcard.

    :param flashcard: flashcard to be edited
    :param db_session: database session
    """
    while True:
        edit_input = input('press "d" to delete the flashcard:\n'
                           'press "e" to edit the flashcard:')
        if edit_input == 'd':
            db_session.delete(flashcard)
            db_session.commit()
            break
        elif edit_input == 'e':
            _edit_flashcard_menu(flashcard, db_session)
            break
        else:
            print(f'There is no option {edit_input}')


def learning_menu(flashcard: FlashCard, db_session: Session) -> None:
    """

    :param flashcard: current flashcard
    :param db_session: database session
    """
    answer_dict = {'y': True, 'n': False}
    user_input = ''
    while user_input not in ('y', 'n'):
        user_input = input('press "y" if your answer is correct:\n'
                           'press "n" if your answer is wrong:').strip()
        if user_input not in ('y', 'n'):
            print(f'{user_input} is not an option!')
    _update_leitner(flashcard, answer_dict[user_input], db_session)


def _update_leitner(flashcard: FlashCard, answer: bool, db_session: Session) -> None:
    """Update the Leitner box of a flashcard and commit it to the database.

    :param flashcard: flashcard to be updated
    :param answer: answer correct or not
    :param db_session: database session
    """
    min_box = 1
    max_box = 3
    if answer and flashcard.box_number >= max_box:
        db_session.delete(flashcard)
    elif answer and flashcard.box_number < max_box:
        flashcard.box_number += 1
    elif not answer:
        flashcard.box_number = max(min_box, flashcard.box_number - 1)
    db_session.commit()


def _edit_flashcard_menu(flashcard: FlashCard, db_session: Session) -> None:
    """Let the user edit a flashcard and commit it to the database.

    :param flashcard: flashcard to be edited
    :param db_session: database session
    """
    # update the question
    print(f'current question: {flashcard.question}')
    flashcard.question = input('please write a new question:')

    # update the answer
    print(f'current answer: {flashcard.answer}')
    flashcard.answer = input('please write a new answer:')
    db_session.commit()
