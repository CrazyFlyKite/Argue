import logging
from typing import List

from data_manager import translation_manager


def get_translation(language: str, text_id: str) -> str:
	try:
		if '/' in text_id:
			path: List[str] = text_id.split('/')
			translation = translation_manager.load()[language][path[0]][path[1]]
		else:
			translation = translation_manager.load()[language][text_id]

		if isinstance(translation, list):
			return '\n'.join(translation)

		return translation
	except KeyError:
		logging.error(f'The key {text_id} doesn\'t exist in translations')
		exit()
