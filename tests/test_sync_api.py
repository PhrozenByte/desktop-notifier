import sys

import pytest

from desktop_notifier import (
    DEFAULT_SOUND,
    Button,
    DesktopNotifierSync,
    DispatchedNotification,
    ReplyField,
    Urgency,
)


def test_send(notifier_sync: DesktopNotifierSync) -> None:
    dispatched_notification = notifier_sync.send(
        title="Julius Caesar",
        message="Et tu, Brute?",
        urgency=Urgency.Critical,
        buttons=[
            Button(
                title="Mark as read",
                on_pressed=lambda: print("Marked as read"),
            )
        ],
        reply_field=ReplyField(
            title="Reply",
            button_title="Send",
            on_replied=lambda text: print("Brutus replied:", text),
        ),
        on_clicked=lambda: print("Notification clicked"),
        on_dismissed=lambda: print("Notification dismissed"),
        sound=DEFAULT_SOUND,
        thread="test_notifications",
        timeout=5,
    )
    assert isinstance(dispatched_notification, DispatchedNotification)
    assert dispatched_notification in notifier_sync.get_current_notifications().values()


@pytest.mark.skipif(
    sys.platform.startswith("win"),
    reason="Clearing individual notifications is broken on Windows",
)
def test_clear(notifier_sync: DesktopNotifierSync) -> None:
    n0 = notifier_sync.send(
        title="Julius Caesar",
        message="Et tu, Brute?",
    )
    n1 = notifier_sync.send(
        title="Julius Caesar",
        message="Et tu, Brute?",
    )

    assert isinstance(n0, DispatchedNotification)
    assert isinstance(n0, DispatchedNotification)

    nlist0 = notifier_sync.get_current_notifications().values()
    assert len(nlist0) == 2
    assert n0 in nlist0
    assert n1 in nlist0

    notifier_sync.clear(n0.identifier)
    nlist1 = notifier_sync.get_current_notifications().values()
    assert len(nlist0) == 1
    assert n0 not in nlist1


def test_clear_all(notifier_sync: DesktopNotifierSync) -> None:
    n0 = notifier_sync.send(
        title="Julius Caesar",
        message="Et tu, Brute?",
    )
    n1 = notifier_sync.send(
        title="Julius Caesar",
        message="Et tu, Brute?",
    )

    assert isinstance(n0, DispatchedNotification)
    assert isinstance(n0, DispatchedNotification)

    current_notifications = notifier_sync.get_current_notifications().values()
    assert len(current_notifications) == 2
    assert n0 in current_notifications
    assert n1 in current_notifications

    notifier_sync.clear_all()
    assert len(notifier_sync.get_current_notifications()) == 0
