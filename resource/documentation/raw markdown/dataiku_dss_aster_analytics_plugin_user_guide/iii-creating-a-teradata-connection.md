# III. Creating a Teradata Connection

---

1.    Follow the instructions in the Dataiku Reference Doc for Installing Database Drivers.
    In summary, one needs to:
    
        a.    Stop the Data Science Studio server, where DATA_DIR is the data directory where Data Science Studio is installed.
        
        &nbsp;    `DATA_DIR/bin/dss stop`
        
        b.    Copy the Teradata JDBC driver to DATA_DIR/lib/jdbc directory.
        &nbsp;    
        
        c.    Restart Data Science Studio        
        &nbsp;    `DATA_DIR/bin/dss start`
        
2.    In the Dataiku DSS home page, click on Apps then on the submenu click Administration (gear icon). Alternatively, you can go to http://dataikuhost:port/admin/.        

    ![](/assets/1a.png)
&nbsp;
    ![](/assets/1b.png)
    
3.    In the DSS settings page, Connections tab, Click on NEW CONNECTION. From the options that will be presented, choose Teradata.

    ![](/assets/2.png)
    
4.    Fill up the fields as needed:    
        **Basic Params**
        **Host**: database.host.name
        **User**: Username    
        **Password**: User's password    
        **Default Database**: default_database    
        **Advanced JDBC properties**:
	    CHARSET:       UTF8
	    TMODE:	 TERA or ANSI                
        
        All other fields can be left as-is.

	    
5.    Click on Test button to verify that connection details provided are valid.
6.    Finally, click on Save button.
