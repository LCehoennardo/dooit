from typing import List

from textual import on
from dooit.ui.widgets.switcher import FlexibleSwitcher
from dooit.ui.widgets.trees.todos_tree import TodosTree
from .model_tree import ModelTree
from ..renderers.workspace_renderer import WorkspaceRender


class WorkspacesTree(ModelTree):
    def get_option(self, option_id: str) -> WorkspaceRender:
        option = super().get_option(option_id)
        if not isinstance(option, WorkspaceRender):
            raise ValueError(f"Expected WorkspaceRender, got {type(option)}")

        return option

    def _get_children(self, id: str) -> List[WorkspaceRender]:
        workspace_model = self.get_option(id).model
        return [WorkspaceRender(workspace) for workspace in workspace_model.workspaces]

    def force_refresh(self) -> None:
        self.clear_options()

        for workspace in self.model.workspaces:
            self.add_option(WorkspaceRender(workspace))

    @on(ModelTree.OptionHighlighted)
    def update_todo_tree(self, event: ModelTree.OptionHighlighted):
        if not event.option_id:
            return

        switcher = self.screen.query_one("#todo_switcher", expect_type=FlexibleSwitcher)
        todo_obj = self.get_option(event.option_id).model
        tree = TodosTree(todo_obj)

        if not self.screen.query(f"#{tree.id}"):
            switcher.add_widget(tree)

        switcher.current = tree.id