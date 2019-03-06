library(DBI)
library(dplyr)

db = dbConnect(RSQLite::SQLite(),'test.db')
dbt = tbl(db,'data')

query = dbt %>%
    group_by(x) %>%
    summarise(mean_y = mean(y))

df = collect(query)

head(df)
