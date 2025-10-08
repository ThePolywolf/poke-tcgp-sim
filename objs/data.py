from tools.validation import validate_type

class PokemonCard:
    def __init__(self, name: str, pk_type: str, hp: int, stage: str, weakness: str, retreat: int, pack: str, number: int, rarity: str, img_url: str, illustrator: str, description: str) -> None:
        validate_type(name, str)
        validate_type(pk_type, str)
        validate_type(hp, int)
        validate_type(stage, str)
        validate_type(weakness, str)
        validate_type(retreat, int)
        validate_type(pack, str)
        validate_type(number, int)
        validate_type(rarity, str)
        validate_type(img_url, str)
        validate_type(illustrator, str)
        validate_type(description, str)

        self.name = name
        self.pk_type = pk_type
        self.hp = hp
        self.level = stage
        self.weakness = weakness
        self.retreat = retreat
        self.pack = pack
        self.number = number
        self.rarity = rarity
        self.img_url = img_url
        self.illustrator = illustrator
        self.description = description

    def __str__(self) -> str:
        text = [
            f"{self.name.upper()} | {self.level} | {self.pk_type} - {self.hp} HP",
            f"{self.img_url}",
            f"ATTACKS",
            f"Weakness: {self.weakness}, Retreat: {self.retreat}",
            f"Illustrated by {self.illustrator}",
            f"{self.description}",
            f"Pack {self.pack}, #{self.number} - {self.rarity}",
        ]
        return "\n".join(text)

    def __dict__(self) -> dict[str, str | int]:
        return {
            "name": self.name,
            "pk_type": self.pk_type,
            "hp": self.hp,
            "level": self.level,
            "weakness": self.weakness,
            "retreat": self.retreat,
            "pack": self.pack,
            "number": self.number,
            "rarity": self.rarity,
            "img_url": self.img_url,
            "illustrator": self.illustrator,
            "description": self.description,
        }

    @staticmethod
    def from_dict(data: dict[str, str | int]) -> "PokemonCard":
        return PokemonCard(*[val for _, val in data.items()])

class PokemonBuilder:
    def __init__(self):
        self.__name, self.__pk_type, self.__hp, self.__stage, self.__weakness, self.__retreat, self.__pack, self.__number, self.__rarity, self.__img_url, self.__illustrator, self.__description = [None] * 12

    def set_name(self, name): self.__name = name
    def set_pk_type(self, pk_type): self.__pk_type = pk_type
    def set_hp(self, hp): self.__hp = hp
    def set_stage(self, stage): self.__stage = stage
    def set_weakness(self, weakness): self.__weakness = weakness
    def set_retreat(self, retreat): self.__retreat = retreat
    def set_pack(self, pack): self.__pack = pack
    def set_number(self, number): self.__number = number
    def set_rarity(self, rarity): self.__rarity = rarity
    def set_img_url(self, img_url): self.__img_url = img_url
    def set_illustrator(self, illustrator): self.__illustrator = illustrator
    def set_description(self, description): self.__description = description

    def Build(self) -> PokemonCard:
        parameters = {"name": self.__name, "pk_type": self.__pk_type, "hp": self.__hp, "stage": self.__stage,
                      "weakness": self.__weakness, "retreat": self.__retreat, "pack": self.__pack,
                      "number": self.__number, "rarity": self.__rarity, "img_url": self.__img_url,
                      "illustrator": self.__illustrator, "description": self.__description}
        unassigned = [p for p, val in parameters.items() if val is None]
        if len(unassigned) == 0:
            return PokemonCard(*[val for _, val in parameters.items()])

        raise Exception(f"Pokemon builder has unassigned parameters: {unassigned}")