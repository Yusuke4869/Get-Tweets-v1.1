import yaml

class Settings:

    def __init__(self) -> None:
        self.set()

    def set(self) -> None:
        with open("settings.yaml", "r", encoding="utf-8") as f:
            self.data = yaml.safe_load(f)
        self.generate_searchword()

    def generate_searchword(self) -> None:
        account_ids = self.data["search"]["account_ids"]
        and_words = self.data["search"]["and_words"]
        or_words = self.data["search"]["or_words"]
        ignore_words = self.data["search"]["ignore_words"]

        # Noneの削除
        account_ids = [value for value in account_ids if value]
        and_words = [value for value in and_words if value]
        or_words = [value for value in or_words if value]
        ignore_words = [value for value in ignore_words if value]

        account_ids = [f'from:{account_id}' for account_id in account_ids]
        and_words = [f'"{and_word}"' for and_word in and_words]
        or_words = [f'"{or_word}"' for or_word in or_words]
        ignore_words = [f'-"{ignore_word}"' for ignore_word in ignore_words]

        serchword_list = []

        if len(account_ids) > 0:
            serchword_list.append(f'({" OR ".join(account_ids)})')

        if len(and_words) > 0:
            serchword_list.append(" ".join(and_words))

        if len(or_words) > 0:
            serchword_list.append(f'({" OR ".join(or_words)})')

        if len(ignore_words) > 0:
            serchword_list.append(" ".join(ignore_words))

        self.SearchWord = " ".join(serchword_list)

    def get_searchword(self) -> str:
        return self.SearchWord

    def sending_to_line(self) -> bool:
        return self.data["sending"]["line"]

    def sending_to_discord(self) -> bool:
        return self.data["sending"]["discord"]

    def get_db_names(self) -> dict:
        names = {}
        names["database_name"] = self.data["database"]["database_name"]
        names["collection_name"] = self.data["database"]["collection_name"]
        return names

    def get_db_program_name(self) -> str:
        return self.data["database"]["program_name"]

    def get_interval(self) -> int:
        interval = self.data["control"]["interval"]
        try:
            return int(interval)
        except ValueError:
            return 5

    def set_interval(self, interval) -> None:
        try:
            interval = int(interval)
        except ValueError:
            return

        self.data["control"]["interval"] = interval

settings = Settings()