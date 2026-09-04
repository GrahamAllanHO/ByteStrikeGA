const fs = require("fs");

/**
 * Reads a blueprint file and extracts all secrets marked between {* and *}
 * Example: League transmission contains {* EMERGENCY_PROTOCOL: NIGHTFALL_SEQUENCE_ACTIVE *}
 * Extracts: "EMERGENCY_PROTOCOL: NIGHTFALL_SEQUENCE_ACTIVE" (without markers)
 * Uses regex pattern with matchAll()
 * @param {string} filename - Path to the blueprint file
 * @returns {Array<string>} Array of extracted secret strings
 */
function decodeBlueprint(filename) {
    const content = fs.readFileSync(filename, "utf8");

    const pattern = /\{\* (.*?) \*\}/g;
    const matches = [...content.matchAll(pattern)];
    const secrets = matches.map((match) => match[1]);

    return secrets;
}

function decodeBlueprintSafe(filename) {
    try {
        return decodeBlueprint(filename);
    } catch (err) {
        console.log(`Error: File '${filename}' not found.`);
        return [];
    }
}

const secrets1 = decodeBlueprintSafe("nonexistent.txt");
console.log(`Found ${secrets1.length} secrets`);

const secrets2 = decodeBlueprintSafe("blueprint-data.txt");
console.log(`Found ${secrets2.length} secrets`);

module.exports = {
    decodeBlueprint,
    decodeBlueprintSafe,
};

function decodeBlueprint(filename) {
    const content = fs.readFileSync(filename, "utf8");
    const pattern = /\{\* (.*?) \*\}/g;
    const matches = [...content.matchAll(pattern)];
    const secrets = matches.map((match) => match[1]);
    return secrets;
}
