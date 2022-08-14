from aiogram.dispatcher.filters.state import StatesGroup, State


class SelectTextTypeStatesGroup(StatesGroup):
    select_type_state = State()
