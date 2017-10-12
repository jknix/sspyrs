link = 'http://localhost/reportserver?%2fdevelop%2freportproject%2fExecutions&rs:Command=Render'
link2 = 'http://localhost/ReportServer/Pages/ReportViewer.aspx?%2fdevelop%2freportproject%2fOverallUsageAnalysis&rs:Command=Render'

u = 'nix'
pw = 'Nix123'

rpt = report(link, u, pw)

rd = rpt.rawdata()

table = rpt.tabledata()

rpt.directdown('tmpout/myfile','PDF')
rpt.directdown('tmpout/myfile','Excel')
rpt.directdown('tmpout/myfile','Word')
rpt.directdown('tmpout/myfile','XML')
rpt.directdown('tmpout/myfile','IMAGE')
rpt.directdown('tmpout/myfile','PPTX')
rpt.directdown('tmpout/myfile','CSV')
rpt.directdown('tmpout/myfile','ATOM')