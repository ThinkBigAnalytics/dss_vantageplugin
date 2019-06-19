# II. Requirements

---

1. **Dataiku Data Science Studio version 5.1.2 or later**

   Dataiku DSS enterprise edition is required to import datasets from Vantage tables. Dataiku offers both downloadable and online options which can be obtained from the Dataiku [website](https://www.dataiku.com/dss/trynow/). The downloadable option can be configured to use the free or the enterprise edition, while the online option only comes in enterprise edition with free trial for a period of 14 days. A comparison between the two editions can be seen in the features table for [Dataiku DSS Editions](https://www.dataiku.com/dss/editions/).

   Teradata Vantage Analytic Functions plugin has been tested on Dataiku DSS version 5.1.2.  
   &nbsp; 

2. **Teradata Vantage Analytic Functions Plugin**

   The compressed file "`TeradataVantagePlugin.zip`" contains the Teradata Vantage Analytic Functions plugin program and metadata.  
   &nbsp;  

3. **Access Credentials**

   The first set of credentials required is the Vantage Credentials which allow the user to read and write tables into a NewSQL Engine Database. These credentials are used as input to the Dataiku-Vantage connector. Section 3 provides instructions on how to setup a Dataiku connection to a NewSQL Engine database. It is suggested to create one connection per database where one intends to store output tables.

   The next set is the Dataiku User Credentials which allow the user to login to  Dataiku DSS. Section 4 outlines the steps in creating a user in Dataiku.  
   &nbsp;  

4. **Teradata JDBC Driver**

   The Teradata JDBC Driver is required to establish a connection between a Vantage system and Dataiku.



