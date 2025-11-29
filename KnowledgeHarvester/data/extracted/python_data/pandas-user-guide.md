User Guide — pandas 2.3.3 documentation


























[Skip to main content](#main-content)



 Back to top
 










`Ctrl`+`K`















* [GitHub](https://github.com/pandas-dev/pandas "GitHub")
* [Twitter](https://twitter.com/pandas_dev "Twitter")
* [Mastodon](https://fosstodon.org/@pandas_dev "Mastodon")
























# User Guide[#](#user-guide "Link to this heading")


The User Guide covers all of pandas by topic area. Each of the subsections
introduces a topic (such as “working with missing data”), and discusses how
pandas approaches the problem, with many examples throughout.


Users brand-new to pandas should start with [10 minutes to pandas](10min.html#min).


For a high level summary of the pandas fundamentals, see [Intro to data structures](dsintro.html#dsintro) and [Essential basic functionality](basics.html#basics).


Further information on any specific method can be obtained in the
[API reference](../reference/index.html#api).



## How to read these guides[#](#how-to-read-these-guides "Link to this heading")


In these guides you will see input code inside code blocks such as:



```
import pandas as pd
pd.DataFrame({'A': [1, 2, 3]})

```


or:



```
In [1]: import pandas as pd

In [2]: pd.DataFrame({'A': [1, 2, 3]})
Out[2]: 
 A
0 1
1 2
2 3

```


The first block is a standard python input, while in the second the `In [1]:` indicates the input is inside a [notebook](https://jupyter.org). In Jupyter Notebooks the last line is printed and plots are shown inline.


For example:



```
In [3]: a = 1

In [4]: a
Out[4]: 1

```


is equivalent to:



```
a = 1
print(a)

```




## Guides[#](#guides "Link to this heading")



* [10 minutes to pandas](10min.html)
	+ [Basic data structures in pandas](10min.html#basic-data-structures-in-pandas)
	+ [Object creation](10min.html#object-creation)
	+ [Viewing data](10min.html#viewing-data)
	+ [Selection](10min.html#selection)
	+ [Missing data](10min.html#missing-data)
	+ [Operations](10min.html#operations)
	+ [Merge](10min.html#merge)
	+ [Grouping](10min.html#grouping)
	+ [Reshaping](10min.html#reshaping)
	+ [Time series](10min.html#time-series)
	+ [Categoricals](10min.html#categoricals)
	+ [Plotting](10min.html#plotting)
	+ [Importing and exporting data](10min.html#importing-and-exporting-data)
	+ [Gotchas](10min.html#gotchas)
* [Intro to data structures](dsintro.html)
	+ [Series](dsintro.html#series)
	+ [DataFrame](dsintro.html#dataframe)
* [Essential basic functionality](basics.html)
	+ [Head and tail](basics.html#head-and-tail)
	+ [Attributes and underlying data](basics.html#attributes-and-underlying-data)
	+ [Accelerated operations](basics.html#accelerated-operations)
	+ [Flexible binary operations](basics.html#flexible-binary-operations)
	+ [Descriptive statistics](basics.html#descriptive-statistics)
	+ [Function application](basics.html#function-application)
	+ [Reindexing and altering labels](basics.html#reindexing-and-altering-labels)
	+ [Iteration](basics.html#iteration)
	+ [.dt accessor](basics.html#dt-accessor)
	+ [Vectorized string methods](basics.html#vectorized-string-methods)
	+ [Sorting](basics.html#sorting)
	+ [Copying](basics.html#copying)
	+ [dtypes](basics.html#dtypes)
	+ [Selecting columns based on `dtype`](basics.html#selecting-columns-based-on-dtype)
* [IO tools (text, CSV, HDF5, …)](io.html)
	+ [CSV & text files](io.html#csv-text-files)
	+ [JSON](io.html#json)
	+ [HTML](io.html#html)
	+ [LaTeX](io.html#latex)
	+ [XML](io.html#xml)
	+ [Excel files](io.html#excel-files)
	+ [OpenDocument Spreadsheets](io.html#opendocument-spreadsheets)
	+ [Binary Excel (.xlsb) files](io.html#binary-excel-xlsb-files)
	+ [Calamine (Excel and ODS files)](io.html#calamine-excel-and-ods-files)
	+ [Clipboard](io.html#clipboard)
	+ [Pickling](io.html#pickling)
	+ [msgpack](io.html#msgpack)
	+ [HDF5 (PyTables)](io.html#hdf5-pytables)
	+ [Feather](io.html#feather)
	+ [Parquet](io.html#parquet)
	+ [ORC](io.html#orc)
	+ [SQL queries](io.html#sql-queries)
	+ [Google BigQuery](io.html#google-bigquery)
	+ [Stata format](io.html#stata-format)
	+ [SAS formats](io.html#sas-formats)
	+ [SPSS formats](io.html#spss-formats)
	+ [Other file formats](io.html#other-file-formats)
	+ [Performance considerations](io.html#performance-considerations)
* [PyArrow Functionality](pyarrow.html)
	+ [Data Structure Integration](pyarrow.html#data-structure-integration)
	+ [Operations](pyarrow.html#operations)
	+ [I/O Reading](pyarrow.html#i-o-reading)
* [Indexing and selecting data](indexing.html)
	+ [Different choices for indexing](indexing.html#different-choices-for-indexing)
	+ [Basics](indexing.html#basics)
	+ [Attribute access](indexing.html#attribute-access)
	+ [Slicing ranges](indexing.html#slicing-ranges)
	+ [Selection by label](indexing.html#selection-by-label)
	+ [Selection by position](indexing.html#selection-by-position)
	+ [Selection by callable](indexing.html#selection-by-callable)
	+ [Combining positional and label-based indexing](indexing.html#combining-positional-and-label-based-indexing)
	+ [Selecting random samples](indexing.html#selecting-random-samples)
	+ [Setting with enlargement](indexing.html#setting-with-enlargement)
	+ [Fast scalar value getting and setting](indexing.html#fast-scalar-value-getting-and-setting)
	+ [Boolean indexing](indexing.html#boolean-indexing)
	+ [Indexing with isin](indexing.html#indexing-with-isin)
	+ [The `where()` Method and Masking](indexing.html#the-where-method-and-masking)
	+ [Setting with enlargement conditionally using `numpy()`](indexing.html#setting-with-enlargement-conditionally-using-numpy)
	+ [The `query()` Method](indexing.html#the-query-method)
	+ [Duplicate data](indexing.html#duplicate-data)
	+ [Dictionary-like `get()` method](indexing.html#dictionary-like-get-method)
	+ [Looking up values by index/column labels](indexing.html#looking-up-values-by-index-column-labels)
	+ [Index objects](indexing.html#index-objects)
	+ [Set / reset index](indexing.html#set-reset-index)
	+ [Returning a view versus a copy](indexing.html#returning-a-view-versus-a-copy)
* [MultiIndex / advanced indexing](advanced.html)
	+ [Hierarchical indexing (MultiIndex)](advanced.html#hierarchical-indexing-multiindex)
	+ [Advanced indexing with hierarchical index](advanced.html#advanced-indexing-with-hierarchical-index)
	+ [Sorting a `MultiIndex`](advanced.html#sorting-a-multiindex)
	+ [Take methods](advanced.html#take-methods)
	+ [Index types](advanced.html#index-types)
	+ [Miscellaneous indexing FAQ](advanced.html#miscellaneous-indexing-faq)
* [Copy-on-Write (CoW)](copy_on_write.html)
	+ [Previous behavior](copy_on_write.html#previous-behavior)
	+ [Migrating to Copy-on-Write](copy_on_write.html#migrating-to-copy-on-write)
	+ [Description](copy_on_write.html#description)
	+ [Chained Assignment](copy_on_write.html#chained-assignment)
	+ [Read-only NumPy arrays](copy_on_write.html#read-only-numpy-arrays)
	+ [Patterns to avoid](copy_on_write.html#patterns-to-avoid)
	+ [Copy-on-Write optimizations](copy_on_write.html#copy-on-write-optimizations)
	+ [How to enable CoW](copy_on_write.html#how-to-enable-cow)
* [Merge, join, concatenate and compare](merging.html)
	+ [`concat()`](merging.html#concat)
	+ [`merge()`](merging.html#merge)
	+ [`DataFrame.join()`](merging.html#dataframe-join)
	+ [`merge\_ordered()`](merging.html#merge-ordered)
	+ [`merge\_asof()`](merging.html#merge-asof)
	+ [`compare()`](merging.html#compare)
* [Reshaping and pivot tables](reshaping.html)
	+ [`pivot()` and `pivot\_table()`](reshaping.html#pivot-and-pivot-table)
	+ [`stack()` and `unstack()`](reshaping.html#stack-and-unstack)
	+ [`melt()` and `wide\_to\_long()`](reshaping.html#melt-and-wide-to-long)
	+ [`get\_dummies()` and `from\_dummies()`](reshaping.html#get-dummies-and-from-dummies)
	+ [`explode()`](reshaping.html#explode)
	+ [`crosstab()`](reshaping.html#crosstab)
	+ [`cut()`](reshaping.html#cut)
	+ [`factorize()`](reshaping.html#factorize)
* [Working with text data](text.html)
	+ [Text data types](text.html#text-data-types)
	+ [String methods](text.html#string-methods)
	+ [Splitting and replacing strings](text.html#splitting-and-replacing-strings)
	+ [Concatenation](text.html#concatenation)
	+ [Indexing with `.str`](text.html#indexing-with-str)
	+ [Extracting substrings](text.html#extracting-substrings)
	+ [Testing for strings that match or contain a pattern](text.html#testing-for-strings-that-match-or-contain-a-pattern)
	+ [Creating indicator variables](text.html#creating-indicator-variables)
	+ [Method summary](text.html#method-summary)
* [Working with missing data](missing_data.html)
	+ [Values considered “missing”](missing_data.html#values-considered-missing)
	+ [`NA` semantics](missing_data.html#na-semantics)
	+ [Inserting missing data](missing_data.html#inserting-missing-data)
	+ [Calculations with missing data](missing_data.html#calculations-with-missing-data)
	+ [Dropping missing data](missing_data.html#dropping-missing-data)
	+ [Filling missing data](missing_data.html#filling-missing-data)
* [Duplicate Labels](duplicates.html)
	+ [Consequences of Duplicate Labels](duplicates.html#consequences-of-duplicate-labels)
	+ [Duplicate Label Detection](duplicates.html#duplicate-label-detection)
	+ [Disallowing Duplicate Labels](duplicates.html#disallowing-duplicate-labels)
* [Categorical data](categorical.html)
	+ [Object creation](categorical.html#object-creation)
	+ [CategoricalDtype](categorical.html#categoricaldtype)
	+ [Description](categorical.html#description)
	+ [Working with categories](categorical.html#working-with-categories)
	+ [Sorting and order](categorical.html#sorting-and-order)
	+ [Comparisons](categorical.html#comparisons)
	+ [Operations](categorical.html#operations)
	+ [Data munging](categorical.html#data-munging)
	+ [Getting data in/out](categorical.html#getting-data-in-out)
	+ [Missing data](categorical.html#missing-data)
	+ [Differences to R’s `factor`](categorical.html#differences-to-r-s-factor)
	+ [Gotchas](categorical.html#gotchas)
* [Nullable integer data type](integer_na.html)
	+ [Construction](integer_na.html#construction)
	+ [Operations](integer_na.html#operations)
	+ [Scalar NA Value](integer_na.html#scalar-na-value)
* [Nullable Boolean data type](boolean.html)
	+ [Indexing with NA values](boolean.html#indexing-with-na-values)
	+ [Kleene logical operations](boolean.html#kleene-logical-operations)
* [Chart visualization](visualization.html)
	+ [Basic plotting: `plot`](visualization.html#basic-plotting-plot)
	+ [Other plots](visualization.html#other-plots)
	+ [Plotting with missing data](visualization.html#plotting-with-missing-data)
	+ [Plotting tools](visualization.html#plotting-tools)
	+ [Plot formatting](visualization.html#plot-formatting)
	+ [Plotting directly with Matplotlib](visualization.html#plotting-directly-with-matplotlib)
	+ [Plotting backends](visualization.html#plotting-backends)
* [Table Visualization](style.html)
	+ [Styler Object and Customising the Display](style.html#Styler-Object-and-Customising-the-Display)
	+ [Formatting the Display](style.html#Formatting-the-Display)
	+ [Styler Object and HTML](style.html#Styler-Object-and-HTML)
	+ [Methods to Add Styles](style.html#Methods-to-Add-Styles)
	+ [Table Styles](style.html#Table-Styles)
	+ [Setting Classes and Linking to External CSS](style.html#Setting-Classes-and-Linking-to-External-CSS)
	+ [Styler Functions](style.html#Styler-Functions)
	+ [Tooltips and Captions](style.html#Tooltips-and-Captions)
	+ [Finer Control with Slicing](style.html#Finer-Control-with-Slicing)
	+ [Optimization](style.html#Optimization)
	+ [Builtin Styles](style.html#Builtin-Styles)
	+ [Sharing styles](style.html#Sharing-styles)
	+ [Limitations](style.html#Limitations)
	+ [Other Fun and Useful Stuff](style.html#Other-Fun-and-Useful-Stuff)
	+ [Export to Excel](style.html#Export-to-Excel)
	+ [Export to LaTeX](style.html#Export-to-LaTeX)
	+ [More About CSS and HTML](style.html#More-About-CSS-and-HTML)
	+ [Extensibility](style.html#Extensibility)
* [Group by: split-apply-combine](groupby.html)
	+ [Splitting an object into groups](groupby.html#splitting-an-object-into-groups)
	+ [Iterating through groups](groupby.html#iterating-through-groups)
	+ [Selecting a group](groupby.html#selecting-a-group)
	+ [Aggregation](groupby.html#aggregation)
	+ [Transformation](groupby.html#transformation)
	+ [Filtration](groupby.html#filtration)
	+ [Flexible `apply`](groupby.html#flexible-apply)
	+ [Numba Accelerated Routines](groupby.html#numba-accelerated-routines)
	+ [Other useful features](groupby.html#other-useful-features)
	+ [Examples](groupby.html#examples)
* [Windowing operations](window.html)
	+ [Overview](window.html#overview)
	+ [Rolling window](window.html#rolling-window)
	+ [Weighted window](window.html#weighted-window)
	+ [Expanding window](window.html#expanding-window)
	+ [Exponentially weighted window](window.html#exponentially-weighted-window)
* [Time series / date functionality](timeseries.html)
	+ [Overview](timeseries.html#overview)
	+ [Timestamps vs. time spans](timeseries.html#timestamps-vs-time-spans)
	+ [Converting to timestamps](timeseries.html#converting-to-timestamps)
	+ [Generating ranges of timestamps](timeseries.html#generating-ranges-of-timestamps)
	+ [Timestamp limitations](timeseries.html#timestamp-limitations)
	+ [Indexing](timeseries.html#indexing)
	+ [Time/date components](timeseries.html#time-date-components)
	+ [DateOffset objects](timeseries.html#dateoffset-objects)
	+ [Time Series-related instance methods](timeseries.html#time-series-related-instance-methods)
	+ [Resampling](timeseries.html#resampling)
	+ [Time span representation](timeseries.html#time-span-representation)
	+ [Converting between representations](timeseries.html#converting-between-representations)
	+ [Representing out-of-bounds spans](timeseries.html#representing-out-of-bounds-spans)
	+ [Time zone handling](timeseries.html#time-zone-handling)
* [Time deltas](timedeltas.html)
	+ [Parsing](timedeltas.html#parsing)
	+ [Operations](timedeltas.html#operations)
	+ [Reductions](timedeltas.html#reductions)
	+ [Frequency conversion](timedeltas.html#frequency-conversion)
	+ [Attributes](timedeltas.html#attributes)
	+ [TimedeltaIndex](timedeltas.html#timedeltaindex)
	+ [Resampling](timedeltas.html#resampling)
* [Options and settings](options.html)
	+ [Overview](options.html#overview)
	+ [Available options](options.html#available-options)
	+ [Getting and setting options](options.html#getting-and-setting-options)
	+ [Setting startup options in Python/IPython environment](options.html#setting-startup-options-in-python-ipython-environment)
	+ [Frequently used options](options.html#frequently-used-options)
	+ [Number formatting](options.html#number-formatting)
	+ [Unicode formatting](options.html#unicode-formatting)
	+ [Table schema display](options.html#table-schema-display)
* [Enhancing performance](enhancingperf.html)
	+ [Cython (writing C extensions for pandas)](enhancingperf.html#cython-writing-c-extensions-for-pandas)
	+ [Numba (JIT compilation)](enhancingperf.html#numba-jit-compilation)
	+ [Expression evaluation via `eval()`](enhancingperf.html#expression-evaluation-via-eval)
* [Scaling to large datasets](scale.html)
	+ [Load less data](scale.html#load-less-data)
	+ [Use efficient datatypes](scale.html#use-efficient-datatypes)
	+ [Use chunking](scale.html#use-chunking)
	+ [Use Other Libraries](scale.html#use-other-libraries)
* [Sparse data structures](sparse.html)
	+ [SparseArray](sparse.html#sparsearray)
	+ [SparseDtype](sparse.html#sparsedtype)
	+ [Sparse accessor](sparse.html#sparse-accessor)
	+ [Sparse calculation](sparse.html#sparse-calculation)
	+ [Interaction with *scipy.sparse*](sparse.html#interaction-with-scipy-sparse)
* [Migration guide for the new string data type (pandas 3.0)](migration-3-strings.html)
	+ [Background](migration-3-strings.html#background)
	+ [Brief introduction to the new default string dtype](migration-3-strings.html#brief-introduction-to-the-new-default-string-dtype)
	+ [Overview of behavior differences and how to address them](migration-3-strings.html#overview-of-behavior-differences-and-how-to-address-them)
* [Frequently Asked Questions (FAQ)](gotchas.html)
	+ [DataFrame memory usage](gotchas.html#dataframe-memory-usage)
	+ [Using if/truth statements with pandas](gotchas.html#using-if-truth-statements-with-pandas)
	+ [Mutating with User Defined Function (UDF) methods](gotchas.html#mutating-with-user-defined-function-udf-methods)
	+ [Missing value representation for NumPy types](gotchas.html#missing-value-representation-for-numpy-types)
	+ [Differences with NumPy](gotchas.html#differences-with-numpy)
	+ [Thread-safety](gotchas.html#thread-safety)
	+ [Byte-ordering issues](gotchas.html#byte-ordering-issues)
* [Cookbook](cookbook.html)
	+ [Idioms](cookbook.html#idioms)
	+ [Selection](cookbook.html#selection)
	+ [Multiindexing](cookbook.html#multiindexing)
	+ [Missing data](cookbook.html#missing-data)
	+ [Grouping](cookbook.html#grouping)
	+ [Timeseries](cookbook.html#timeseries)
	+ [Merge](cookbook.html#merge)
	+ [Plotting](cookbook.html#plotting)
	+ [Data in/out](cookbook.html#data-in-out)
	+ [Computation](cookbook.html#computation)
	+ [Timedeltas](cookbook.html#timedeltas)
	+ [Creating example data](cookbook.html#creating-example-data)
	+ [Constant series](cookbook.html#constant-series)










 On this page
 



[Show Source](../_sources/user_guide/index.rst.txt)