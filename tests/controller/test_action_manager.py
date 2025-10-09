from src.controller.action_manager import ActionManager


class DummyAction:
    def __init__(self):
        self.done = False
        self.undone = False
    def redo(self):
        self.done = True
    def undo(self):
        self.undone = True

def test_do_action_and_undo_redo():
    manager = ActionManager()
    action = DummyAction()
    manager.do_action(action)
    assert action.done
    assert manager.can_undo()
    manager.undo()
    assert action.undone
    assert manager.can_redo()
    manager.redo()
    assert action.done

def test_clear_stacks():
    manager = ActionManager()
    action = DummyAction()
    manager.do_action(action)
    manager.clear_stacks()
    assert not manager.can_undo()
    assert not manager.can_redo()
