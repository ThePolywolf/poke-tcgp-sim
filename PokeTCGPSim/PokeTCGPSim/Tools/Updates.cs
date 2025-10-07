namespace PokeTCGPSim.Tools;

public static class Updates
{
    public struct SetSource
    {
        public string name;
        public string code;
        public string url;
        public int cards;
    }

    public struct PokemonSource
    {
        public string name;
        public string type;
        public int hp;
    }
    
    private const string SetUrl = "https://pocket.limitlesstcg.com";

    /// <summary>
    /// Attempts to find the start and end indexes of the first element of the given type
    /// </summary>
    /// <param name="element">HTML element to find, using angle brackets</param>
    /// <param name="html">html to search for element</param>
    /// <param name="start">start index of the element</param>
    /// <param name="end">end index of the element</param>
    /// <returns>True iff the element was found in the given html</returns>
    private static bool FindElement(string element, string html, out int start, out int end)
    {
        if (!html.Contains($"<{element}"))
        {
            start = 0;
            end = 0;
            return false;
        }

        start = html.IndexOf($"<{element}");
        end = html.IndexOf($"</{element}>");
        return true;
    }

    /// <summary>
    /// Returns the starting index of the property in the html. Assumes html contains the property
    /// </summary>
    /// <param name="prop">property to find using =</param>
    /// <param name="html">html to search for property</param>
    /// <returns>index after the property declaration</returns>
    private static int FindPropertyIndex(string prop, string html)
    {
        var propStr = $"{prop}=";
        return html.IndexOf(propStr) + propStr.Length;
    }

    private static int FindClassInstance(string htmlClass, string html)
    {
        var clsStr = $"class=\"{htmlClass}";
        return html.IndexOf(clsStr) + clsStr.Length;
    }

    /// <summary>
    /// Finds all set sources from the set webpage
    /// </summary>
    /// <returns>A list of all set sources</returns>
    public static List<SetSource>? GetSets()
    {
        using var client = new HttpClient();

        var response = client.GetAsync(SetUrl + "/cards").Result;
        if (!response.IsSuccessStatusCode)
            return null;
        Console.WriteLine($"-- Accessed Site {SetUrl + "/cards"}");
        
        var html = response.Content.ReadAsStringAsync().Result;

        if (!FindElement("table", html, out var start, out var end))
            return null;
        
        var table = html[start..end];

        var setSources = new List<SetSource>();
        while (table.Contains("<tr>"))
        {
            FindElement("tr", table, out var rowStart, out var rowEnd);
            var row = table[(rowStart + 4)..rowEnd];
            table = table[(rowEnd + 4)..];
            
            
            if (!FindElement("a", row, out var linkStart, out var linkEnd))
                continue;
            
            var link = row[linkStart..linkEnd].Trim();
            var append = row[(linkEnd + 4)..].Trim();
            
            var hrefStart = FindPropertyIndex("href", link);
            var hrefEnd = link.IndexOf(">");
            var url = SetUrl + link[hrefStart..hrefEnd].Replace("\"", "");
            link = link[(hrefEnd + 1)..];
            
            var altStart = FindPropertyIndex("alt", link);
            link = link[(altStart + 1)..];
            var altEnd = link.IndexOf("\"");
            var code = link[..altEnd];
            link = link[(altEnd + 1)..];
            
            var nameStart = link.IndexOf("</span>") + 7;
            var nameEnd = link.IndexOf("<span");
            var name = link[nameStart..nameEnd].Trim();

            FindElement("a", append, out _, out var dateEnd);
            append = append[(dateEnd + 4)..];
            FindElement("a", append, out var countStart, out var countEnd);
            append = append[(countStart + 3)..countEnd];
            var cards = append.Split('>')[1];

            setSources.Add(new SetSource { name = name, code = code, url = url, cards = int.Parse(cards) });
        }

        Console.WriteLine($"-- {setSources.Count} sets found");
        
        // foreach (var set in setSources)
        //     Console.WriteLine($"Set: {set.name} ({set.code}), {set.cards} cards | {set.url}");
        
        return setSources;
    }

    public static List<PokemonSource> GetPokemonSources(SetSource setSource)
    {
        using var client = new HttpClient();
        
        var pkmnSources = new List<PokemonSource>();

        for (var pkCount = 0; pkCount < Math.Min(10, setSource.cards); pkCount++)
        {
            var response = client.GetAsync(setSource.url + $"/{pkCount + 1}").Result;
            if (!response.IsSuccessStatusCode)
                continue;
            var html = response.Content.ReadAsStringAsync().Result;

            var nameIdx = FindClassInstance("card-text-name", html);
            html = html[nameIdx..];
            FindElement("a", html, out var linkStart, out var linkEnd);
            var nameLink = html[(linkStart + 3)..linkEnd].Trim();
            var name = nameLink.Split('>')[1];
            html = html[(linkEnd + 4)..];

            Console.WriteLine(html[..200]);

            pkmnSources.Add(new PokemonSource { name = name });
        }
        
        foreach (var pokemonSource in pkmnSources)
            Console.WriteLine($"Pokemon:  {pokemonSource.name}");

        return pkmnSources;
    }
}