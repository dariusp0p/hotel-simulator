class Action:
    def __init__(self, action_type, redo_func, undo_func, *args, **kwargs):
        self.action_type = action_type
        self.redo_func = redo_func
        self.undo_func = undo_func
        self.args = args
        self.kwargs = kwargs

    def undo(self):
        self.undo_func(*self.args, **self.kwargs)

    def redo(self):
        self.redo_func(*self.args, **self.kwargs)
