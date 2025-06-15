#!/usr/bin/env python3
import json
import os
from pathlib import Path

def convert_mdoc_to_draft13(mdoc_file):
    """Convert mdoc format to draft 13 format."""
    with open(mdoc_file, 'r') as f:
        mdoc_data = json.load(f)

    # Get the credential type (e.g., 'eu.europa.ec.eudi.pid_mdoc')
    credential_type = list(mdoc_data.keys())[0]
    
    # Extract the claims
    claims = mdoc_data[credential_type].get('claims', {}).get('eu.europa.ec.eudi.pid.1', {})
    
    # Create draft 13 format
    draft13_format = {
        "credential_definition": {
            "type": ["VerifiableCredential", credential_type.replace('_mdoc', 'Credential')],
            "credentialSubject": {
                "type": [credential_type.replace('_mdoc', 'CredentialSubject')]
            }
        },
        "format": "jwt_vc_json",
        "scope": mdoc_data[credential_type].get('scope', ''),
        "cryptographic_binding_methods_supported": ["did:key"],
        "credential_signing_alg_values_supported": ["ES256"],
        "display": mdoc_data[credential_type].get('display', []),
        "claims": {}
    }

    # Convert claims to draft 13 format
    for claim_name, claim_data in claims.items():
        draft13_format["claims"][claim_name] = {
            "mandatory": claim_data.get("mandatory", False),
            "display": claim_data.get("display", []),
            "value_type": claim_data.get("value_type", "string")
        }

    return {
        credential_type.replace('_mdoc', '_jwt_vc'): draft13_format
    }

def process_directory(input_dir, output_dir):
    """Process all mdoc files in a directory."""
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    for mdoc_file in input_path.glob('*_mdoc.json'):
        try:
            draft13_data = convert_mdoc_to_draft13(mdoc_file)
            output_file = output_path / mdoc_file.name.replace('_mdoc.json', '_jwt_vc.json')
            
            with open(output_file, 'w') as f:
                json.dump(draft13_data, f, indent=2)
            
            print(f"Converted {mdoc_file.name} to {output_file.name}")
        except Exception as e:
            print(f"Error converting {mdoc_file.name}: {str(e)}")

if __name__ == "__main__":
    # Example usage
    input_dir = "app/metadata_config/credentials_supported"
    output_dir = "app/metadata_config/credentials_supported/draft13"
    
    process_directory(input_dir, output_dir) 