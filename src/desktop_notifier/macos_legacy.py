# -*- coding: utf-8 -*-
"""
NSUserNotificationCenter backend for macOS.

* Should be used for macOS 10.13 and earlier.
* Deprecated but still available in macOS 11.0.
* Requires a running CFRunLoop to invoke callbacks.

"""

# system imports
import uuid
import platform
import logging
from typing import Optional

# external imports
from rubicon.objc import NSObject, ObjCClass, objc_method, py_from_ns  # type: ignore
from rubicon.objc.runtime import load_library  # type: ignore

# local imports
from .base import Notification, DesktopNotifierBase


__all__ = ["CocoaNotificationCenterLegacy"]

logger = logging.getLogger(__name__)
macos_version, *_ = platform.mac_ver()

foundation = load_library("Foundation")

NSUserNotification = ObjCClass("NSUserNotification")
NSUserNotificationCenter = ObjCClass("NSUserNotificationCenter")
NSDate = ObjCClass("NSDate")

NSUserNotificationActivationTypeContentsClicked = 1
NSUserNotificationActivationTypeActionButtonClicked = 2
NSUserNotificationActivationTypeAdditionalActionClicked = 4


class NotificationCenterDelegate(NSObject):  # type: ignore
    """Delegate to handle user interactions with notifications"""

    @objc_method
    def userNotificationCenter_didActivateNotification_(
        self, center, notification
    ) -> None:

        internal_nid = py_from_ns(notification.userInfo["internal_nid"])
        notification_info = self.interface.current_notifications[internal_nid]

        if (
            notification.activationType
            == NSUserNotificationActivationTypeContentsClicked
        ):

            if notification_info.action:
                notification_info.action()

        elif (
            notification.activationType
            == NSUserNotificationActivationTypeActionButtonClicked
        ):

            button_title = py_from_ns(notification.actionButtonTitle)
            callback = notification_info.buttons.get(button_title)

            if callback:
                callback()


class CocoaNotificationCenterLegacy(DesktopNotifierBase):
    """NSUserNotificationCenter backend for macOS

    Should be used for macOS High Sierra and earlier. Supports only a single button per
    notification. Both app name and bundle identifier will be ignored. The notification
    center automatically uses the values provided by the app bundle or the Python
    framework.

    :param app_name: The name of the app. Does not have any effect because the app
        name is automatically determined from the bundle or framework.
    :param notification_limit: Maximum number of notifications to keep in the system's
        notification center.
    """

    def __init__(self, app_name: str = "Python", notification_limit: int = 5) -> None:
        super().__init__(app_name, notification_limit)

        self.nc = NSUserNotificationCenter.defaultUserNotificationCenter
        self.nc_delegate = NotificationCenterDelegate.alloc().init()
        self.nc_delegate.interface = self
        self.nc.delegate = self.nc_delegate

    def _send(
        self,
        notification: Notification,
        notification_to_replace: Optional[Notification],
    ) -> str:
        """
        Uses NSUserNotificationCenter to schedule a notification.

        :param notification: Notification to send.
        :param notification_to_replace: Notification to replace, if any.
        """

        if notification_to_replace:
            platform_nid = str(notification_to_replace.identifier)
        else:
            platform_nid = str(uuid.uuid4())

        n = NSUserNotification.alloc().init()
        n.title = notification.title
        n.informativeText = notification.message
        n.identifier = platform_nid
        n.userInfo = {"internal_nid": self.next_nid()}
        n.deliveryDate = NSDate.dateWithTimeInterval(0, sinceDate=NSDate.date())

        if notification.buttons:
            if len(notification.buttons) > 1:
                logger.debug(
                    "NSUserNotificationCenter: only a single button is supported"
                )
            n.hasActionButton = True
            n.actionButtonTitle = list(notification.buttons.keys())[0]

        self.nc.scheduleNotification(n)

        return platform_nid
