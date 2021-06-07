"""Application for memorizing flashcards.

"""

from typing import Type, List

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

import flashcard_states as fs
import sub_menus as sm


def main():
    """Entry point of the program.

    """
    db_session = initialize_db('sqlite:///flashcard.db?check_same_thread=False')

    end_loop: bool = False
    state: Type[fs.State] = fs.MainMenu
    while not end_loop:
        if state == fs.MainMenu:
            state = main_menu()
        elif state == fs.AddCard:
            state = add_card(db_session)
        elif state == fs.Practice:
            state = practice(db_session)
        elif state == fs.End:
            state = end(db_session)
            end_loop = True
        else:
            state = fs.End


def main_menu() -> Type[fs.State]:
    """Main menu, lets the user choose what to do next.

    :return: next state
    """
    choice: str = input('1. Add flashcards\n'
                        '2. Practice flashcards\n'
                        '3. Exit\n')
    if choice == '1':
        return fs.AddCard
    elif choice == '2':
        return fs.Practice
    elif choice == '3':
        return fs.End
    else:
        print(f'{choice} is not an option')
        return fs.MainMenu


def add_card(db_session: Session) -> Type[fs.State]:
    """Let user add new flashcards to the database.

    :param db_session: session with the database
    :return: next state
    """
    choice = input('1. Add a new flashcard\n'
                   '2. Exit\n')
    if choice == '1':
        question = ''
        while not question:
            question = input('Question:\n')
        answer = ''
        while not answer:
            answer = input('Answer:\n')
        new_card = FlashCard(question=question, answer=answer)
        store_card_db(new_card, db_session)
        return fs.AddCard
    elif choice == '2':
        return fs.MainMenu
    else:
        print(f'{choice} is not an option\n')
        return fs.AddCard


def practice(db_session: Session) -> Type[fs.State]:
    """Practice the flashcards.

    :param db_session: session with the database
    :return: next state
    """
    # read cards from the database
    flashcards: List[FlashCard] = db_session.query(FlashCard).all()

    if not flashcards:
        print('There is no flashcard to practice!')
        return fs.MainMenu
    else:
        for flashcard in flashcards:
            print(f'Question: {flashcard.question}')
            usr_input = input('press "y" to see the answer:\n'
                              'press "n" to skip:\n'
                              'press "u" to update:')
            if usr_input == 'y':
                print(f'Answer: {flashcard.answer}')
                sm.learning_menu(flashcard, db_session)
            elif usr_input == 'n':
                sm.learning_menu(flashcard, db_session)
                break
            elif usr_input == 'u':
                sm.edit_flashcard_menu(flashcard, db_session)
            else:
                print(f'There is no option {usr_input}')
                break
    return fs.MainMenu


def end(db_session: Session) -> Type[fs.State]:
    """End the application.

    :type db_session: session with the database
    :return: next state
    """
    db_session.close()
    print('Bye!')
    return fs.End


def initialize_db(db_url: str) -> Session:
    """Initialize the database and start a session.

    :param db_url: url of the database
    :return: a session for the specified database
    """
    engine = create_engine(db_url)
    Base.metadata.create_all(engine)

    Session_ = sessionmaker(bind=engine)
    return Session_()


Base = declarative_base()


class FlashCard(Base):
    """Object corresponding to the database table flashcard.

    """
    __tablename__ = 'flashcard'

    id = Column(Integer, primary_key=True)
    question = Column(String(100))
    answer = Column(String(100))
    box_number = Column(Integer, default=1)

    def __str__(self):
        return f'\n' \
               f'Flashcard:\n' \
               f'********\n' \
               f'id:       {self.id}\n' \
               f'question: {self.question}\n' \
               f'answer:   {self.answer}\n'


def store_card_db(new_card: FlashCard, db_session: Session) -> None:
    """Store a flashcard in the database.

    :param new_card: flashcard to be added
    :param db_session: database session
    """
    db_session.add(new_card)
    db_session.commit()


if __name__ == '__main__':
    main()
