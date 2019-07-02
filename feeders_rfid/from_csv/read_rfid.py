import csv

# must have header

def read_rfid (fname):
    with open(fname) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            tag, antenna = row['TAG'], row['ANTENNA']
            # print (antenna)
            return tag, antenna

if __name__ == "__main__":
    # fname = 'filename2.csv'
    # tag, antenna = read_rfid (fname)
    # if antenna == '102':
    #     print ("yes")