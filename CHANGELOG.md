# Changelog

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Method to store arrays in ASE and schnetpack databases.

### Changed

- PDB writer requires arrays instead of reptar files and group keys.
- Rename `data` class to `File`.
This clears up previous ambiguous usage of "data" to refer to both a file and value of a key.
- Rename reptarWriter to textWriter (more specific).
- Require setting the memory for Psi4 worker.

## [0.0.2] - 2022-05-03

### Added

- Parallel implementation of Psi4 and xTB energy and gradient calculations with ray.
- Zenodo DOI.

### Changed

- Updating README and documentation home page.
- Document pip install of reptar.
- Sampling structures copies gradients instead of forces.
- Write test files to temporary, untracked directory.

## [0.0.1] - 2022-04-30

- Initial release!