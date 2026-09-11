package demo;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

class SecretEntryTest {
    @Test
    void fromRawSeparatesLabelAndValue() {
        SecretEntry entry = SecretEntry.fromRaw("AGENT_CODENAME: SHADOWMIND");

        assertEquals("AGENT_CODENAME", entry.label());
        assertEquals("SHADOWMIND", entry.value());
        assertTrue(entry.hasValue());
    }

    @Test
    void fromRawHandlesLabelOnlyEntries() {
        SecretEntry entry = SecretEntry.fromRaw("SECURE_COMMS_PROTOCOL");

        assertEquals("SECURE_COMMS_PROTOCOL", entry.label());
        assertEquals("", entry.value());
        assertFalse(entry.hasValue());
    }
}
