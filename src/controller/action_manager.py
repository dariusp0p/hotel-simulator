from src.utilities.exceptions import ActionError


class ActionManager:
    """
    Manages undo and redo actions.
    """

    def __init__(self):
        self._undo_stack = []
        self._redo_stack = []

    def do_action(self, action) -> None:
        """Executes a new action and adds it to the undo stack."""
        try:
            action.redo()
            self._undo_stack.append(action)
            self._redo_stack.clear()
        except Exception as e:
            raise ActionError(f"Failed to execute action: {e}")

    def undo(self) -> None:
        """Undoes the last action."""
        if not self._undo_stack:
            raise ActionError("Nothing to undo.")
        action = self._undo_stack.pop()
        action.undo()
        self._redo_stack.append(action)

    def redo(self) -> None:
        """Redoes the last undone action."""
        if not self._redo_stack:
            raise ActionError("Nothing to redo.")
        action = self._redo_stack.pop()
        action.redo()
        self._undo_stack.append(action)

    def can_undo(self) -> bool:
        """Checks if there are actions to undo."""
        return bool(self._undo_stack)

    def can_redo(self) -> bool:
        """Checks if there are actions to redo."""
        return bool(self._redo_stack)

    def clear_stacks(self) -> None:
        """Clears both undo and redo stacks."""
        self._undo_stack.clear()
        self._redo_stack.clear()
