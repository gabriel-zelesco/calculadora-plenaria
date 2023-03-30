from pollsresult import PollsResult
from largestremainder import LargestRemainder
  

class DhontMethod(PollsResult):
    '''D'Hondt method for the distribution of seats.
    
    votes: dictionary with the votes of each party.
    
    n_seats: number of seats to distribute.
    
    abstention: if True, it counts the abstention votes in the total.
    
    largest_remainder: if True, it uses the largest remainder method to
    establish the limit of seats for each party.
    '''
    
    def __init__(self, votes, n_seats, abstention=True, largest_remainder=False):
        PollsResult.__init__(self, votes, n_seats, abstention)
        self.largest_remainder = largest_remainder
        self.votes = votes
        self.limit = LargestRemainder(votes, n_seats, abstention).result
        self.seats = self._set_seats_dic()
        self.cumulative_order = self._set_cumulative_dic()
        self.order = []
        self.round = self.valid.copy()
        self.tie = self._set_cumulative_dic(value='')
        self.limit_check = self._set_cumulative_dic(value='')
        self.report = self._set_report()

        
    def _set_seats_dic(self, value=0):
        """Returns a dictionary for the seats of each party."""
        seats = {}
        for key in self.valid:
            seats[key] = value
        return seats
        
    def _set_report(self):
        """Returns a dictionary for the report of each round."""
        report = {}
        for i in range(1, self.n_seats + 1):
            report[i] = {}
        return report
    
    def _set_cumulative_dic(self, value=0):
        """Returns a dictionary for the cumulative order of each round."""
        cumulative_dic = {}
        for i in range(1, self.n_seats + 1):
            cumulative_dic[i] = self._set_seats_dic(value)
        return cumulative_dic       
    
    
    def _check_tie(self, max_votes, call):
        """Checks if there is a tie in the votes."""
        tie_list = []
        if list(self.round.values()).count(max_votes) > 1:
            tie_list = [k for k, v in self.round.items() if v == max_votes]
        for party in self.tie[1].keys():
            if party in tie_list:
                self.tie[call][party] = 'EMPATE'
            else:
                self.tie[call][party] = ''
   
    def _check_limit(self, call):
        """Checks if the party has reached the limit."""
        for party in self.seats.keys():
            if self.seats[party] >= self.limit[party]:
                self.round[party] = 0
                self.limit_check[call][party] = 'LIMITE'
            else:
                self.limit_check[call][party] = ''
        

    def dhont(self):
        """
        n_seats is the number of seats.
        self.round is a dictionary with the votes of each party for each round.
        self.order is a list with the order of the calls.
        self.seats is a dictionary with the final result.
        """
        
        for call in range(1, self.n_seats + 1):
            if self.largest_remainder:
                self._check_limit(call)
            
            max_votes = max(self.round.values())
            
            self._check_tie(max_votes, call)

            party = list(self.round.keys())[list(self.round.values()).index(max_votes)]      
            
            self.seats[party] += 1
            self.cumulative_order[call]= self.seats.copy()
            self.order.append(party)
            self.report[call][party] = self.round.copy()
            self.round[party] = self.valid[party] / (self.seats[party] + 1)
        return self.seats

    def print_report(self):
        """Prints the report of each round."""
        for call in self.report:
            print(f"{call}º call: {self.order[call-1]}")
            for party in self.report[call][self.order[call-1]]: 
                text = f"""\t{party}[{self.cumulative_order[call][party]}]: \
{self.report[call][self.order[call-1]][party]:.2f} \
    {self.tie[call][party]} \
    {self.limit_check[call][party]}"""
                print(text)  
            print("\b")
    
if __name__ == '__main__':
    n_seats = 8
    votes = {'a':200,'b':72,'c':72,'d':64,'e':40, 'abstention': 30}
    resultados = DhontMethod(votes,n_seats, largest_remainder=True)
    resultados.dhont()
    resultados.print_report()
    print(dir(resultados))