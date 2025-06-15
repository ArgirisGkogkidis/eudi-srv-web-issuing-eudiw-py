import json
import sys
from collections import defaultdict

def convert_claims(claims_list):
    """
    Converts a list of claim dictionaries into a nested dict structure
    grouped by doctype → claim name.
    """
    claims_map = defaultdict(dict)
    for claim in claims_list:
        path = claim.get("path", [])
        if len(path) != 2:
            continue  # skip unsupported structures

        doctype, claim_name = path
        entry = {
            "mandatory": claim.get("mandatory", False)
        }
        if "value_type" in claim:
            entry["value_type"] = claim["value_type"]
        if "display" in claim:
            entry["display"] = claim["display"]
        if "source" in claim:
            entry["source"] = claim["source"]
        if "issuer_conditions" in claim:
            entry["issuer_conditions"] = claim["issuer_conditions"]

        claims_map[doctype][claim_name] = entry

    return dict(claims_map)

def convert_display(display_list):
    """
    Fix logo.uri -> logo.url if needed.
    """
    new_display = []
    for item in display_list:
        if "logo" in item and "uri" in item["logo"]:
            item["logo"]["url"] = item["logo"].pop("uri")
        new_display.append(item)
    return new_display

def convert_entry(entry):
    """
    Converts a single entry (e.g., "eu.europa.ec.eudi.pid_mdoc") configuration.
    """
    new_entry = {}

    # Copy fields directly if they exist
    copy_fields = [
        "format", "doctype", "scope", "cryptographic_binding_methods_supported",
        "credential_signing_alg_values_supported", "credential_alg_values_supported",
        "credential_crv_values_supported", "issuer_config"
    ]
    for key in copy_fields:
        if key in entry:
            new_entry[key] = entry[key]

    # Handle proof_types_supported directly
    if "proof_types_supported" in entry:
        new_entry["proof_types_supported"] = entry["proof_types_supported"]

    # Normalize display
    if "display" in entry:
        new_entry["display"] = convert_display(entry["display"])

    # Convert claims
    if "claims" in entry:
        new_entry["claims"] = convert_claims(entry["claims"])

    return new_entry

def transform(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as infile:
        data = json.load(infile)

    result = {}
    for key, value in data.items():
        result[key] = convert_entry(value)

    with open(output_path, 'w', encoding='utf-8') as outfile:
        json.dump(result, outfile, indent=2, ensure_ascii=False)

    print(f"✔ Transformed config written to: {output_path}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python convert_mdoc_to_draft13.py <input.json> <output.json>")
    else:
        transform(sys.argv[1], sys.argv[2])