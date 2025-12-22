# Salesforce Metadata

This directory contains Salesforce metadata required by the weather pipeline.

## Versioned in v0.3

- Custom Objects & Fields
- Reports
- Permission Sets
- Custom Metadata

## Not Versioned

- Auth information
- Org-specific config
- Data
- Logs

Deploy using:
sf project deploy start --source-dir salesforce/metadata
