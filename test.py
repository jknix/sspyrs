link = 'http://localhost/reportserver?%2fdevelop%2freportproject%2fExecutions&rs:Command=Render'
link2 = 'http://localhost/ReportServer/Pages/ReportViewer.aspx?%2fdevelop%2freportproject%2fOverallUsageAnalysis&rs:Command=Render'

u = 'nix'
pw = 'Nix123'

rpt = report(link2, u, pw)

rd = rpt.rawdata()

table = rpt.tabledata()










from pandas import DataFrame, to_numeric, to_datetime
from re import search
rawdata = rpt.rawdata()
xmltables = [x for x in list(rawdata['Report'].keys()) if '@' not in x]
datadict = {}
for t in xmltables:
    t_group = rawdata['Report'][t]
    if t_group is not None:
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

        def guesstype(ser, sample=50):
            sersam = ser.sample(min(sample, len(ser)))
            if all([x[5] == '-' and x[10] == 'T' for x in sersam]):
                return 'date'
            else:
                return 1

        #todo add float parser
        datadict[t] = df
    else:
        import warnings
        warnings.warn(
            'Table ' + t + ' detected with no data, skipping.')
return datadict