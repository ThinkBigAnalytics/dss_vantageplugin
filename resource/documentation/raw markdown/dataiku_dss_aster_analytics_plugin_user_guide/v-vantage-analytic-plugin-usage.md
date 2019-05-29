# V. Teradata Vantage Analytic Functions plugin Usage

---
##Usage
This section assumes that a Dataiku project already exists and input datasets have already been imported. Note that recipes need a non-empty dataset as input to run.

1. Go to the flow view of the Dataiku project, where the recipe is to be created, by clicking on the GO TO FLOW button or by clicking on the flow icon in the project menu.

 ![](/assets/usage_1.png)  
 &nbsp;

2. In the Flow view, under Recipe, select desired recipe under the Teradata Vantage Analytic Functions plugin. The recipe names correspond to the different categories of Teradata Vantage Analytic Functions.
 
 ![](/assets/recipe.png)   
 &nbsp;
 ![](/assets/usage_2.png)   
 &nbsp;

3. In New custom recipe popup, specify the input and output datasets. There can be more than one input dataset, as in the case of multiple-input analytic functions. The same is also the case for ML Functions with multiple output datasets. The output dataset will be stored in the database and schema corresponding to the connection selected in the Store into field. Click on CREATE button when done.

 ![](/assets/usage_3.png)   
 &nbsp;
 
4. In the recipe settings, one can select the most suitable function for manipulating or analysing the input dataset. Configure the chosen analytic recipe (input tables, partition and order attributes, and arguments). Required and optional fields are separated into tabs.

 ![](/assets/usage_4.png) 
 &nbsp;  
 
5. The SQL Clauses tab allows the user to modify the query to be performed.

 ![](/assets/additional_clauses.png) 
 &nbsp;  
 
*Modify Select Columns of Output Query* allows the user to modify the SELECT clause of the query.
*Additional Clauses* allows the user to append additional SQL clauses to the query such as WHERE, ORDER BY, GROUP BY, and other similar clauses..
```
SELECT {modified select} FROM function_name(
    ...
    )
    {additional clauses}
```

6. Click on the RUN button or save the recipe settings for later use.
 
 ![](/assets/usage_5.png) 
 &nbsp;  

##Usage Notes

1. Functions with multiple output datasets will normally require an output dataset for the functions' output message/result alongside any other output tables/datasets specified in the recipe.
Please note that the output dataset/s name/s should also match the name within the recipe's settings.

<!-- 2. Some functions allow -->