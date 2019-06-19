# I. Introduction

---

Dataiku Data Science Studio \(DSS\) is a collaborative platform that enables teams of people with different data expertise, such as data engineers, data scientists and analysts, to work together efficiently. Dataiku DSS provides a set of built-in recipes or operations that can be applied to transform or analyse a dataset. It also allows users to create their own recipes in Python, SQL or R. Custom reusable recipes for Dataiku are called plugins and can only be written in Python.

Dataiku provides a platform that allows to visualize and re-run workflows. In a Dataiku project, one can easily visualize how data flows across tables and recipes.

The Teradata Vantage Analytic Functions Plugin for Dataiku DSS integrates about 180 of the Vantage Machine Learning Engine \(MLE\) analytic functions, by providing a user-friendly, easy-to-use, no-SQL interface for the functions in the Dataiku DSS environment. The MLE analytic functions can be accessed through the \[+RECIPE\] menu of the FLOW view of a Dataiku project, and are grouped into nine categories:

* Time Series, Path and Attribution Analysis
* Ensemble Methods
* Text Analysis
* Naïve Bayes
* Graph Analysis
* Association Analysis
* Statistical Analysis
* Cluster Analysis
* Data Transformation

In the background of the Teradata Vantage Analytic Functions Plugin user interface, the plugin essentially translates its user input into SQL queries that are sent to the NewSQL Engine of a connected Vantage system via JDBC. This way, all analytic queries are executed in-database, while also all input and output managed datasets are physically located in the database of the NewSQL Engine on the connected Vantage system.

