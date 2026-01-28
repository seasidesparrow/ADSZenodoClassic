# ADSZenodoClassic
Repository for the current (as of 2026) Zenodo set-harvesting package used by classic backoffice


# Parameters
- LOG_DIR: Each harvested set has its own log that gets written to this directory.  These logs record both the harvest results, and the date of last harvest. The log file is read at the start of each operation to determine the last harvest date, and then appended to at the end of operation.

- SETS_FILENAME: the name of a file containing set names to be harvested from Zenodo.org (one set per line, with anything after a pound sign (`#`) ignored)

- SLEEP_TIME: integer in seconds, to set how long the harvester will sleep in between set harvests (mainly as a courtesy to the upstream provider)


# Output
The harvester currently outputs content to the directory (`./oai/`) in Dublin Core XML format.  The file tree inside of `oai/` conforms to the old-style classic harvest where the output file is put into its own directory path created from the record's OAI identifier.  As an example the output file for the record `"oai:zenodo.org:17834270"` is written to `oai/zenodo.org/17/83/42/70/metadata.xml`
