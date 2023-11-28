# Changelog

## [Unreleased]

### Changed

- Correction of names `Standard entities editor` in `entities_ui` and `Standard collections editor` in `collections_ui`.
- Correction of values in `04.2_ProjectsAll.xlsx`.

## [0.1.0] - 2023-10-27

### Added

- Added settings features (`usewysiwygeditor`, `fieldWidth` and `fieldHeight`) to `metadataElement code="description"`.
- Included a validator for XML against the XSD schema. Validator can be run with the help of `runValidator.bat` (Windows) or `runValidator.sh` (Linux/MacOS) scripts.

### Changed

- Adjust XSD schema to match the new metadataElement structure.

### Removed

- Removed tags `entry`, `dcequivalent`, `repeatable`, `modality`, `guideline`, and `example` from `metadataElement/labels/label`.
