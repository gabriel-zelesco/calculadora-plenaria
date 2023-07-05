import json

class PollsResult():
    '''This class is responsible for getting the data from the polls.
    The data is get from the json files: votes.json, abstention.json,
    n_seats.json and options.json.
    This class is the only one that can access the json files and is the
    superclass of the classes that will be responsible for the calculations.'''
    
    def __init__(self):
        self.data = self.__load_data('data.json')
        
        self.sort = self.data['sort']
        self.abstention_as_valid = self.data['abstention_as_valid']
        self.n_seats = self.__check_n_seats() 
        self.votes = self.__get_votes(self.data['votes'])
        self.abstention = int(self.data['abstention'])
        self.proportional_limit = self.data['proportional_limit']
        self.parties = self.__get_parties()
        self.valid_votes = self.__sum_votes()
        self.total_votes = self.valid_votes + self.abstention 
        self.used_votes = self.__get_used_votes()
        self.message = self.__make_message()
        
    
    def __check_n_seats(self):
        if int(self.data['n_seats']) < 1:
            self.data['n_seats'] = "1"
            self.data['warning_n_seats'] = ['n_seats must be greater than 0.']
            self.__save_data('data.json', self.data)
            return 1
        else:
            if 'warning_n_seats' in self.data:
                self.data.pop("warning_n_seats")
                self.__save_data('data.json', self.data)
        return int(self.data['n_seats'])
            
    
    def __str_to_int(self,dict_):
        for key in dict_:
            dict_[key] = int(dict_[key])
        return dict_

    def __sort_votes(self, votes):
        if self.sort == 'desc':
            ordered_votes = sorted(
                votes.items(),
                key=lambda x:x[1],
                reverse=True
            )
            return dict(ordered_votes)
        elif self.sort == 'asc':
            ordered_votes = sorted(
                votes.items(),
                key=lambda x:x[1],
                reverse=False
            )
            return dict(ordered_votes)
        elif self.sort == None:
            return votes
        else:
            raise ValueError("The sort parameter must be 'desc' or 'asc'.")

    def __get_votes(self, votes):
        votes = self.__str_to_int(votes)
        votes = self.__sort_votes(votes)
        return votes
    
    def __sum_votes(self):
        return sum(self.votes.values())
    
    def __get_used_votes(self):
        if self.abstention_as_valid == "True":
            return self.total_votes
        elif self.abstention_as_valid == "False":
            return self.valid_votes
        else:
            raise ValueError("The abstention_as_valid parameter must be \
                             'True' or 'False' as string.")

    def __load_data(self, file_name):
        with open(file_name, 'r') as f:
            return json.load(f)
        
    def __save_data(self, file_name, data):
        with open(file_name, 'w') as f:
            json.dump(data, f)
    
    def __get_parties(self):
        return list(self.votes.keys())
    
    def __make_message(self):
        if self.valid_votes == 0:
            return "There are no valid votes."
        elif self.parties == []:
            return "There are no parties."
        elif self.used_votes == 0:
            return "There are no used votes."
        elif self.data['votes'] == {}:
            return "There are no votes."
        else:
            return None
                
        


if __name__ == '__main__':
    resultado = PollsResult()
    print(f'votes: {resultado.votes}')
    print(f'abstention_as_valid: {type(resultado.abstention_as_valid)}')
    print(f'abstention: {resultado.abstention}')
    print(f'valid_votes: {resultado.valid_votes}')
    print(f'total_votes: {resultado.total_votes}')
    print(f'n_seats: {resultado.n_seats}')
    print(f'sort: {resultado.sort}')
    print(f'used_votes: {resultado.used_votes}')
    print(f'proportional_limit: {resultado.proportional_limit}')
    print(f'parties: {resultado.parties}')
    print(f'message: {resultado.message}')
    

    