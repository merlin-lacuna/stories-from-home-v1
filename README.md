# stories-from-home-v1

Repository for the data and code that powers the "Stories from Home" art project.

## Data Guidelines

When commiting data make sure that the file meets the following criteria.

1. The file is in CSV format.

2. The name follows the format `element_entity_measurement_location_name.csv` — e.g "`fire_forestfire_nvdi_mendocino.csv`"

3. For the `entity_measurement` combination, make sure that there is a matching story template in the [Story Templates file](https://docs.google.com/spreadsheets/d/1ppMOdtHwWckeUYHZIU_a8FEKzK9PkKGkz_7ZyAikNjg/edit#gid=310651524)
    * If there's no matching story template, request one in the "Stories from Home" WhatsApp group or adjust the dataset.

4. The column that stores the time period should always be called "*Time*".

5. The column that stores the measurement should always be called "*Data*".

6. There should be no empty spaces around the column title "e.g. "Time,Data" not " Time , Data"

7. The time format should always be `YYY-MM-DD`, even if it's monthly or yearly.
    * If years, add january of each year like this "`2020-01-01`, `2021-01-01`, `2022-01-01`"
    * If months, add the first of each month like this: "`2021-01-01`, `2021-02-01`, `2021-03-01`"
    * Don't worry if the data did not fall on that precise date, it will be aggregated.

8. After you've commited the data file, add an corresponding entry to the [Metadata CSV](https://github.com/merlin-lacuna/stories-from-home-v1/blob/main/data/metadata.csv) file and commit the updated metadata file as well.
