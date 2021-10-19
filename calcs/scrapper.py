from urllib.request import Request, urlopen
from bs4 import BeautifulSoup 

base_url="https://dpboss.net/"
def get_live_satta():
    req = Request('https://dpboss.net', headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    # URL='https://www.google.com/search?&q=weather in bangalore'
    # URL='https://dpboss.net/milan-night-chart.php'
    # URL='https://dpboss.net'
    # req=requests.get(url=URL,  verify=False).text
    sor = BeautifulSoup(webpage, "html.parser")  
    # 
    # Finding temperature in Celsius 
    # 
    root = sor.find("div", class_='satta-result')
    # 
    # print(root.text)
    # 
    all_li=root.find_all("div")
    satta={}
    for i in range(len(all_li)):
        if(i%3==0):
            ini=all_li[i]
            h4s=ini.find("h4").text
            h5s=ini.find("h5").text
            h6s=ini.find("h6").text.replace(u'\xa0', u' ').split('   ')
            lefti=str(ini.find("div", class_='result_timing')).replace('<div class="result_timing">\n<a class="btn_chart" href="','').replace('">Jodi</a>\n</div>','')
            righti=str(ini.find("div", class_='result_timing_right')).replace('<div class="result_timing_right">\n<a class="btn_chart" href="','').replace('">Panel</a>\n</div>','')
            
            satta.update({h4s:{}})
            satta[h4s].update({"score":h5s})
            satta[h4s].update({"start":h6s[0].strip()})
            satta[h4s].update({"end":h6s[1].strip()})
            satta[h4s].update({"jodi_link":lefti})
            satta[h4s].update({"panel_link":righti})
            # 
            # print(h4s,h5s,h6s,lefti,righti)
    
    return satta

satta=get_live_satta()

def try_int(x):
    try:
        try:
            ss=x[2]
            jj = [int(a) for a in str(x)]
            return(jj)
        except:
            return int(x.strip())
    except ValueError:
        return x.strip()

def dates_stripper(date_ranges):
    # from datetime import datetime
    import datetime
    try:
        start_str=date_ranges.split('To')[0].strip()
        end_str=date_ranges.split('To')[1].strip()
    except:
        start_str=date_ranges.split('to')[0].strip()
        end_str=date_ranges.split('to')[1].strip()
    # 
    try:
        start=datetime.datetime.strptime(start_str,'%d-%m-%Y')
        end=datetime.datetime.strptime(end_str,'%d-%m-%Y')
    except:
        try:
            start=datetime.datetime.strptime(start_str,'%d/%m/%Y')
            end=datetime.datetime.strptime(end_str,'%d/%m/%Y')
        except:
            start=datetime.datetime.strptime(start_str,'%Y-%m-%d')
            end=datetime.datetime.strptime(end_str,'%Y-%m-%d')
    # 
    # 
    days_diff=int(str(end-start).split(" ")[0])
    date_li=[]
    for i in range(days_diff+1):
        new_date=start+datetime.timedelta(days=i)
        new_date_str=datetime.datetime.strftime(new_date,'%d-%m-%Y')
        date_li.append(new_date_str)
    # 
    return date_li


def get_chart_data(game):
    panel_linker=base_url+satta[game]['panel_link']
    # starts here
    req = Request(panel_linker, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    # 
    sor = BeautifulSoup(webpage, "html.parser")  
    # 
    # Finding temperature in Celsius 
    # 
    table = sor.find("table", class_='panel-chart chart-table')
    tbody=table.find("tbody")
    # 
    trs=tbody.find_all("tr")
    chart_data={}
    for i in range(len(trs)):
        ini=(trs[i])
        tds=ini.find_all("td")
        # for the internal one
        try:
            date_ranges=tds[0].text
            tds.pop(0)
            date_li=dates_stripper(date_ranges)
            k=-1
            for j in range(len(tds)):
                if((j%3==0)):
                    k=k+1
                    # print(k)
                    # print(i,j,k)
                    chart_data.update({date_li[k]:{}})
                    val=[try_int(x) for x in  tds[j].text.split('  ')]
                    try:
                        val[0][0]
                        chart_data[date_li[k]].update({"open_panel":val[0]})
                    except:
                        chart_data[date_li[k]].update({"open_panel":val})
                elif((j%3==1)):
                    try:
                        chart_data[date_li[k]].update({"jodi":(tds[j].text)})
                        chart_data[date_li[k]].update({"open_ank":int(str(tds[j].text)[0])})
                        chart_data[date_li[k]].update({"close_ank":int(str(tds[j].text)[1])})
                    except:
                        chart_data[date_li[k]].update({"jodi":(tds[j].text)})
                        chart_data[date_li[k]].update({"open_ank":(str(tds[j].text)[0])})
                        chart_data[date_li[k]].update({"close_ank":(str(tds[j].text)[1])})
                elif((j%3==2)):
                    val=[try_int(x) for x in  tds[j].text.strip().split(' ')]
                    try:
                        val[0][0]
                        chart_data[date_li[k]].update({"close_panel":val[0]})
                    except:
                        chart_data[date_li[k]].update({"close_panel":val})
                # print(j)
        except:
            pass
    return chart_data



# get_chart_data('MILAN MORNING')
# get_chart_data('SRIDEVI')
# get_chart_data('KALYAN MORNING')
# get_chart_data('MADHURI')
# get_chart_data('PADMAVATI')
# get_chart_data('TIME BAZAR')
# get_chart_data('TARA MUMBAI DAY')
# get_chart_data('TIME BAZAR DAY')
# get_chart_data('MILAN DAY')
# get_chart_data('MAIN BAZAR DAY')
# get_chart_data('KALYAN')
# get_chart_data('SRIDEVI NIGHT')
# get_chart_data('MADHURI NIGHT')
#     # get_chart_data('NIGHT TIME BAZAR')
# get_chart_data('TARA MUMBAI NIGHT')
# get_chart_data('MILAN NIGHT')
# get_chart_data('RAJDHANI NIGHT')
# get_chart_data('MAIN BAZAR')
#     # get_chart_data('MAIN MILAN DAY')
# get_chart_data('MUMBAI ROYAL DAY')
# get_chart_data('MUMBAI ROYAL NIGHT')
# get_chart_data('NEW RAJDHANI DAY')
# get_chart_data('KALYAN NIGHT')
# get_chart_data('SHUBHANK')
# get_chart_data('SILVER')
#             # get_chart_data('SILVER NIGHT')
# get_chart_data('RAJASHREE MORNING')
# get_chart_data('RAJASHREE')
# get_chart_data('OLD MAIN MUMBAI')
# get_chart_data('RAJASHREE NIGHT')
# get_chart_data('RAJLAXMI')
# get_chart_data('PUNA BAZAR')
# get_chart_data('MADHUR MORNING ')
# get_chart_data('MADHUR DAY')
# get_chart_data('MADHUR NIGHT')
# get_chart_data('RATAN KHATRI')
# get_chart_data('NEW COUNTRY BAZAR')
# get_chart_data('SRIDEVI   [ main ]')
# get_chart_data('SRIDEVI   [ main ] NIGHT')
# get_chart_data('NEW MAIN MUMBAI')
# get_chart_data('KBC DAY')
# get_chart_data('SAPNA DAY')
# get_chart_data('MAIN MUMBAI RK')
# get_chart_data('MATKA KING DAY')
# get_chart_data('MATKA KING NIGHT')
# get_chart_data('SRI STAR NIGHT')
# get_chart_data('RATAN DAY')
# get_chart_data('RATAN NIGHT')
# get_chart_data('KALYAN BAZAR')
# get_chart_data('NEW BOMBAY')
# get_chart_data('JODI BAZAR')
# get_chart_data('GUJRAT')
# get_chart_data('GUJRAT NIGHT')
# get_chart_data('MAIN GOA')
# get_chart_data('JANTA MORNING')
# get_chart_data('WORLI MUMBAI')
# get_chart_data('MAIN MUMBAI NIGHT')
# get_chart_data('BABY DAY')
# get_chart_data('BABY NIGHT')
# get_chart_data('STAR KALYAN')
# get_chart_data('SUPER MILAN NIGHT')
# get_chart_data('SUPREME DAY')
# get_chart_data('SUPREME NIGHT')
# get_chart_data('ROSE BAZAR DAY')
# get_chart_data('ROSE BAZAR NIGHT')
# get_chart_data('TIME BAZAR NIGHT [MAIN]')
# get_chart_data('CENTRAL BOMBAY')
# get_chart_data('PADMAVATI NIGHT')
# get_chart_data('MARUTI DAY')
# get_chart_data('MARUTI NIGHT')
# get_chart_data('KALYAN KBC')
#             # get_chart_data('MUMBAI NIGHT')
# get_chart_data('GOLDEN')
#             # get_chart_data('GOLDEN TIME')
# get_chart_data('OMI DAY')
# get_chart_data('MAHARASHTRA DAY')
# get_chart_data('MAHARASHTRA NIGHT')
#             # get_chart_data('DAYAWAN DAY')
#             # get_chart_data('JOCKER')
# get_chart_data('SUPER MATKA')
# get_chart_data('MUMBAI MARKET NIGHT')
# get_chart_data('KALYAN MARKET NIGHT')
# get_chart_data('MILAN MARKET DAY')
# get_chart_data('MILAN MARKET NIGHT')
# get_chart_data('BOMBAY RAJSHREE DAY')
# get_chart_data('BOMBAY RAJSHREE NIGHT')
#             # get_chart_data('DHANLAXMI DAY')
#             # get_chart_data('DHANLAXMI NIGHT')


# newJson={}
# newCsv=[]
# for key in satta.keys():
#     val={"game":key,'score': satta[key]['score'], 'start': satta[key]['start'], 'end': satta[key]['end'], 'jodi_link': satta[key]['jodi_link'], 'panel_link': satta[key]['panel_link']}
#     newCsv.append(val)

# df=spark.read.json(sc.parallelize([newCsv]))


# df=df.select("game","start","end")
# df.repartition(1).write.csv(path="/hdfsData/supply_chain/fulfillment/stgfiles/del", mode="overwrite", header="True")
