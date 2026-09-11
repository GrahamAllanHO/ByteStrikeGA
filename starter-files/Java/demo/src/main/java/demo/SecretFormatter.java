package demo;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import picocli.CommandLine.Help.Ansi;

public class SecretFormatter {
    private static final String[] LABEL_STYLES = {
        "fg(red)",
        "fg(green)",
        "fg(yellow)",
        "fg(blue)",
        "fg(magenta)",
        "fg(cyan)"
    };

    private final Ansi ansi;
    private final Map<String, String> labelStyles = new LinkedHashMap<>();

    public SecretFormatter() {
        this(Ansi.AUTO);
    }

    SecretFormatter(Ansi ansi) {
        this.ansi = ansi;
    }

    public List<String> formatTable(List<SecretEntry> secrets) {
        List<String> lines = new ArrayList<>();
        lines.add(formatHeader());
        lines.add("-----\t\t-----");

        for (SecretEntry secret : secrets) {
            lines.add(formatSecret(secret));
        }

        return lines;
    }

    public String formatHeader() {
        return styledText("bold", "LABEL\t\tVALUE");
    }

    public String formatSecret(SecretEntry secret) {
        String style = labelStyles.computeIfAbsent(
            secret.label(),
            ignored -> LABEL_STYLES[labelStyles.size() % LABEL_STYLES.length]
        );

        if (secret.hasValue()) {
            return styledText("bold," + style, secret.label() + ":")
                + tabPadding(secret.label())
                + secret.value();
        }

        return styledText("bold," + style, secret.label());
    }

    static String tabPadding(String label) {
        int targetColumn = 24;
        int tabWidth = 8;
        int visibleWidth = label.length() + 1;
        int tabsNeeded = Math.max(1, (targetColumn - visibleWidth + tabWidth - 1) / tabWidth);
        return "\t".repeat(tabsNeeded);
    }

    private String styledText(String style, String text) {
        return ansi.string("@|" + style + " " + text + "|@");
    }
}
