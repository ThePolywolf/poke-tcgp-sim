from tools import update, webhook
import json

src_url = "https://pocket.limitlesstcg.com"

# page = webhook.get_site_html(src_url + "/cards")
# hooks = update.scrape_set_hooks(page, src_url)
#
# print(hooks[0].display_header())
# for hook in hooks:
#     print(hook)
#
# set_0_pkmn = update.scrape_set_pokemon(hooks[0])
#
# with open("data/pokemon.json", "w", encoding="utf-8") as f:
#     json.dump(set_0_pkmn, f, ensure_ascii=False, indent=4)

pokemon = update.scrape_pokemon(webhook.get_site_html("https://pocket.limitlesstcg.com/cards/A4b/5"))
print(pokemon)