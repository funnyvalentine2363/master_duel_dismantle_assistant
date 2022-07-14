import difflib


class CardInfo:
    def __init__(self, rarity, deck_used, deck_info):
        self.rarity = rarity
        self.deck_used = deck_used
        self.deck_info = deck_info

    def __str__(self):
        res = f"Rarity {self.rarity}\n"
        for deck in self.deck_used:
            numbers = self.deck_info[deck]
            res += f"{deck}\t{numbers}\n"

        return res

    def valid(self):
        return self.rarity is not None


class CardInfoDB:
    def __init__(self):
        self.names = []
        self.info = {}

    def insert(self, name: str, ci: CardInfo):
        self.info[name] = ci
        self.names.append(name)

    def search(self, name: str):
        name = name.lower()
        name_matches = difflib.get_close_matches(
            name, self.names, n=1, cutoff=0)

        if(len(name_matches) > 0):
            name = name_matches[0]
            return name, self.info[name]
        else:
            return None, None


class CardInfoDBGroup:
    def __init__(self, dbs: [CardInfo]):
        self.dbs = dbs
        return

    def search(self, name: str, mask: [bool]):
        return [db.search(name) for (db, mask) in zip(self.dbs, mask) if mask]
