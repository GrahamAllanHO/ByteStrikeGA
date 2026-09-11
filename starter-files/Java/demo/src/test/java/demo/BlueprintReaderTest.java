package demo;

import static org.junit.jupiter.api.Assertions.assertEquals;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.io.TempDir;

class BlueprintReaderTest {
    @TempDir
    Path tempDir;

    @Test
    void extractRawSecretsReturnsAllMarkedSecrets() throws IOException {
        Path blueprint = tempDir.resolve("blueprint.txt");
        Files.writeString(
            blueprint,
            "Alpha {* AGENT_CODENAME: SHADOWMIND *}\n"
                + "Beta {* VAULT_ACCESS_CODE: DELTA-7-7-ECHO *}\n"
                + "Gamma {* SECURE_COMMS_PROTOCOL *}"
        );

        List<String> secrets = BlueprintReader.extractRawSecrets(blueprint);

        assertEquals(
            List.of(
                "AGENT_CODENAME: SHADOWMIND",
                "VAULT_ACCESS_CODE: DELTA-7-7-ECHO",
                "SECURE_COMMS_PROTOCOL"
            ),
            secrets
        );
    }

    @Test
    void readSecretsParsesEntriesIntoLabelAndValue() throws IOException {
        Path blueprint = tempDir.resolve("blueprint.txt");
        Files.writeString(blueprint, "{* AGENT_CODENAME: SHADOWMIND *}\n{* SECURE_COMMS_PROTOCOL *}");

        List<SecretEntry> secrets = BlueprintReader.readSecrets(blueprint);

        assertEquals(
            List.of(
                new SecretEntry("AGENT_CODENAME", "SHADOWMIND"),
                new SecretEntry("SECURE_COMMS_PROTOCOL", "")
            ),
            secrets
        );
    }
}
