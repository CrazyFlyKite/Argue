import logging
import webbrowser
from typing import List

from kivy.core.text import LabelBase
from kivy.uix.screenmanager import SlideTransition
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDIcon, MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.widget import MDWidget

from data_manager import data_manager
from utilities import *


class ArgueApp(MDApp):
	correct: int = 0
	incorrect: int = 0
	info: str = INFO
	history: List[PointInfo]
	dialog: MDDialog
	correct_percentage: int = 0
	incorrect_percentage: int = 0

	def build(self) -> MDWidget:
		self.theme_cls.primary_palette = PALETTE
		self.theme_cls.theme_style = THEME

		LabelBase.register(name='JetBrainsMono', fn_regular='JetBrainsMono.ttf')

		data = data_manager.load()
		self.correct = data.get('correct')
		self.incorrect = data.get('incorrect')
		self.history = data.get('history')

		self.update_labels()
		self.update_percentages()

		return super().build()

	def increase_correct(self) -> None:
		if self.correct < MAX_COUNT:
			self.correct += 1
			self.update_labels()
			data_manager.write('correct', self.correct)

	def decrease_correct(self) -> None:
		if self.correct > MIN_COUNT:
			self.correct -= 1
			self.update_labels()
			data_manager.write('correct', self.correct)

	def increase_incorrect(self) -> None:
		if self.incorrect < MAX_COUNT:
			self.incorrect += 1
			self.update_labels()
			data_manager.write('incorrect', self.incorrect)

	def decrease_incorrect(self) -> None:
		if self.incorrect > MIN_COUNT:
			self.incorrect -= 1
			self.update_labels()
			data_manager.write('incorrect', self.incorrect)

	def update_labels(self) -> None:
		self.update_percentages()
		self.root.ids.correct_label.text = str(self.correct)
		self.root.ids.incorrect_label.text = str(self.incorrect)

	def update_percentages(self):
		total: int = self.correct + self.incorrect
		if total > 0:
			self.root.ids.correct_percentage_label.text = f'{self.correct / total:.0%}'
			self.root.ids.incorrect_percentage_label.text = f'{self.incorrect / total:.0%}'
		else:
			self.root.ids.correct_percentage_label.text = ''
			self.root.ids.incorrect_percentage_label.text = ''

	def show_reason_dialog(self, point_type: str) -> None:
		self.dialog = MDDialog(
			title=f'Reason for {point_type} point',
			type='custom',
			content_cls=MDTextField(hint_text='Enter the reason'),
			buttons=[
				MDRaisedButton(
					text='Cancel',
					on_release=lambda *args: self.dialog.dismiss(),
					size=('100dp', '40dp'),
				),
				MDRaisedButton(
					text='Save',
					on_release=lambda *args: self.save_reason(point_type),
					size=('100dp', '40dp'),
				),
			],
		)
		self.dialog.open()

	def save_reason(self, point_type: str) -> None:
		if reason := self.dialog.content_cls.text:
			self.history.append({'type': point_type, 'reason': reason})
			self.dialog.dismiss()

			if point_type == 'correct':
				self.increase_correct()
			elif point_type == 'incorrect':
				self.increase_incorrect()

		data_manager.write('history', self.history)

	def show_history(self) -> None:
		history_list = self.root.ids.history_list
		history_list.clear_widgets()

		for index, entry in enumerate(reversed(self.history)):
			item_layout = MDBoxLayout(
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
					on_release=lambda *args, i=index: self.edit_history_point(i),
				)
			)

			# Delete button
			item_layout.add_widget(
				MDIconButton(
					icon='delete',
					theme_text_color='Custom',
					text_color=COLOR_DELETE,
					on_release=lambda *args, i=index: self.delete_history_point(i),
				)
			)

			history_list.add_widget(item_layout)

		self.root.transition = SlideTransition(duration=0.3)
		self.root.current = HISTORY_SCREEN

	def edit_history_point(self, index: int) -> None:
		self.dialog = MDDialog(
			title='Edit Reason',
			type='custom',
			content_cls=MDTextField(hint_text='Enter new reason'),
			buttons=[
				MDRaisedButton(
					text='Cancel',
					on_release=lambda *args: self.dialog.dismiss(),
					size=('100dp', '40dp'),
				),
				MDRaisedButton(
					text='Save',
					on_release=lambda *args: self.save_edited_reason(index),
					size=('100dp', '40dp'),
				),
			],
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
		self.dialog = MDDialog(
			title='Confirm Deletion',
			text='Are you sure you want to delete this entry?',
			size_hint=(0.8, 0.3),
			buttons=[
				MDRaisedButton(
					text='Cancel',
					on_release=lambda *args: self.dialog.dismiss(),
					size=('100dp', '40dp'),
				),
				MDRaisedButton(
					text='Delete',
					on_release=lambda *args: self.confirm_delete(index),
					size=('100dp', '40dp'),
				),
			]
		)
		self.dialog.open()

	def confirm_delete(self, index: int) -> None:
		if self.history[index].get('type') == 'correct':
			self.decrease_correct()
		else:
			self.decrease_incorrect()

		del self.history[index]
		data_manager.write('history', self.history)
		self.dialog.dismiss()
		self.show_history()

	def show_info(self) -> None:
		self.root.transition = SlideTransition(duration=0.3)
		self.root.current = INFO_SCREEN

	def open_github(self) -> None:
		webbrowser.open('https://github.com/CrazyFlyKite?tab=repositories')

	def delete_history(self):
		def delete_history():
			self.history.clear()
			self.root.ids.history_list.clear_widgets()
			self.correct = 0
			self.incorrect = 0
			self.update_labels()
			dialog.dismiss()
			data_manager.write('history', self.history)
			data_manager.write('correct', 0)
			data_manager.write('incorrect', 0)

		dialog: MDDialog = MDDialog(
			title='Delete History',
			text='Are you sure you want to delete the history?',
			size_hint=(0.8, None),
			height='200dp',
			buttons=[
				MDRaisedButton(
					text='No',
					on_release=lambda x: dialog.dismiss()
				),
				MDRaisedButton(
					text='Yes',
					on_release=lambda *args: delete_history()
				),
			]
		)
		dialog.open()

	def go_to_main_screen(self) -> None:
		self.root.transition = SlideTransition(direction='right', duration=0.3)
		self.root.current = MAIN_SCREEN


if __name__ == '__main__':
	try:
		ArgueApp().run()
	except KeyboardInterrupt:
		logging.debug('Exiting the app…')
