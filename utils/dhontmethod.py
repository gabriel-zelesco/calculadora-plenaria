from utils.pollsresult import PollsResult
from utils.largestremainder import LargestRemainder
  

class DhontMethod(PollsResult):
    '''D'Hondt method for the distribution of seats.
    
    votes: dictionary with the votes of each party.
    
    n_seats: number of seats to distribute.
    
    abstention: if True, it counts the abstention votes in the total.
    
    proportional_limit: if True, it uses the largest remainder method to
    establish the limit of seats for each party.
    '''
    
    def __init__(self,):
        PollsResult.__init__(self)
        self.limit = LargestRemainder().result
        self.rounds = range(1, self.n_seats + 1)
        self.round_report = {}
        self.dhont()        
        self.seats = self.round_report[self.n_seats]['seats']
        self.call_list = self.__generate_call_list()
        

    def __set_tie_dic(self):
        """Returns an empty dictionary for the tie"""
        tie_dic = {}
        for party in self.parties:
            tie_dic[party] = ''
        return tie_dic
    
    def __set_limit_dic(self):
        """Returns an empty dictionary for the limit"""
        limit_dic = {}
        for party in self.parties:
            limit_dic[party] = ''
        return limit_dic
       
    
    def __set_rounds_report(self):
        '''
        Returns an empty dictionary for the rounds report
        The round_report is a dictionary of dictionaries
        '''       
        seats_dic = {}
        for party in self.parties:
            seats_dic[party] = 0
        
        tie_dic = self.__set_tie_dic()            
        limit_dic = self.__set_limit_dic()
            
        round = {'votes': self.votes.copy(),
                 'next_votes': self.votes.copy(),
                 'seats': seats_dic.copy(),
                 'tie': tie_dic.copy(),
                 'limit': limit_dic.copy(),
                 'winner': ''}
            
        return round
            
    def __set_dhont_variables(self, call, round_report):
            _votes = round_report[call-1]['next_votes'].copy()
            _next_votes = _votes.copy()
            _seats = round_report[call-1]['seats'].copy()
            _tie = self.__set_tie_dic()
            _limit = self.__set_limit_dic()
            return (_votes, _next_votes, _seats, _tie, _limit)
        
    def __check_tie(self, max_parties, tie):
        """Check if there is a tie."""
        if len(max_parties) > 1:
            for party in max_parties:
                tie[party] = 'tie'
        return tie
        
    def __check_limit(self, call):
        """Check if the party has reached the limit."""
        for party, seats in zip(
            self.round_report[call]['seats'],
            self.round_report[call]['seats'].values()):
            
            if seats >= self.limit[party]:
                self.round_report[call]['limit'][party] = 'limit'
                self.round_report[call]['next_votes'][party] = 0
    
    
    def dhont(self):
        """Returns a dictionary with the seats for each party."""
        #round_report = {}
        for call in self.rounds:
            if call == 1:
                self.round_report[call-1] = self.__set_rounds_report()
            
            _votes, _next_votes, _seats, _tie, _limit = \
                self.__set_dhont_variables(call, self.round_report)
            
            
            max_votes = max(_votes.values())
            max_parties = [k for k, v in _votes.items() if v == max_votes]
            # Check if there is a tie
            _tie = self.__check_tie(max_parties, _tie)
                        
            party = max_parties[0] # If there is a tie, the first party wins
            
            _seats[party] += 1
            _next_votes[party] = round(
                _next_votes[party] / (_seats[party] + 1), 3)
            
            # Save the results of the round
            self.round_report[call] = {'votes': _votes.copy(),
                                  'next_votes': _next_votes.copy(),
                                  'seats': _seats.copy(),
                                  'tie': _tie.copy(),
                                  'limit': _limit.copy(),
                                  'winner': party}
            
            # Check if the party has reached the limit
            if self.proportional_limit == 'True':
                self.__check_limit(call)
            


    def __generate_call_list(self):
        ordered_calls = {}
        for call in self.rounds:
            ordered_calls[call] = self.round_report[call]['winner']
        return ordered_calls
    
    def print_report(self):
        for call in self.round_report.keys():
            print(f'Round {call}: {self.round_report[call]["winner"]}')
            for party in self.parties:
                print(f'{party}: {self.round_report[call]["votes"][party]}',
                      f' {self.round_report[call]["tie"][party]}', 
                      f'[{self.round_report[call]["seats"][party]}]',
                      f' {self.round_report[call]["limit"][party]}')
            print('\n')
                


if __name__ == '__main__':
    resultados = DhontMethod()
    print(resultados.print_report())
    print(resultados.call_list)








