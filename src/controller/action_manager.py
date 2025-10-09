from src.utilities.exceptions import ActionError



class ActionManager:
    def __init__(self):
        self._undo_stack = []
        self._redo_stack = []

    def do_action(self, action):
        try:
            action.redo()
            self._undo_stack.append(action)
            self._redo_stack.clear()
        except Exception as e:
            raise ActionError(f"Failed to execute action: {e}")

    def undo(self):
        if not self._undo_stack:
            raise ActionError("Nothing to undo.")
        action = self._undo_stack.pop()
        action.undo()
        self._redo_stack.append(action)

    def redo(self):
        if not self._redo_stack:
            raise ActionError("Nothing to redo.")
        action = self._redo_stack.pop()
        action.redo()
        self._undo_stack.append(action)

    def can_undo(self):
        return bool(self._undo_stack)

    def can_redo(self):
        return bool(self._redo_stack)