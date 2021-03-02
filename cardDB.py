from hearthstone.cardxml import load_dbf
from hearthstone.enums import CardClass


_CARD_DATA_CACHE = {}

#pip install hearthstone_data
def card_db():
	if "db" not in _CARD_DATA_CACHE:
		db, _ = load_dbf()
		_CARD_DATA_CACHE["db"] = db
	return _CARD_DATA_CACHE["db"]