from collections import defaultdict as dd
import csv

class Store:
    def __init__(self):
        # read in data inputs and store them
        self.params = None
        
        # initialize empty variables for data frames
        self.teams, self.products, self.sales= [], [], []
        
        # initialize output data frames
        self.teamreport, self.productreport = dd(int), dd(dict)
    
    def __readvars(self):
        # read arguments in from command line
        import argparse 
        parser = argparse.ArgumentParser()
        parser.add_argument('-t', help='path to teams.csv')
        parser.add_argument('-p', help='path to products.csv')
        parser.add_argument('-s', help='path to sales.csv')
        parser.add_argument('--team-report', help='path to team-report.csv')
        parser.add_argument('--product-report', help='path to product-report.csv')
        self.params = vars(parser.parse_args())
    
    def __readdata(self):
        # read in csv data
        with open(self.params['t'], 'r') as file:
            my_reader = csv.reader(file, delimiter=',')
            header = True
            for row in my_reader:
                if header:
                    header=False
                    continue
                self.teams.append((int(row[0]), row[1]))
            
        with open(self.params['p'], 'r') as file:
            my_reader = csv.reader(file, delimiter=',')
            for row in my_reader:
                self.products.append((int(row[0]), row[1], float(row[2]), int(row[3])))
                
        with open(self.params['s'], 'r') as file:
            my_reader = csv.reader(file, delimiter=',')
            for row in my_reader:
                self.sales.append((int(row[0]), int(row[1]), int(row[2]), int(row[3]), float(row[4])))
       
        # convert to dict for easy access
        self.teams = dict([(i,n) for i,n in self.teams])
        self.products = dict([(i,[n,p,l]) for i,n,p,l in self.products])

    def __build_reports(self):
        for sid,pid,tid,q,d in self.sales:
            # calculate revenue
            revenue = self.products[pid][1] * q * (1-(d/100.0))
            
            # update team report
            self.teamreport[self.teams[tid]] += revenue
            
            # update product report
            if pid not in self.productreport:
                self.productreport[self.products[pid][0]] = {'GrossRevenue': revenue, 'TotalUnits': q, 'DiscountCost': d}
            else:
                self.productreport[self.products[pid][0]]['GrossRevenue'] += revenue
                self.productreport[self.products[pid][0]]['TotalUnits'] += q
                self.productreport[self.products[pid][0]]['DiscountCost'] += d
   
    def __write_reports(self):
        # sort reports and convert to data frames
        self.teamreport = sorted(self.teamreport.items(), key=lambda x: x[1], reverse=True)
        self.productreport = sorted([tuple([key]+list(self.productreport[key].values())) for key in self.productreport],key=lambda x: x[1],reverse=True)
        
        # write reports to csv
        with open(self.params['team_report'], 'w') as file:
            file.write('Team' + ',' + 'Revenue'+'\n')
            for n,r in self.teamreport:
                file.write(n+','+str(r)+'\n')
        
        with open(self.params['product_report'], 'w') as file:
            file.write('Product' + ',' + 'GrossRevenue' + ',' + 'TotalUnits' + ',' + 'DiscountCost'+'\n')
            for n,r,u,d in self.productreport:
                file.write(n+','+str(r)+','+str(u)+','+str(d)+'\n')
    
    def analyzesales(self):
        # create public method to invoke all functions 
        self.__readvars()
        self.__readdata()
        self.__build_reports()
        self.__write_reports()
        
if __name__ == '__main__':
    report = Store()
    report.analyzesales()

            
        
        
        

    