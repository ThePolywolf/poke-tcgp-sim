from bs4 import BeautifulSoup, Tag

from objs.web_struct import SetHook
from objs.data import PokemonCard, PokemonBuilder

from tools.webhook import get_site_html

def scrape_set_hooks(page, page_url) -> list[SetHook]:
    """
    Scrapes the webpage for set hooks
    :param page: webpage to scrape (html)
    :param page_url: url of the webpage, used to build a complete reference for href links
    :return: All set hooks found | Raises exception if no hooks found
    """
    all_rows = page.find_all("tr")
    rows = [row for row in all_rows if sum([1 if td.find('a') is not None else 0 for td in row.find_all("td")]) == 3]

    if len(rows) == 0:
        raise Exception(f"No set hooks found for {page_url}")

    hooks: list[SetHook] = []
    for row in rows:
        data, _, count_data = [data.find('a') for data in row.find_all("td")]

        code = data.find('img').attrs['alt']
        name = data.find('span').next_sibling.strip().title()
        url = page_url + data['href']
        card_count = int(count_data.get_text())
        hook = SetHook(name, code, url, card_count)

        hooks.append(hook)

    return hooks

def scrape_attack(html: Tag) -> tuple[str, str, str, str]:
    info = html.find('p', {'class': 'card-text-attack-info'}).get_text().strip()
    effect = html.find('p', {'class': 'card-text-attack-effect'}).get_text().strip()

    info_splits = info.split(" ")
    cost = info_splits[0].replace("\n", "")
    damage = info_splits[-1]
    name = " ".join([item for item in info_splits[1:-1] if item != ""])

    cost = None if cost == '' else cost
    effect = None if effect == '' else effect

    return cost, name, damage, effect

def scrape_pokemon(html: BeautifulSoup) -> PokemonCard:
    pk = PokemonBuilder()

    card_profile = html.find('div', {'class': 'card-profile'})

    card_image = card_profile.find('img')['src']
    pk.set_img_url(card_image)

    header_text, attack_text, footer_text, illus_text, desc_text = card_profile.find_all('div', attrs={'class': 'card-text-section'})

    # header: name, pk_type, hp, card_type, stage, pre_evo
    card_name_text = header_text.find('span', {'class': 'card-text-name'})
    card_name = card_name_text.find('a').get_text()
    pk.set_name(card_name)
    type_hp_split = [item.strip() for item in card_name_text.next_sibling.strip().split("-") if item != ""]
    pk_type, hp = type_hp_split
    pk.set_pk_type(pk_type)
    pk.set_hp(int(hp.split(" ")[0]))

    card_type = header_text.find('p', {'class': 'card-text-type'})
    card_type_splits = [item.strip() for item in card_type.get_text().split("-") if item != ""]

    # card_type = card_type_splits[0]
    stage = card_type_splits[1]
    pk.set_stage(stage)

    if stage.lower() != 'basic':
        pk.set_pre_evolution(card_type_splits[2].split("\n")[1].strip())

    ability = attack_text.find('div', {'class': 'card-text-ability'})
    if ability is not None:
        pk.set_ability_name(ability.find('p', {'class': 'card-text-ability-info'}).get_text().replace("\n", "").strip()[9:].strip())
        pk.set_ability_effect(ability.find('p', {'class': 'card-text-ability-effect'}).get_text().strip())

    attacks = attack_text.find_all('div', {'class': 'card-text-attack'})
    atk_number = 0
    for attack in attacks:
        atk_number += 1
        if atk_number == 1:
            pk.set_attack_1(*scrape_attack(attack))
        elif atk_number == 2:
            pk.set_attack_2(*scrape_attack(attack))
        else:
            raise Exception(f"Unable to process more than two attacks")

    # footer: weakness, retreat
    weakness_text, retreat_text = [item.strip() for item in footer_text.get_text().split("\n") if item != ""]
    pk.set_weakness(weakness_text.split(" ")[1])
    pk.set_retreat(int(retreat_text.split(" ")[1]))

    # ex changes position of bottom text and illustrator
    is_ex = card_name[-2:].lower() == "ex"
    if is_ex:
        desc_text, illus_text = illus_text, desc_text

    # illustrator
    illustrator = illus_text.find('a').get_text().strip()
    pk.set_illustrator(illustrator)

    desc = desc_text.get_text().strip()
    pk.set_description(desc)

    card_prints = html.find('div', {'class': 'card-prints'})

    pack_text, nr_text = card_prints.find('div', {'class': 'prints-current-details'}).find_all('span')
    pk.set_pack(pack_text.get_text().strip())
    nr_text = nr_text.get_text().strip().split(" ")
    nr_text.pop(1)
    number, rarity = nr_text[0], nr_text[1]
    pk.set_number(int(number[1:]))
    pk.set_rarity(rarity)

    return pk.Build()

def scrape_set_pokemon(set_hook: SetHook) -> list[PokemonCard]:
    cards = []
    for i in range(set_hook.cards):
        card_html = get_site_html(f"{set_hook.url}/{i + 1}")
        card = scrape_pokemon(card_html)
        cards.append(card)
        print(str(card) + "\n")

    return cards