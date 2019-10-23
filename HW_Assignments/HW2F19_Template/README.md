# W4111_F19_HW2
Implementation template for homework 2.

##Files included and directory structure:
- HW_Assignments:
    - HW2F19_Template:
        - src:
            - data_service:
                - data_table_adaptor.py
                - dbutils.py
                - RDBDataTable.py
        - test:
            - test_data_table_adaptor.py
            - output:
                - GET_databases.png
                - GET_resource_by_id_1.png
                - GET_resource_by_id_2.png
                - test_data_table_adaptor.txt
        - README.md
---

##Notes on what is delivered:


###data_table_adaptor:

*data_table_adaptor.py* and its tests in *test_data_table_adaptor.py* have been fully implemented to the extent of my 
knowledge. Their output can be found in *test/output/test_data_table_adaptor.txt*

###RDBDataTable:

Functions *get_primary_key_columns()* and *get_row_count()* have been implemented and work to the best of my knowledge. 
Their implementation is based on Dr. Ferguson's examples during video office hours on 10-13-2019, as well as some other 
resources detailed in the source code comments. Some minor changes were made to the rest of the source code for this 
class in order to make it work properly.

There are no proper unit tests for these two functions, but they were tested one by one when debugging and doing 
requests using *Postman*. Details about *Postman* tests are in the *app.py* section below.

###app.py:

Due to time constraints, only *dbs()* and GET request for *resource_by_id()* were implemented. The code is based on Dr. 
Ferguson's examples during video office hours on 10-13-2019. 

The results using *Postman* can be found at: 
- *output/GET_databases.png* for *dbs()*
- *output/GET_resource_by_id_1* and *output/GET_resource_by_id_2* for *resource_by_id()*

###Part 2 (Written) and Part 3 (SQL Queries)

Delivered via Courseworks as separate files, as instructed in *Specification_HW2.pdf*.

##Late Days:

This assignment was due on Friday, October 18. I am delivering it on Tuesday, October 22. This is a difference of 4 days. 

I will be using 3 of my 5 late days without penalty. I will take 1 day with penalty.