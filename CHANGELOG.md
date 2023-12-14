# Changelog

## [Unreleased]

## Fixed

- Encoding and extra columns in csv mapings and data in `installationdocs`
- Restore `themes` and `culturalcontext` types in `relationshipTable name="ca_objects_x_vocabulary_terms"`
- Update splitter conditions in `installationdocs/04.1_ResourcesMapping.csv`.

### Changed

- Reduce multiple `related_places` elements in the `Spatial Coverage` screen of `objects_ui`.
- Change defaul term in `collection_types` to `project`.
- Replacing "Eurasia" label with "Europe and Central Asia" to separates Europe from the broader Asian context while including Central Asian countries.
- Adding the label "South Asia" to distinct recognition of the countries in this region.


### Added

- Include `georeference` to `places_ui`.

### Fixed

- Renamed `Loan editor` to `Standard objects editor` for `objects_ui`.

## [1.1.0] - 2023-11-29

Detailed changelog in https://github.com/ImaginingFutures/metadata-schema/compare/v0.1.0...v1.1.0

### Changed

- Correction of names `Standard entities editor` in `entities_ui` and `Standard collections editor` in `collections_ui`.
- Transform all installationdocs to csv files for better control.
- Modifications to themes and cultural context vocabularies.
- Changes on the structure of rights statements and licenses. All information regarding user access is included in the category `Usage Permissions`.

## [0.1.0] - 2023-10-27

### Added

- Added settings features (`usewysiwygeditor`, `fieldWidth` and `fieldHeight`) to `metadataElement code="description"`.
- Included a validator for XML against the XSD schema. Validator can be run with the help of `runValidator.bat` (Windows) or `runValidator.sh` (Linux/MacOS) scripts.

### Changed

- Adjust XSD schema to match the new metadataElement structure.

### Removed

- Removed tags `entry`, `dcequivalent`, `repeatable`, `modality`, `guideline`, and `example` from `metadataElement/labels/label`.
