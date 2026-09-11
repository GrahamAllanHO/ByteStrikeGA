package demo;

import java.io.IOException;
import java.nio.file.Path;
import java.util.List;
import java.util.concurrent.Callable;
import picocli.CommandLine;
import picocli.CommandLine.Command;
import picocli.CommandLine.Parameters;

@Command(
    name = "demo",
    mixinStandardHelpOptions = true,
    description = "Extracts blueprint secrets and prints them in a formatted table."
)
public class Demo implements Callable<Integer> {
    @Parameters(
        index = "0",
        arity = "0..1",
        description = "Optional path to the blueprint file."
    )
    private Path blueprintPath;

    @Override
    public Integer call() throws IOException {
        Path resolvedBlueprintPath = blueprintPath != null
            ? blueprintPath
            : BlueprintReader.findDefaultBlueprint();
        List<SecretEntry> secrets = BlueprintReader.readSecrets(resolvedBlueprintPath);

        if (secrets.isEmpty()) {
            System.out.println("No secrets found.");
            return 0;
        }

        SecretFormatter formatter = new SecretFormatter();
        for (String line : formatter.formatTable(secrets)) {
            System.out.println(line);
        }

        return 0;
    }

    public static void main(String[] args) {
        new CommandLine(new Demo()).execute(args);
    }
}
