#  VI. Limitations

---

1.    For analytic functions that 
    * take in output table names as arguments, and
    * where the select query produces only a message table indicating the name of the output model/metrics table,
    
it is the responsibility of the user to specify output table names that are **different** from those of the existing tables.

Some analytic functions provide an option to delete an already existing output table prior to executing an algorithm, but others do not. In the former case, the NewSQL Engine throws an "`Already exists`" exception.


2.    The appended version of the Dataiku DSS Teradata Vantage Analytic Functions plugin has been tested to work with the MLE analytic functions on Vantage 1.1 systems. Earlier or later analytic function versions may require a different set of function metadata.

3.    The plugin currently only supports NewSQL Engine datasets as input and output.

4.    Functions with any OUTPUT TABLE type arguments will require the user to add an output dataset for the SELECT statement results of the query and any additional output tables. Please refer to the [Teradata® Vantage Machine Learning Engine Analytic Function](https://docs.teradata.com/reader/AI5zLpFtwEQWIVvpnZgB8g/gaonTshoL4qMQM6~Y~mp5A) Reference documentation page at docs.teradata.com to learn about the output tables of each function.

5.    MapReduce Function pairs are currently limited to the following a select few: `ApproxDCount`, `ApproxPercentile`, `Correlation`, `PCA`, and `Naïve Bayes`. In order to use these functions, please call their corresponding Map Functions on the function selection box and it will display the arguments for both functions.

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

