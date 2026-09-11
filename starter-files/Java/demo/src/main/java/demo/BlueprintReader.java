package demo;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public final class BlueprintReader {
    private static final Pattern SECRET_PATTERN = Pattern.compile("\\{\\*\\s*(.*?)\\s*\\*\\}");

    private BlueprintReader() {
    }

    public static List<String> extractRawSecrets(Path filePath) throws IOException {
        String content = Files.readString(filePath);
        Matcher matcher = SECRET_PATTERN.matcher(content);
        List<String> secrets = new ArrayList<>();

        while (matcher.find()) {
            secrets.add(matcher.group(1));
        }

        return secrets;
    }

    public static List<SecretEntry> readSecrets(Path filePath) throws IOException {
        List<String> rawSecrets = extractRawSecrets(filePath);
        List<SecretEntry> secrets = new ArrayList<>(rawSecrets.size());

        for (String rawSecret : rawSecrets) {
            secrets.add(SecretEntry.fromRaw(rawSecret));
        }

        return secrets;
    }

    public static Path findDefaultBlueprint() {
        Path current = Paths.get("").toAbsolutePath();

        while (current != null) {
            Path candidate = current.resolve("blueprint-data.txt");
            if (Files.exists(candidate)) {
                return candidate;
            }
            current = current.getParent();
        }

        throw new IllegalStateException("Could not find blueprint-data.txt");
    }
}
