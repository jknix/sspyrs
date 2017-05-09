class report(object):
    """Create a report object with baseline attributes

    """

    # add option to export to different formats

    def __init__(self, link, username, password, parameters=None):
        """Iniates a report object

        Parameters
        ----------
        link : str
            The raw link of the report to use.
        username : str
            The username to access the report
        password : str
            The password to access the report
        parameters : dict 
            A dictionary of parameters to pass to the report
        """
        self.link = link
        self.username = username
        self.password = password
        self.reportname = ''
        if parameters is not None and type(parameters) != dict:
            raise ValueError('Invalid parameters')
        else:
            self.parameters = parameters

    def exportlink(self):
        """Generate a link to a report session

        Returns
        -------
        str
            Link with valid session to get the export information.
        """
        import re
        import requests
        from requests_ntlm import HttpNtlmAuth

        def addparams(link, params):
            linkstring = link
            if params is not None:
                for i in params.keys():
                    keylabel = i
                    keyvalue = params[i]
                    linkstring += '&' + str(keylabel) + '=' + str(keyvalue)

            return linkstring

        link_param = addparams(self.link, self.parameters)

        linkbase = link_param[:re.search('/Report', link_param).start(0) + 1]

        session = requests.session()
        session.auth = HttpNtlmAuth('settlementplan\\' + self.username,
                                    self.password,
                                    session)

        pg = session.get(link_param)
        pg_text = pg.text
        pg_text_split = pg_text.split('\n')
        relpage = [s for s in pg_text_split if 'ExportUrlBase' in s][0]

        linkstart = re.search('ExportUrlBase', relpage).start(0) + 17
        linkend = re.search('FixedTableId', relpage).start(0) - 3
        exportlink = relpage[linkstart:linkend]

        newlink = linkbase + exportlink + 'XML'

        return newlink

    def rawdata(self):
        """Retrieve raw report XML data as a dictionary

        Useful in the case of special reports which may contain graphs, 
        unstructured information, or other inconsistencies. 

        Returns
        -------
        dict
            Dictionary of report data
        """
        import requests
        import xmltodict
        from re import search
        from requests_ntlm import HttpNtlmAuth

        session = requests.session()
        session.auth = HttpNtlmAuth('settlementplan\\' + self.username,
                                    self.password,
                                    session)

        pg = session.get(self.exportlink())
        pg_txt = pg.text[search('<', pg.text).start():]
        pg_xml = xmltodict.parse(pg_txt)
        self.reportname = pg_xml['Report']['@Name']
        self.tables = [x for x in list(pg_xml['Report'].keys()) if
                       '@' not in x]
        return pg_xml

    def tabledata(self):
        """Retrieve only table data from XML

        Returns
        -------
        dict
            Dictionary of pandas DataFrame objects

        """
        from pandas import DataFrame
        from re import search
        rawdata = self.rawdata()
        xmltables = [x for x in list(rawdata['Report'].keys()) if '@' not in x]
        datadict = {}
        for t in xmltables:
            t_group = rawdata['Report'][t]
            t_details_col = t_group[list(t_group.keys())[0]]
            t_details = t_details_col[list(t_details_col.keys())[0]]
            if type(t_details) != list:
                t_details = [t_details]
            df = DataFrame.from_records(t_details, columns=t_details[0].keys())
            df.columns = [x.replace('@', '') for x in df.columns]
            columnends = [x[-1:] for x in df.columns]
            if all([x == columnends[0] for x in columnends]):
                if search('[0-9]', columnends[0]).start() >= 0:
                    df.columns = [x[:-1] for x in df.columns]
            datadict[t] = df
        return datadict

    def download(self, exportformat='CSV'):
        """

        Parameters
        ----------
        exportformat : str
            The format to export the data. Allows excel, json, or csv. Not
            case sensitive. For csv and json, files are created with the
            format <reportname>__<tableobjname>.<ext>. For excel files, 
            the workbook is titled <reportname>.xlsx, and the sheets within 
            are titled by table object name. 

        Returns
        -------
        list
            The list of files/sheets that were successfully written

        """
        from os import path
        from pandas import DataFrame
        exportformat = exportformat.upper()
        allowedformats = ['CSV', 'JSON', 'EXCEL']

        if exportformat not in allowedformats:
            raise ValueError('Format not in allowed types.')

        data = self.tabledata()

        def filever(fname):
            if not path.exists(fname):
                return fname
            else:
                filename, file_extension = path.splitext(fname)
                i = 0
                while i < 5:
                    tmpname = filename + '_' + str(i) + file_extension
                    if not path.exists(tmpname):
                        return tmpname
                    else:
                        i += 1

        basename = filever(self.reportname)

        files = []

        if exportformat != 'EXCEL':
            for dskey in self.tables:
                dataset = data[dskey]
                if exportformat == 'CSV':
                    exportdest = filever(basename + '__' + dskey + '.csv')
                    dataset.to_csv(exportdest)
                    files += [exportdest]
                elif exportformat == 'JSON':
                    exportdest = filever(basename + '__' + dskey + '.json')
                    dataset.to_json(exportdest)
                    files += [exportdest]
                else:
                    pass
        else:
            from pandas import ExcelWriter, DataFrame
            writer = ExcelWriter(filever(basename + '.xlsx'))
            for dskey in self.tables:
                dataset = data[dskey]
                dataset.to_excel(writer, dskey, index=False)
                files += [dskey]
            writer.save()

        return files
