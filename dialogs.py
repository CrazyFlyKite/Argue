from typing import Callable

from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField

from utilities import ColorType


def ask_text_dialog(*, title: str, hint: str, button_text: str, button_color: ColorType,
                    function: Callable) -> MDDialog:
	dialog: MDDialog = MDDialog(
		title=title,
		type='custom',
		content_cls=MDTextField(hint_text=hint),
		buttons=[
			MDRaisedButton(
				text='Cancel',
				on_release=lambda *args: dialog.dismiss(),
				size=('100dp', '40dp'),
			),
			MDRaisedButton(
				text=button_text.capitalize(),
				md_bg_color=button_color,
				on_release=function,
				size=('100dp', '40dp'),
			)
		]
	)

	return dialog


def yes_no_dialog(*, title: str, description: str, button_text: str, button_color: ColorType,
                  function: Callable) -> MDDialog:
	dialog: MDDialog = MDDialog(
		title=title,
		text=description,
		buttons=[
			MDRaisedButton(
				text='Cancel',
				on_release=lambda *args: dialog.dismiss(),
				size=('100dp', '40dp'),
			),
			MDRaisedButton(
				text=button_text.capitalize(),
				md_bg_color=button_color,
				on_release=function,
				size=('100dp', '40dp'),
			)
		]
	)

	return dialog
