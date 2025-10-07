
using PokeTCGPSim.Tools;

var sets = Updates.GetSets();

if (sets is null)
    return;

Console.WriteLine($"Set 1: {sets[0].name} ({sets[0].code}) {sets[0].url}");
Updates.GetPokemonSources(sets[0]);

// foreach (var set in sets)
// {
//     continue;
// }