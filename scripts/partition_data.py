from pathlib import Path

from ppp.util import CONFIG_PATH, DATA_PATH, load_config, logging_setup


def extract_year(file: Path):
    """Extracts the year from a file
    name provided by the NYC Taxi
    dataset.
    """
    return file.stem[-7:-3]


def main():
    config = load_config(CONFIG_PATH)
    logger = logging_setup(config)

    parquet_files = list(DATA_PATH.glob("*.parquet"))
    logger.info("Found %d parquet files", len(parquet_files))

    unique_years = {extract_year(file) for file in parquet_files}
    for year in unique_years:
        logger.info("Creating partition for year %s", year)
        (DATA_PATH / f"year={year}").mkdir(exist_ok=True)

    for file in parquet_files:
        year = extract_year(file)
        logger.info("Moving %s to year=%s", file.stem, year)
        new_file = DATA_PATH / f"year={year}" / file.name
        file.rename(new_file)


if __name__ == "__main__":
    main()
