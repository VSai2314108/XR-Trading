import pandas as pd
from collections import defaultdict as dd

class Store:
    def __init__(self):
        # read in data inputs and store them
        self.params = None
        
        # initialize empty variables for data frames
        self.teams, self.products, self.sales= None, None, None
        
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
        self.teams = pd.read_csv(self.params['t'])
        self.products = pd.read_csv(self.params['p'], names=['ProductId', 'Name', 'Price', 'LotSize'])
        self.sales = pd.read_csv(self.params['s'], names=['SaleID', 'ProductID', 'TeamID', 'Quantity', 'Discount'])
        
        # convert to dict or list
        self.teams = dict([(i,n) for i,n in zip(self.teams.TeamId, self.teams.Name)])
        self.products = dict([(i,[n,p,l]) for i,n,p,l in zip(self.products.ProductId, self.products.Name, self.products.Price, self.products.LotSize)])
        self.sales = list((s,p,t,q,d) for s,p,t,q,d in zip(self.sales.SaleID, self.sales.ProductID, self.sales.TeamID, self.sales.Quantity, self.sales.Discount))

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
        self.teamreport = pd.DataFrame(sorted(self.teamreport.items(), key=lambda x: x[1], reverse=True), columns=['Team', 'Revenue'])
        self.productreport = pd.DataFrame(sorted([tuple([key]+list(self.productreport[key].values())) for key in self.productreport],key=lambda x: x[1],reverse=True), columns=['Product', 'GrossRevenue', 'TotalUnits', 'DiscountCost'])
        
        # write data frames to csv output files
        self.productreport.to_csv(self.params['product_report'], index=False)
        self.teamreport.to_csv(self.params['team_report'], index=False)
    
    def analyzesales(self):
        # create public method to invoke all functions 
        self.__readvars()
        self.__readdata()
        self.__build_reports()
        self.__write_reports()
        
if __name__ == '__main__':
    report = Store()
    report.analyzesales()

            
        
        
        

    