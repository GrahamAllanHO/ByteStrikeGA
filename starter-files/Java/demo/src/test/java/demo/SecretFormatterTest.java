package demo;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.List;
import org.junit.jupiter.api.Test;
import picocli.CommandLine.Help.Ansi;

class SecretFormatterTest {
    @Test
    void formatSecretReusesTheSameColorForRepeatedLabels() {
        SecretFormatter formatter = new SecretFormatter(Ansi.ON);

        String first = formatter.formatSecret(new SecretEntry("VAULT_ACCESS_CODE", "DELTA-7-7-ECHO"));
        String second = formatter.formatSecret(new SecretEntry("VAULT_ACCESS_CODE", "DELTA-7-7-GAMMA"));

        String firstPrefix = first.substring(0, first.indexOf("VAULT_ACCESS_CODE"));
        String secondPrefix = second.substring(0, second.indexOf("VAULT_ACCESS_CODE"));

        assertEquals(firstPrefix, secondPrefix);
        assertTrue(first.endsWith("DELTA-7-7-ECHO"));
        assertTrue(second.endsWith("DELTA-7-7-GAMMA"));
    }

    @Test
    void tabPaddingAddsAtLeastOneTab() {
        assertFalse(SecretFormatter.tabPadding("LABEL").isEmpty());
        assertTrue(SecretFormatter.tabPadding("LABEL").contains("\t"));
    }

    @Test
    void formatTableAddsHeaderBeforeSecretRows() {
        SecretFormatter formatter = new SecretFormatter(Ansi.OFF);

        List<String> lines = formatter.formatTable(List.of(new SecretEntry("AGENT_CODENAME", "SHADOWMIND")));

        assertEquals("LABEL\t\tVALUE", lines.get(0));
        assertEquals("-----\t\t-----", lines.get(1));
        assertTrue(lines.get(2).contains("AGENT_CODENAME"));
    }
}
