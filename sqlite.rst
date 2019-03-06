Data interchange between Python and R via sqlite3
-------------------------------------------------------------------------------------

A general overview of the problem is:

* You love to *program* in Python, generating results there.
* You love to *process results* in R, using the tidyverse_.
* Your sets of results may be quite large, perhaps too large to fit nicely into memory.

An obvious solution is to dump the results to an intermediate file.  If you dump to a database,
then you can do at least some of your analysis out of memory using dplyr_, using their database
interface_.

The code for these examples is included in the repo, in the `sqlite_example` directory. They are copied 
here because GitHub doesn't allow the `literalinclude` directive.  The versions here have more detailed
comments.

.. code-block:: python

    import sqlite3
    import pandas as pd
    from collections import namedtuple

    # Create a data type for our data.
    # Named tuples are more storage-efficient
    # than a typical Python class, as they
    # use __slots__.  Member acccess 
    # is via the field names, which are x 
    # and y here.
    # Oddly, the string used for the 
    # constructor seems to be meaningless?
    Datum = namedtuple('Datum', ['x', 'y'])

    # Make some data
    data = [Datum(1, i) for i in range(10)]
    data.extend([Datum(2, i*i) for i in range(11, 21)])

    # MAke a data frame and send it do a database.
    df = pd.DataFrame(data, columns=Datum._fields)

    # NOTE: here is where you have to worry 
    # about what the right thing to do is 
    # if the db already exists, or if the 
    # table does, etc.
    with sqlite3.connect("test.db") as conn:
        df.to_sql('data', # Name of the SQL table
                  conn,
                  if_exists='replace', # Can use 'append', too.
                  index=False) # You usually want this
        # Bonus points: create an index
        conn.execute('create index index_x on data(x)')

The **amazing** thing is that we may now analyze our data using dplyr!
As long as we restrict ourselves to the set of verbs that map directly to 
SQL operations, everything will "just work".  More on that after the code:

.. code-block:: r

    library(DBI)
    library(dplyr)

    # Instead of opening a file, we connect
    # to the database:
    db = dbConnect(RSQLite::SQLite(),'test.db')
    # And then connect to the table:
    dbt = tbl(db,'data')

    # This is our query. Under the hood,
    # dplyr will write the SQL for us:
    query = dbt %>%
        group_by(x) %>%
        summarise(mean_y = mean(y))

    # The query is not evaluated 
    # until we collect it:
    df = collect(query)

    head(df)

The result is::

        # A tibble: 2 x 2
          x mean_y
      <int>  <dbl>
    1     1    4.5
    2     2  248. 
    
If you need to use dplyr verbs that do not map one-to-one to existing SQL operations,
then you need a two-step pipeline:

1. Do what you can in the query and collect it.
2. Do the rest on what you get from the query.

.. _tidyverse: https://www.tidyverse.org/
.. _dplyr: https://dplyr.tidyverse.org
.. _interface: https://db.rstudio.com/dplyr/
