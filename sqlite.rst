Data interchange between Python and R via sqlite3
-------------------------------------------------------------------------------------

A general overview of the problem is:

* You love to *program* in Python, generating results there.
* You love to *process results* in R, using the tidyverse_.
* Your sets of results may be quite large, perhaps too large to fit nicely into memory.

An obvious solution is to dump the results to an intermediate file.  If you dump to a database,
then you can do at least some of your analysis out of memory using dplyr_, using their database
interface_.

.. literalinclude:: sqlite_example/make_data.py

.. literalinclude:: sqlite_example/process.R

.. _tidyverse: https://www.tidyverse.org/
.. _dpylr: https://dplyr.tidyverse.org
.. _interface: https://db.rstudio.com/dplyr/
