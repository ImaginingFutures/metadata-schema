# Changelog

## [Unreleased]

### Added

- Added settings features (`usewysiwygeditor`, `fieldWidth` and `fieldHeight`) to `metadataElement code="description"`.
- Included a validator for XML against the XSD schema. Validator can be run with the help of `runValidator.bat` (Windows) or `runValidator.sh` (Linux/MacOS) scripts.

### Changed

- Adjust XSD schema to match the new metadataElement structure.

### Removed

- Removed tags `entry`, `dcequivalent`, `repeatable`, `modality`, `guideline`, and `example` from `metadataElement/labels/label`.
