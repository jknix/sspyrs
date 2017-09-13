SSPYRS
======

The SSPYRS (SQL Server Python Reporting Services) library is a lightweight interface for interacting with and retrieving data from SSRS reports. The core functionality of the library is straightforward. Perform authentication to an SSRS server, initialize a session, and then retrieve the report data from that session. Report data can be interacted with via raw XML, but has predefined methods to organize it into Pandas DataFrame objects.


The SSPYRS library works primarily from the XML export functionality of SSRS. However, this neither XML nor CSV exports are provided in the express versions of SQL Server. The library does include direct download functions for the Excel export included in the express version, however it will not read the data directly into memory.

SSPYRS has been validated to work with SSRS 2008 R2, SSRS 2014, and SSRS 2016 under most server settings.


Usage and Documentation
=======================

Report Objects
--------------

A report object can be initialized as follows::

    import sspyrs
    myrpt = sspyrs.report('http://myreportserver/report',
                           myusername,
                           pass)

If passing parameters to the report, they can be passed as a dictionary as an argument called 'parameters'. Note that parameters must use the actual parameter names designated within the rdl file. Parameters with defaults do not need to be specified unless desired.

Retrieving Data
---------------

**Raw XML Data**

To retrieve the raw XML from the report, use the ``rawdata()`` method::

    rpt_xml = myrpt.rawdata()

The resulting variable will be a dictionary with all report data elements. This will include some report metadata in addition to the XML formatted data elements from the report. Note that some of the XML tags and headings may appear differently than their corresponding report attributes. This is due to the fact that the XML does not include any XML object labels, only their names, which must be unique across the entire .rdl file, not just within an element. For example, in a report with 2 tables which share column names between them, the first table or data object will have the normal column names appended with an "@" (e.g. "@ID","@Val"), while the second table will have column names like "@ID2", "@Val2". The ``tabledata()`` method strips the "@" and numbers out, but the ``rawdata()`` method leaves them be.


**Tabular Data**

To quickly organize the raw XML into a tabular format, use the ``tabledata()`` method::

    rpt_tables = myrpt.tabledata()

The resulting variable will be a dictionary of Pandas DataFrames, whose keys in the dictionary correspond to the data object names within the .rdl file. This method also attempts some limited data parsing for number and date columns.

Exporting Data
--------------

**Default Download**

When working with versions that allow XML exports, the report data can be directly exported to a few convenient formats using the ``download()`` method::

    rpt_downresults = myrpt.download(type='CSV')

The resulting variable lists out the data objects which were downloaded and written to files. Currently available exports include CSV, JSON, and Excel. The default download file type is CSV. For CSV and JSON, a file will be created for each data object, named by its dictionary key from the ``tabledata()`` results. For Excel, a single file with multiple tabs is created.

**Direct Download**

When working with versions of SSRS which do not allow XML data exports (typically because the feature is not included in express editions), the data can be exported directly to any of the available export types (on express editions this usually includes Excel, Word, and PDF) using the ``directdown()`` method.
