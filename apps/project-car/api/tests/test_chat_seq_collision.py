from types import SimpleNamespace

from sqlalchemy.exc import IntegrityError

from app.services.chat import _is_seq_collision


class FakePgError(Exception):
    def __init__(self, constraint_name):
        super().__init__("duplicate key")
        self.diag = SimpleNamespace(constraint_name=constraint_name)


def test_seq_collision_true_for_pg_constraint_and_sqlite_text():
    assert _is_seq_collision(IntegrityError("INSERT", {}, FakePgError("ix_chat_messages_room_seq"))) is True
    sqlite = Exception("UNIQUE constraint failed: chat_messages.room_id, chat_messages.seq")
    assert _is_seq_collision(IntegrityError("INSERT", {}, sqlite)) is True


def test_seq_collision_false_for_unrelated_constraint():
    assert _is_seq_collision(IntegrityError("INSERT", {}, FakePgError("ix_other_constraint"))) is False
    assert _is_seq_collision(IntegrityError("INSERT", {}, Exception("UNIQUE constraint failed: users.email"))) is False
