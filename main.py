import webbrowser

from kivy.properties import ListProperty
from kivy.uix.screenmanager import SlideTransition
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDIcon, MDLabel
from kivymd.uix.widget import MDWidget

from data_manager import data_manager
from dialogs import ask_text_dialog, yes_no_dialog
from utilities import *


class ArgueApp(MDApp):
	info: str = INFO
	history: ListProperty([])
	dialog: MDDialog

	def __init__(self, **kwargs) -> None:
		super().__init__(**kwargs)
		self.history = data_manager.load().get('history', [])

	def build(self) -> MDWidget:
		self.theme_cls.primary_palette = PALETTE
		self.theme_cls.theme_style = THEME
		self.update_labels()

		return super().build()

	@property
	def correct(self) -> int:
		return sum(1 for entry in self.history if entry.get('type') == 'correct')

	@property
	def incorrect(self) -> None:
		return sum(1 for entry in self.history if entry.get('type') == 'incorrect')

	def update_labels(self) -> None:
		if (total := self.correct + self.incorrect) > 0:
			self.root.ids.correct_percentage_label.text = f'{self.correct / total:.0%}'
			self.root.ids.incorrect_percentage_label.text = f'{self.incorrect / total:.0%}'
		else:
			self.root.ids.correct_percentage_label.text = ''
			self.root.ids.incorrect_percentage_label.text = ''

		self.root.ids.correct_label.text = str(self.correct)
		self.root.ids.incorrect_label.text = str(self.incorrect)

	def show_reason_dialog(self, point_type: str) -> None:
		def save() -> None:
			if reason := self.dialog.content_cls.text:
				self.history.append({'type': point_type, 'reason': reason})
				self.update_labels()
				self.dialog.dismiss()

		self.dialog = ask_text_dialog(
			title=f'Reason for {point_type} point', hint='Reason',
			button_text='Save', button_color=(0.1, 0.7, 0.2, 1), function=lambda *args: save()
		)
		self.dialog.open()

		data_manager.write('history', self.history)
		self.update_labels()

	def show_history(self) -> None:
		history_list = self.root.ids.history_list
		history_list.clear_widgets()

		for index, entry in enumerate(self.history[::-1]):
			item_layout: MDBoxLayout = MDBoxLayout(
				orientation='horizontal',
				spacing=10,
				adaptive_height=True,
				padding=(50, 10),
			)

			item_layout.add_widget(
				MDIcon(
					icon='circle',
					theme_text_color='Custom',
					text_color=COLOR_CORRECT if entry['type'] == 'correct' else COLOR_INCORRECT,
					pos_hint={'y': 0.25},
				)
			)

			item_layout.add_widget(
				MDLabel(
					text=entry['reason'],
					halign='center',
					size_hint_x=0.7,
				)
			)

			# Edit button
			item_layout.add_widget(
				MDIconButton(
					icon='pencil',
					theme_text_color='Custom',
					text_color=COLOR_EDIT,
					on_release=lambda *args, i=len(self.history) - index - 1: self.edit_history_point(i),
				)
			)

			# Delete button
			item_layout.add_widget(
				MDIconButton(
					icon='delete',
					theme_text_color='Custom',
					text_color=COLOR_DELETE,
					on_release=lambda *args, i=len(self.history) - index - 1: self.delete_history_point(i),
				)
			)

			history_list.add_widget(item_layout)

		self.root.transition = SlideTransition(duration=0.3)
		self.root.current = HISTORY_SCREEN

	def edit_history_point(self, index: int) -> None:
		self.dialog = ask_text_dialog(
			title='Edit Reason', hint='Enter new reason',
			button_text='Save', button_color=(1, 0, 0, 1), function=lambda *args: self.save_edited_reason(index)
		)
		self.dialog.content_cls.text = self.history[index]['reason']
		self.dialog.open()

	def save_edited_reason(self, index: int) -> None:
		if new_reason := self.dialog.content_cls.text:
			self.history[index]['reason'] = new_reason
			data_manager.write('history', self.history)
			self.dialog.dismiss()
			self.show_history()

	def delete_history_point(self, index: int) -> None:
		def delete(i: int) -> None:
			del self.history[index]
			data_manager.write('history', self.history)
			self.dialog.dismiss()
			self.show_history()

		self.dialog = yes_no_dialog(
			title='Confirm Deletion', description='Are you sure you want to delete this entry?',
			button_text='Delete', button_color=(1, 0, 0, 1), function=lambda *args: delete(index)
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
			title='Open GitHub', description='Are you sure you want to visit the GitHub page of this project?',
			button_text='Yes', button_color=(0.1, 0.7, 0.2, 1),
			function=lambda *args: open_github()
		)
		self.dialog.open()

	def clear_history(self) -> None:
		def clear() -> None:
			self.history.clear()
			data_manager.write('history', self.history)
			self.root.ids.history_list.clear_widgets()
			self.dialog.dismiss()

		self.dialog = yes_no_dialog(
			title='Clear History', description='Are you sure you want to clear the history?',
			button_text='Clear', button_color=(1, 0, 0, 1), function=lambda *args: clear()
		)
		self.dialog.open()

	def go_to_main_screen(self) -> None:
		self.update_labels()
		self.root.transition = SlideTransition(direction='right', duration=0.3)
		self.root.current = MAIN_SCREEN


if __name__ == '__main__':
	ArgueApp().run()
