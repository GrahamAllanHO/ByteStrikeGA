using NUnit.Framework;
using System.Collections.Generic;
using System.IO;

[TestFixture]
public class BlueprintDecoderTests
{
    [Test]
    public void ExtractSecretsFromBlueprint_WithMultipleSecrets_ReturnsAllSecrets()
    {
        string filePath = Path.GetTempFileName();

        try
        {
            File.WriteAllText(
                filePath,
                "Mission {* AGENT_CODENAME: SHADOWMIND *} note {* VAULT_ACCESS_CODE: DELTA-7-7-ECHO *}");

            var result = BlueprintDecoder.ExtractSecretsFromBlueprint(filePath);

            Assert.That(
                result,
                Is.EqualTo(new List<string>
                {
                    "AGENT_CODENAME: SHADOWMIND",
                    "VAULT_ACCESS_CODE: DELTA-7-7-ECHO"
                }));
        }
        finally
        {
            File.Delete(filePath);
        }
    }

    [Test]
    public void ExtractSecretsFromBlueprint_WithWhitespaceAroundMarker_TrimsOuterWhitespace()
    {
        string filePath = Path.GetTempFileName();

        try
        {
            File.WriteAllText(filePath, "Intel {*   MEETING_LOCATION: SAFEHOUSE_BERLIN_CHECKPOINT_C   *}");

            var result = BlueprintDecoder.ExtractSecretsFromBlueprint(filePath);

            Assert.That(result, Is.EqualTo(new List<string> { "MEETING_LOCATION: SAFEHOUSE_BERLIN_CHECKPOINT_C" }));
        }
        finally
        {
            File.Delete(filePath);
        }
    }

    [Test]
    public void ExtractSecretsFromBlueprint_WithNoSecrets_ReturnsEmpty()
    {
        string filePath = Path.GetTempFileName();

        try
        {
            File.WriteAllText(filePath, "Technical notes without any hidden markers.");

            var result = BlueprintDecoder.ExtractSecretsFromBlueprint(filePath);

            Assert.That(result, Is.Empty);
        }
        finally
        {
            File.Delete(filePath);
        }
    }

    [Test]
    public void DecodeBlueprint_UsesSameExtractionLogic()
    {
        string filePath = Path.GetTempFileName();

        try
        {
            File.WriteAllText(filePath, "{* EMERGENCY_PROTOCOL: NIGHTFALL_SEQUENCE_ACTIVE *}");

            var result = BlueprintDecoder.DecodeBlueprint(filePath);

            Assert.That(result, Is.EqualTo(new List<string> { "EMERGENCY_PROTOCOL: NIGHTFALL_SEQUENCE_ACTIVE" }));
        }
        finally
        {
            File.Delete(filePath);
        }
    }
}
