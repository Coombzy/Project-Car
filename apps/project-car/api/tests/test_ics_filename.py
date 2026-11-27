import unittest
from uuid import UUID

from app.services.ics import ics_filename


class TestIcsFilename(unittest.TestCase):
    def test_todo_uuid_becomes_project_car_todo_ics_name(self) -> None:
        todo_id = UUID("aaaaaaaa-bbbb-4ccc-8ddd-eeeeeeeeeeee")
        self.assertEqual(
            ics_filename(todo_id),
            "project-car-todo-aaaaaaaa-bbbb-4ccc-8ddd-eeeeeeeeeeee.ics",
        )

    def test_nil_uuid_keeps_full_hyphenated_text(self) -> None:
        self.assertEqual(
            ics_filename(UUID(int=0)),
            "project-car-todo-00000000-0000-0000-0000-000000000000.ics",
        )

    def test_name_is_prefix_uuid_text_and_ics_suffix(self) -> None:
        todo_id = UUID("08f7c1be-2d3e-4a5b-8c6d-7e8f9a0b1c2d")
        name = ics_filename(todo_id)
        self.assertTrue(name.startswith("project-car-todo-"))
        self.assertTrue(name.endswith(".ics"))
        self.assertEqual(name, f"project-car-todo-{todo_id}.ics")
