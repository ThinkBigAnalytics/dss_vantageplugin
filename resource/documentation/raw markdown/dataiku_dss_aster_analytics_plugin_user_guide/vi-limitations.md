#  VI. Limitations

---

1.    For analytic functions that take in output table names as arguments and where the select query produces only a message table indicating the name of the output model/metrics table, it is the responsibility of the user to specify output table names that are not the same with that of an existing table. Some analytic functions provide an option to delete an already existing output table prior to executing an algorithm, others do not. If the former is the case, Teradata Database throws an ‘<output table> already exists’ exception.

2.    The appended version of the Dataiku DSS Teradata Vantage Analytic Functions plugin was tested on Teradata 16.20. Earlier or later function versions may require a different set of function metadata.

3.    The plugin currently only supports Teradata Database datasets as input and output.

4.    Functions with any OUTPUT TABLE type arguments will require the user to add an output dataset for the SELECT statement results of the query and any additional output tables. Please refer to the Teradata Vantage Machine Learning Engine Analytic Functions Usage Guide to learn about the output tables of each function.

5.    MapReduce Function pairs are currently limited to a select few: ApproxDCount, ApproxPercentile, Correlation, PCA, and Naive Bayes. In order to use these functions, please call their corresponding Map Functions on the fuction selection box and it will display the arguments for both functions.

6.    Usage of certain functions may feature some inaccuracies, or may not work at all. The functions are as follows:

        * Statistical Analysis
            * Approximate Percentile Map/Reduce
            * Correlation Map/Reduce
            * Cox Hazard Ratio
            * Cross Validation
            * Distribution Match Reduce
        * Text Analysis
            * Text Tokenizer
            * Named Entity Finder Evaluator Map/Reduce            
        * Time Series
            * Time Series Orders
            * Shapelet Supervised
            * ARIMA
        * Ensemble
            * AdaBoost Predict


        


<!-- 3.    In case HTTP error 413 (Request entity too large) or HTTP error 414 (Request URI too long) is encountered after reloading a saved recipe in Dataiku versions earlier than 4.0.4, one can edit Dataiku’s code itself. This is an issue that will be resolved in Dataiku’s next release. To fix this without updating Dataiku, open INSTALL_DIR/frontend/static/dataiku/js/mainpack.js. Locate the  callPythonDo function, and change the HTTP method associated with it from GET to POST. -->

<!-- 6.    As of this writing, Aster Analytics plugin could only refer to SQL-MR functions installed in the public schema. -->
