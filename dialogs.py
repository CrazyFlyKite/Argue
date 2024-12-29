from typing import Callable

from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField

from utilities import ColorType


def ask_text_dialog(*, title: str, hint: str, button_text1: str, button_text2: str, button_color: ColorType,
                    function: Callable) -> MDDialog:
	text_field: MDTextField = MDTextField(hint_text=hint)
	dialog: MDDialog = MDDialog(
		title=title,
		type='custom',
		content_cls=text_field,
		buttons=[
			MDRaisedButton(
				text=button_text1,
				on_release=lambda *args: dialog.dismiss(),
				size=('100dp', '40dp'),
			),
			MDRaisedButton(
				text=button_text2.capitalize(),
				md_bg_color=button_color,
				on_release=function,
				size=('100dp', '40dp'),
			)
		],
		on_open=lambda *args: setattr(text_field, 'focus', True)
	)

	return dialog


def yes_no_dialog(*, title: str, description: str, button_text1: str, button_text2: str, button_color: ColorType,
                  function: Callable) -> MDDialog:
	dialog: MDDialog = MDDialog(
		title=title,
		text=description,
		buttons=[
			MDRaisedButton(
				text=button_text1.capitalize(),
				on_release=lambda *args: dialog.dismiss(),
				size=('100dp', '40dp'),
			),
			MDRaisedButton(
				text=button_text2.capitalize(),
				md_bg_color=button_color,
				on_release=function,
				size=('100dp', '40dp'),
			)
		]
	)

	return dialog


def info_dialog(*, title: str, text: str, button_text: str) -> MDDialog:
	dialog: MDDialog = MDDialog(
		title=title,
		text=text,
		buttons=[
			MDRaisedButton(
				text=button_text,
				on_release=lambda *args: dialog.dismiss(),
				size=('100dp', '40dp'),
			)
		]
	)

	return dialog
