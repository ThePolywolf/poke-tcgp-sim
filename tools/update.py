from bs4 import BeautifulSoup

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

def scrape_pokemon(html: BeautifulSoup) -> PokemonCard:
    pk = PokemonBuilder()

    card_html = html.find('div', attrs={'class': 'card-profile'})

    img_div = card_html.find('div', attrs={'class': 'card-image'})
    img = img_div.find('img')
    pk.set_img_url(img.attrs['src'])

    card_name_span = card_html.find('span', attrs={'class': 'card-text-name'})
    card_name = card_name_span.get_text()
    pk.set_name(card_name)

    # ex. " - Grass - 50 HP "
    card_type, card_hp = [item.strip() for item in card_name_span.next_sibling.strip().split("-") if len(item) > 0]
    pk.set_pk_type(card_type)
    pk.set_hp(int(card_hp.split(" ")[0]))

    pk.set_stage(card_html.find('p', attrs={'class': 'card-text-type'}).get_text().split("-")[1].strip())

    #TODO abilities and attacks

    card_wrr = card_html.find('p', attrs={'class': 'card-text-wrr'})
    card_weak, card_retreat = [item.strip() for item in card_wrr.get_text().split("<br/>")[0].split("\n") if item != ""]
    pk.set_weakness(card_weak.split(" ")[1])
    pk.set_retreat(int(card_retreat.split(" ")[1]))

    artist_div = card_html.find('div', attrs={'class': 'card-text-artist'})
    pk.set_illustrator(artist_div.find('a').get_text().strip())

    is_ex = card_name[-2:].lower() == "ex"
    if is_ex:
        print(card_html.find('span', attrs={'class': 'ptcg-symbol'}))
        ex_rule = "ex" + card_html.find('span', attrs={'class': 'ptcg-symbol'}).next_sibling.next_sibling.strip().replace("\"", "")
        pk.set_description(ex_rule)
    else:
        desc_div = card_html.find('div', attrs={'class': 'card-text-flavor'})
        pk.set_description(desc_div.get_text().replace("\"", "").strip())

    prints_html = html.find('div', attrs={'class': 'prints-current-details'})
    pack_span, nr_span = prints_html.find_all('span')

    pk.set_pack(pack_span.get_text().split("(")[-1].split(")")[0])

    nr_splits = nr_span.get_text().strip().split(" ")
    number, rarity = nr_splits[0], nr_splits[2]
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