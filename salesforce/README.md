# Salesforce Metadata

This directory contains Salesforce metadata used by the weather pipeline.

## Weather Report – Architecture Intent (v0.3)

- Deprecated fields remain in the schema but are clearly marked and not used by the current pipeline

### Data Layer

Schema reflects current pipeline needs.

- Custom object and fields defined in metadata
- Schema aligns with external pipeline output

### Presentation Layer (Page Layouts / FlexiPages / Reports)

Org default with minimal customization.

- Standard Page Layout in use
- Lightning Record Page not customized yet
- Layout and FlexiPage metadata not yet versioned
- No Reports defined

### Logic Layer

Not required for v0.3.

- No Apex triggers or classes
- Salesforce remains passive

### Automation Layer

Not required for v0.3.

- No Flows or Process Builders
- Salesforce remains passive

### Integration Layer

Primary source of system behavior.

- All writes performed by external pipeline
- No inbound logic within Salesforce

### Security Layer

Default configuration.

- Profiles
- Permission Sets
- Field-Level Security
- No custom security model defined yet

### Deploy

```text
sf project retrieve start --metadata CustomObject:Weather_Report__c
```
