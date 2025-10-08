from tools.validation import validate_type, validate_none_or_type

class PokemonCard:
    def __init__(self, name: str, pk_type: str, hp: int, stage: str, pre_evolution: str | None,
                 ability_name: str | None, ability_effect: str | None, atk1_cost: str | None, atk1_name: str,
                 atk1_damage: str, atk1_effect: str | None, atk2_cost: str | None, atk2_name: str | None,
                 atk2_damage: str | None, atk2_effect: str | None, weakness: str, retreat: int, pack: str, number: int,
                 rarity: str, img_url: str, illustrator: str, description: str) -> None:
        validate_type(name, str)
        validate_type(pk_type, str)
        validate_type(hp, int)
        validate_type(stage, str)

        if stage.lower() == "basic": pre_evolution = None
        else: validate_type(pre_evolution, str)
        if ability_name is None:
            ability_effect = None
        else:
            validate_type(ability_name, str)
            validate_type(ability_effect, str)
        validate_none_or_type(atk1_cost, str)
        validate_type(atk1_name, str)
        validate_type(atk1_damage, str)
        validate_none_or_type(atk1_effect, str)
        if not atk2_name is None:
            validate_none_or_type(atk2_cost, str)
            validate_type(atk2_name, str)
            validate_type(atk2_damage, str)
            validate_none_or_type(atk2_effect, str)
        else:
            atk2_cost = None
            atk2_name = None
            atk2_damage = None
            atk2_effect = None
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
        self.stage = stage
        self.pre_evolution = pre_evolution
        self.ability_name = ability_name
        self.ability_effect = ability_effect
        self.atk1_cost = atk1_cost
        self.atk1_name = atk1_name
        self.atk1_damage = atk1_damage
        self.atk1_effect = atk1_effect
        self.atk2_cost = atk2_cost
        self.atk2_name = atk2_name
        self.atk2_damage = atk2_damage
        self.atk2_effect = atk2_effect
        self.weakness = weakness
        self.retreat = retreat
        self.pack = pack
        self.number = number
        self.rarity = rarity
        self.img_url = img_url
        self.illustrator = illustrator
        self.description = description

    def has_ability(self):
        return self.ability_name is not None

    def get_ability(self) -> tuple[str, str]:
        return self.ability_name, self.ability_effect

    def __str__(self) -> str:
        text = [
            f"{self.name.upper()} | {self.pk_type} - {self.hp} HP",
            f"{self.stage} {"" if self.stage.lower() == "basic" else f"| Evolves from {self.pre_evolution}"}",
            f"{self.img_url}",
        ]

        if self.has_ability():
            text += [
                f"   Ability: {self.ability_name}",
                f"   {self.ability_effect}"
            ]

        for cost, name, damage, effect in [(self.atk1_cost, self.atk1_name, self.atk1_damage, self.atk1_effect), (self.atk2_cost, self.atk2_name, self.atk2_damage, self.atk2_effect)]:
            if name is None:
                continue
            text += [f"   {("Free" if cost is None else cost):<7} {name:<20} {damage:>5}"]
            if effect is not None: text += [f"   {effect}"]

        text += [
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
            "stage": self.stage,
            "pre_evolution": self.pre_evolution,
            "ability_name": self.ability_name,
            "ability_effect": self.ability_effect,
            "atk1_cost": self.atk1_cost,
            "atk1_name": self.atk1_name,
            "atk1_damage": self.atk1_damage,
            "atk1_effect": self.atk1_effect,
            "atk2_cost": self.atk2_cost,
            "atk2_name": self.atk2_name,
            "atk2_damage": self.atk2_damage,
            "atk2_effect": self.atk2_effect,
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
        (self.__name, self.__pk_type, self.__hp, self.__stage, self.__pre_evolution, self.__ability_name,
         self.__ability_effect, self.__atk1_cost, self.__atk1_name, self.__atk1_damage, self.__atk1_effect,
         self.__atk2_cost, self.__atk2_name, self.__atk2_damage, self.__atk2_effect,  self.__weakness, self.__retreat,
         self.__pack, self.__number, self.__rarity, self.__img_url, self.__illustrator, self.__description) = [None] * 23

    def set_name(self, name) -> None:           self.__name = name
    def set_pk_type(self, pk_type) -> None:     self.__pk_type = pk_type
    def set_hp(self, hp) -> None:               self.__hp = hp
    def set_stage(self, stage) -> None:         self.__stage = stage
    def set_pre_evolution(self, pre_evolution) -> None:     self.__pre_evolution = pre_evolution
    def set_ability_name(self, ability_name) -> None:       self.__ability_name = ability_name
    def set_ability_effect(self, ability_effect) -> None:   self.__ability_effect = ability_effect
    def set_attack_1(self, cost, name, damage, effect) -> None:
        self.__atk1_cost = cost
        self.__atk1_name = name
        self.__atk1_damage = damage
        self.__atk1_effect = effect
    def set_attack_2(self, cost, name, damage, effect) -> None:
        self.__atk2_cost = cost
        self.__atk2_name = name
        self.__atk2_damage = damage
        self.__atk2_effect = effect
    def set_weakness(self, weakness) -> None:   self.__weakness = weakness
    def set_retreat(self, retreat) -> None:     self.__retreat = retreat
    def set_pack(self, pack) -> None:           self.__pack = pack
    def set_number(self, number) -> None:       self.__number = number
    def set_rarity(self, rarity) -> None:       self.__rarity = rarity
    def set_img_url(self, img_url) -> None:     self.__img_url = img_url
    def set_illustrator(self, illustrator) -> None: self.__illustrator = illustrator
    def set_description(self, description) -> None: self.__description = description

    def Build(self) -> PokemonCard:
        parameters = (self.__name, self.__pk_type, self.__hp, self.__stage, self.__pre_evolution, self.__ability_name,
         self.__ability_effect, self.__atk1_cost, self.__atk1_name, self.__atk1_damage, self.__atk1_effect,
         self.__atk2_cost, self.__atk2_name, self.__atk2_damage, self.__atk2_effect,  self.__weakness, self.__retreat,
         self.__pack, self.__number, self.__rarity, self.__img_url, self.__illustrator, self.__description)
        return PokemonCard(*parameters)