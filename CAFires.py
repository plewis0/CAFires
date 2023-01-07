# need to add '-y 2022' arg to select year, filter


import sys, csv, urllib.request
from tabulate import tabulate

#import arguments
arg = sys.argv

#set up headers for table
headers = ['Name','County','Location','Acres Burned','% Contained','Latitude','Longitude','Start Date','Extinguished Date','Active?'] 

def get_data():
    #Set URL, grab contents
    url_data = urllib.request.urlopen('https://www.fire.ca.gov/imapdata/mapdataall.csv')
    lines = [l.decode('utf-8') for l in url_data.readlines()]
    fire_data = csv.reader(lines)
    return fire_data

def print_help():
    print("\nCAFire.py - a command line tool to scrape data from the CAL Fire website on current CA wildfires")
    print("\nUsage: CAFire.py [-h] [-a]")
    print("\nOptions:")
    print("\t-h\tDisplay this help menu.") 
    print("\t-a\tDisplay all fires, whether active or not. Default is to only show active fires.")


def clean_table(fires_list):
    #copy to new table, cut columns we don't want
    for i in range(len(fires_list)):
        temp_list = fires_list[i]
        
        #remove name descriptions > 20 characters, add ... if so
        temp_list[0] = (temp_list[0][0:20] + '...') if len(temp_list[0]) > 20 else temp_list[0]
        
        #remove county descriptions > 20 characters, add ... if so
        temp_list[6] = (temp_list[6][0:20] + '...') if len(temp_list[6]) > 20 else temp_list[6]
        
        #remove location descriptions > 40 characters, add ... if so
        temp_list[7] = (temp_list[7][0:40] + '...') if len(temp_list[7]) > 40 else temp_list[7]
        
        #only include the columns we want
        temp_list = temp_list[0].strip(),temp_list[6].strip(),temp_list[7].strip(),temp_list[8].strip(),temp_list[9].strip(),temp_list[12].strip(),temp_list[13].strip(),temp_list[19].strip(),temp_list[18].strip(),temp_list[20].strip()
        fires_list[i] = temp_list
    fires_list.pop(0) #remove column headers so we can re-add those from headers variable above
    return fires_list
    
def print_data(print_queue):
    #clean the data using clean_table() above
    final_print_list = clean_table(print_queue)
    
    #if greater than 20 entries split data and use 'ENTER' input from user to proceed
    if len(final_print_list) > 20:
        total_len = len(final_print_list) #get total length of list for count
        while len(final_print_list) > 20:   
            #create temp print list, populate with next 20 entries from final_print_list
            temp_print_list = []        
            for i in range(20):
                temp_print_list.append(final_print_list[i])
            
            #pull those 20 entries from final print list so no duplicate
            final_print_list = final_print_list[20:]
            
            #add headers in for printing
            temp_print_list.insert(0,headers)
            
            #print and wait for user input to proceed with next 20
            print("\n" + tabulate(temp_print_list, headers='firstrow', tablefmt='github'))
            print("\nEntries",total_len - len(final_print_list) - 20 + 1,"to",total_len - len(final_print_list) + 1,"out of",total_len + 1) #include count of entries
            input("\nPress ENTER to continue")
        
        final_print_list.insert(0,headers) #add headers for final print < 20
        print("\n" + tabulate(final_print_list, headers='firstrow', tablefmt='github'))
    
    #otherwise just print the damn thing    
    else:
        final_print_list.insert(0,headers) #add column headers
        print("\n" + tabulate(final_print_list, headers='firstrow', tablefmt='github'))


#main program
#print help menu if indicated
if "-h" in arg:
    print_help()  
elif "-a" in arg:
    fire_data = list(get_data())    
    print_queue = []
    for row in fire_data:
        print_queue.append(row)
    print_data(print_queue)
else:
    fire_data = list(get_data())    
    print_queue = []
    for row in fire_data:
        if row[20] != 'N':
            print_queue.append(row)
    print_data(print_queue)
                        
            


