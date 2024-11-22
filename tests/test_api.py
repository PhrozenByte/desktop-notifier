import sys
from pathlib import Path

import pytest

from desktop_notifier import (
    DEFAULT_SOUND,
    Attachment,
    Button,
    DesktopNotifier,
    DispatchedNotification,
    Icon,
    Notification,
    ReplyField,
    Sound,
    Urgency,
)


@pytest.mark.asyncio
async def test_request_authorisation(notifier: DesktopNotifier) -> None:
    """
    Authorization should already be grated when setting up the test environment.
    Check that calling request_authorisation returns true.
    """
    if not await notifier.has_authorisation():
        pytest.skip("Not authorised and we cannot request authorisation in test")

    has_authorisation = await notifier.request_authorisation()
    assert has_authorisation


@pytest.mark.asyncio
async def test_send(notifier: DesktopNotifier) -> None:
    dispatched_notification = await notifier.send(
        title="Julius Caesar",
        message="Et tu, Brute?",
        urgency=Urgency.Critical,
        buttons=[
            Button(title="Mark as read", on_pressed=lambda: print("Marked as read"))
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

    current_notifications = (await notifier.get_current_notifications()).values()
    assert len(current_notifications) == 1
    assert dispatched_notification in current_notifications


@pytest.mark.asyncio
async def test_send_twice(notifier: DesktopNotifier) -> None:
    notification = Notification(
        title="Julius Caesar",
        message="Et tu, Brute?",
    )

    n0 = await notifier.send_notification(notification)
    assert isinstance(n0, DispatchedNotification)

    n1 = await notifier.send_notification(notification)
    assert isinstance(n1, DispatchedNotification)

    current_notifications = (await notifier.get_current_notifications()).values()
    assert len(current_notifications) == 2
    assert n0 in current_notifications
    assert n1 in current_notifications


@pytest.mark.asyncio
async def test_resend(notifier: DesktopNotifier) -> None:
    notification = Notification(
        title="Julius Caesar",
        message="Et tu, Brute?",
    )

    n0 = await notifier.send_notification(notification)
    assert isinstance(n0, DispatchedNotification)

    n1 = await notifier.send_notification(n0)
    assert isinstance(n1, DispatchedNotification)

    current_notifications = (await notifier.get_current_notifications()).values()
    assert len(current_notifications) == 1
    assert n0 not in current_notifications
    assert n1 in current_notifications


@pytest.mark.asyncio
async def test_icon_name(notifier: DesktopNotifier) -> None:
    await notifier.send(
        title="Julius Caesar", message="Et tu, Brute?", icon=Icon(name="call-start")
    )


@pytest.mark.asyncio
async def test_icon_path(notifier: DesktopNotifier) -> None:
    await notifier.send(
        title="Julius Caesar", message="Et tu, Brute?", icon=Icon(path=Path("/blue"))
    )


@pytest.mark.asyncio
async def test_icon_uri(notifier: DesktopNotifier) -> None:
    await notifier.send(
        title="Julius Caesar", message="Et tu, Brute?", icon=Icon(uri="file:///blue")
    )


@pytest.mark.asyncio
async def test_sound_name(notifier: DesktopNotifier) -> None:
    await notifier.send(
        title="Julius Caesar", message="Et tu, Brute?", sound=Sound(name="Tink")
    )


@pytest.mark.asyncio
async def test_sound_path(notifier: DesktopNotifier) -> None:
    await notifier.send(
        title="Julius Caesar", message="Et tu, Brute?", sound=Sound(path=Path("/blue"))
    )


@pytest.mark.asyncio
async def test_sound_uri(notifier: DesktopNotifier) -> None:
    await notifier.send(
        title="Julius Caesar", message="Et tu, Brute?", sound=Sound(uri="file:///blue")
    )


@pytest.mark.asyncio
async def test_attachment_path(notifier: DesktopNotifier) -> None:
    await notifier.send(
        title="Julius Caesar",
        message="Et tu, Brute?",
        attachment=Attachment(path=Path("/blue")),
    )


@pytest.mark.asyncio
async def test_attachment_uri(notifier: DesktopNotifier) -> None:
    await notifier.send(
        title="Julius Caesar",
        message="Et tu, Brute?",
        attachment=Attachment(uri="file:///blue"),
    )


@pytest.mark.asyncio
@pytest.mark.skipif(
    sys.platform.startswith("win"),
    reason="Clearing individual notifications is broken on Windows",
)
async def test_clear(notifier: DesktopNotifier) -> None:
    n0 = await notifier.send(
        title="Julius Caesar",
        message="Et tu, Brute?",
    )
    n1 = await notifier.send(
        title="Julius Caesar",
        message="Et tu, Brute?",
    )

    assert isinstance(n0, DispatchedNotification)
    assert isinstance(n0, DispatchedNotification)

    nlist0 = (await notifier.get_current_notifications()).values()
    assert len(nlist0) == 2
    assert n0 in nlist0
    assert n1 in nlist0

    await notifier.clear(n0.identifier)
    nlist1 = (await notifier.get_current_notifications()).values()
    assert len(nlist0) == 1
    assert n0 not in nlist1


@pytest.mark.asyncio
async def test_clear_all(notifier: DesktopNotifier) -> None:
    n0 = await notifier.send(
        title="Julius Caesar",
        message="Et tu, Brute?",
    )
    n1 = await notifier.send(
        title="Julius Caesar",
        message="Et tu, Brute?",
    )

    assert isinstance(n0, DispatchedNotification)
    assert isinstance(n0, DispatchedNotification)

    current_notifications = (await notifier.get_current_notifications()).values()
    assert len(current_notifications) == 2
    assert n0 in current_notifications
    assert n1 in current_notifications

    await notifier.clear_all()
    assert len(await notifier.get_current_notifications()) == 0
