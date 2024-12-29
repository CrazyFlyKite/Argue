import webbrowser
from typing import List, Any, Callable

from kivy.uix.screenmanager import SlideTransition
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDIcon, MDLabel
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.widget import MDWidget

from data_manager import data_manager
from dialogs import ask_text_dialog, yes_no_dialog, info_dialog
from translations import get_translation
from utilities import *


class ArgueApp(MDApp):
	def __init__(self, **kwargs) -> None:
		super().__init__(**kwargs)
		data: Any = data_manager.load()
		self.max_length = data.get('max_length')
		self.dialog = MDDialog()
		self.language = data.get('language')
		self.history = data.get('history')
		self.menu = MDDropdownMenu()

	def build(self) -> MDWidget:
		self.theme_cls.primary_palette = PALETTE
		self.theme_cls.theme_style = THEME
		self.update_labels()

		return super().build()

	@property
	def correct(self) -> int:
		return sum(1 for entry in self.history if entry.get('type') == 'correct')

	@property
	def incorrect(self) -> int:
		return sum(1 for entry in self.history if entry.get('type') == 'incorrect')

	def update_labels(self) -> None:
		if (total := self.correct + self.incorrect) > 0:
			self.root.ids.correct_percentage_label.text = f'{self.correct / total:.0%}'
			self.root.ids.incorrect_percentage_label.text = f'{self.incorrect / total:.0%}'
		else:
			self.root.ids.correct_percentage_label.text = '0%'
			self.root.ids.incorrect_percentage_label.text = '0%'

		self.root.ids.correct_label.text = str(self.correct)
		self.root.ids.incorrect_label.text = str(self.incorrect)

	def show_reason_dialog(self, point_type: str) -> None:
		def save() -> None:
			if reason := self.dialog.content_cls.text:
				self.history.append({'type': point_type, 'reason': reason})
				data_manager.write('history', self.history)
				self.update_labels()
				self.dialog.dismiss()

		self.dialog = ask_text_dialog(
			title=self.translate('action_titles/reason_for_point'), hint=self.translate('hints/reason'),
			button_text1=self.translate('buttons/cancel'), button_text2=self.translate('buttons/save'),
			button_color=(0.1, 0.7, 0.2, 1), function=lambda *args: save()
		)
		self.dialog.open()

	def show_history(self) -> None:
		def show_full_reason(r: str) -> None:
			self.dialog = info_dialog(title='Full Reason', text=r, button_text=self.translate('buttons/ok'))
			self.dialog.open()

		history_list = self.root.ids.history_list
		history_list.clear_widgets()

		for index, entry in enumerate(self.history[::-1]):
			item_layout: MDBoxLayout = MDBoxLayout(
				orientation='horizontal',
				spacing=10,
				adaptive_height=True,
				padding=(50, 10)
			)

			item_layout.add_widget(
				MDIcon(
					icon='circle',
					theme_text_color='Custom',
					text_color=COLOR_CORRECT if entry['type'] == 'correct' else COLOR_INCORRECT,
					pos_hint={'y': 0.25}
				)
			)

			reason: str = entry['reason']
			if len(reason) > self.max_length:
				reason = reason[:self.max_length] + '…'

			label: MDLabel = MDLabel(
				text=reason,
				halign='center',
				size_hint_x=0.7,
				font_style='Subtitle1'
			)

			label.bind(
				on_touch_down=lambda instance, touch, r=entry['reason']:
				show_full_reason(r) if instance.collide_point(*touch.pos) else None
			)
			item_layout.add_widget(label)

			# Edit button
			item_layout.add_widget(
				MDIconButton(
					icon='pencil',
					theme_text_color='Custom',
					text_color=COLOR_EDIT,
					on_release=lambda *args, i=len(self.history) - index - 1: self.edit_history_point(i)
				)
			)

			# Delete button
			item_layout.add_widget(
				MDIconButton(
					icon='delete',
					theme_text_color='Custom',
					text_color=COLOR_DELETE,
					on_release=lambda *args, i=len(self.history) - index - 1: self.delete_history_point(i)
				)
			)

			history_list.add_widget(item_layout)

		self.root.transition = SlideTransition(duration=0.3)
		self.root.current = HISTORY_SCREEN

	def edit_history_point(self, index: int) -> None:
		def save_edited_reason() -> None:
			input_text = self.dialog.content_cls.text.strip()

			if input_text.startswith('/max_length '):
				new_max_length = int(input_text.split()[1])
				self.max_length = new_max_length
				data_manager.write('max_length', self.max_length)
				self.dialog.dismiss()
				self.show_history()
				self.dialog = info_dialog(
					title='Command Executed',
					text=f'Maximum length set to {new_max_length} characters.',
					button_text=self.translate('buttons/ok')
				)
				self.dialog.open()
			elif self.dialog.content_cls.text:
				self.history[index]['reason'] = input_text
				data_manager.write('history', self.history)
				self.dialog.dismiss()
				reason: str = self.history[index]['reason']
				if len(reason) > self.max_length:
					reason = reason[:self.max_length] + '…'
				self.root.ids.history_list.children[index].children[2].text = reason

		self.dialog = ask_text_dialog(
			title=self.translate('action_titles/edit_reason'), hint=self.translate('hints/enter_reason'),
			button_text1=self.translate('buttons/cancel'), button_text2=self.translate('buttons/save'),
			button_color=(0.1, 0.7, 0.2, 1), function=lambda *args: save_edited_reason()
		)
		self.dialog.content_cls.text = self.history[index]['reason']
		self.dialog.open()

	def delete_history_point(self, index: int) -> None:
		def delete() -> None:
			del self.history[index]
			data_manager.write('history', self.history)
			self.dialog.dismiss()

			history_list = self.root.ids.history_list
			history_list.remove_widget(history_list.children[index])

		self.dialog = yes_no_dialog(
			title=self.translate('action_titles/confirm_deletion'), description=self.translate('descriptions/delete'),
			button_text1=self.translate('buttons/cancel'), button_text2=self.translate('buttons/delete'),
			button_color=(1, 0, 0, 1), function=lambda *args: delete()
		)
		self.dialog.open()

	def show_info(self) -> None:
		self.root.transition = SlideTransition(duration=0.3)
		self.root.current = INFO_SCREEN

	def open_github(self) -> None:
		def open_github() -> None:
			webbrowser.open(GITHUB_LINK)
			self.dialog.dismiss()

		self.dialog = yes_no_dialog(
			title=self.translate('action_titles/open_github'), description=self.translate('descriptions/open_github'),
			button_text1=self.translate('buttons/cancel'), button_text2=self.translate('buttons/visit'),
			button_color=(0.1, 0.7, 0.2, 1), function=lambda *args: open_github()
		)
		self.dialog.open()

	def clear_history(self) -> None:
		def clear() -> None:
			self.history.clear()
			data_manager.write('history', self.history)
			self.root.ids.history_list.clear_widgets()
			self.dialog.dismiss()

		self.dialog = yes_no_dialog(
			title=self.translate('action_titles/clear_history'),
			description=self.translate('descriptions/clear_history'),
			button_text1=self.translate('buttons/cancel'), button_text2=self.translate('buttons/clear'),
			button_color=(1, 0, 0, 1), function=lambda *args: clear()
		)
		self.dialog.open()

	def go_to_main_screen(self) -> None:
		self.update_labels()
		self.root.transition = SlideTransition(direction='right', duration=0.3)
		self.root.current = MAIN_SCREEN

	def go_to_settings(self) -> None:
		self.root.transition = SlideTransition()
		self.root.current = SETTINGS_SCREEN

	def open_language_menu(self) -> None:
		menu_items: List[Dict[str, str | Callable]] = [
			{'viewclass': 'OneLineListItem', 'text': 'English', 'disabled': self.language == 'en',
			 'on_release': lambda: self.switch_language('en')},
			{'viewclass': 'OneLineListItem', 'text': 'Русский', 'disabled': self.language == 'ru',
			 'on_release': lambda: self.switch_language('ru')},
			{'viewclass': 'OneLineListItem', 'text': 'Українська', 'disabled': self.language == 'ua',
			 'on_release': lambda: self.switch_language('ua')},
			{'viewclass': 'OneLineListItem', 'text': 'Français', 'disabled': self.language == 'fr',
			 'on_release': lambda: self.switch_language('fr')}
		]

		self.menu = MDDropdownMenu(caller=self.root.ids.select_language_button, items=menu_items)
		self.menu.open()

	def switch_language(self, language: str) -> None:
		self.language = language
		data_manager.write('language', language)
		self.root.ids.author.text = self.translate('titles/author')
		self.root.ids.select_language_button.text = self.translate('buttons/select_language')
		self.root.ids.info.text = self.translate('other/info')
		self.root.ids.selected_language_label.text = self.translate('other/selected_language')
		self.root.ids.info_title.text = self.translate('titles/info')
		self.root.ids.settings_title.text = self.translate('titles/settings')
		self.menu.dismiss()

	def translate(self, text_id: str) -> str:
		return get_translation(self.language, text_id)


if __name__ == '__main__':
	ArgueApp().run()
