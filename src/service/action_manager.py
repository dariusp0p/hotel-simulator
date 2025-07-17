from src.service.action import Action
from src.utilities.exceptions import ActionError



class ActionManager:
    def __init__(self):
        self._undo_stack = []
        self._redo_stack = []


    def add_action(self, action: Action):
        self._undo_stack.append(action)


    def undo(self):
        if not self._undo_stack:
            raise ActionError("No more actions to undo!")
        action = self._undo_stack.pop()
        action.undo()
        self._redo_stack.append(action)


    def redo(self):
        if not self._redo_stack:
            raise ActionError("No more actions to redo!")
        action = self._redo_stack.pop()
        action.redo()
        self._undo_stack.append(action)