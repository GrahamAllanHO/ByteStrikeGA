package demo;

public record SecretEntry(String label, String value) {
    public static SecretEntry fromRaw(String rawSecret) {
        int separatorIndex = rawSecret.indexOf(':');
        if (separatorIndex < 0) {
            return new SecretEntry(rawSecret.trim(), "");
        }

        String label = rawSecret.substring(0, separatorIndex).trim();
        String value = rawSecret.substring(separatorIndex + 1).trim();
        return new SecretEntry(label, value);
    }

    public boolean hasValue() {
        return !value.isEmpty();
    }
}
