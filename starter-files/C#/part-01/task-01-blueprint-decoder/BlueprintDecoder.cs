using System;
using System.Collections.Generic;
using System.IO;
using System.Text.RegularExpressions;

public class BlueprintDecoder
{
    public static List<string> ExtractSecretsFromBlueprint(string filePath)
    {
        string content = File.ReadAllText(filePath);
        string pattern = @"\{\*\s*(.*?)\s*\*\}";

        MatchCollection matches = Regex.Matches(content, pattern);
        List<string> secrets = new List<string>();

        foreach (Match match in matches)
        {
            secrets.Add(match.Groups[1].Value);
        }

        return secrets;
    }

    public static List<string> DecodeBlueprint(string filePath)
    {
        return ExtractSecretsFromBlueprint(filePath);
    }

    public static void Main()
    {
        List<string> secrets = ExtractSecretsFromBlueprint("blueprint-data.txt");
        Console.WriteLine("Extracted secrets (c#):");

        foreach (string secret in secrets)
        {
            Console.WriteLine(secret);
        }
    }
}
