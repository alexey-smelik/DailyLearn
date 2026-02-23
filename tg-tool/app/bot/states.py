from aiogram.fsm.state import State, StatesGroup


class ConspectStates(StatesGroup):
    waiting = State()
