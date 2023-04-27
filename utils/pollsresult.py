import json

class PollsResult():
    '''This class is responsible for getting the data from the polls.
    The data is get from the json files: votes.json, abstention.json,
    n_seats.json and options.json.
    This class is the only one that can access the json files and is the
    superclass of the classes that will be responsible for the calculations.'''
    
    def __init__(self):
        self.sort = self.__load_data('options.json').get('sort')
        self.n_seats = self.__get_n_seats()
        self.votes = self.__get_votes()
        self.abstention = self.__get_abstenion()
        self.valid_votes = self.__sum_votes()
        self.total_votes = self.valid_votes + self.abstention 
    
    def __load_data(self, file_name):
        with open(file_name, 'r') as f:
            return json.load(f)
        
    def __str_to_int(self, dict_):
        for key in dict_:
            dict_[key] = int(dict_[key])
        return dict_
    
    def __get_abstenion(self):
        abstention = (
            self
            .__str_to_int(self.__load_data('abstention.json'))
            .get('abstention')
        )
        return abstention
    
    def __save_data(self, file_name, data):
        with open(file_name, 'w') as f:
            json.dump(data, f)
    
    def __get_n_seats(self):
        n_seats = self.__str_to_int(self.__load_data('n_seats.json')).get('n_seats')
        if n_seats < 1:
            n_seats = 1
            self.__save_data('n_seats.json', {"n_seats": f'{n_seats}'})
        return n_seats
        
    
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
    
    def __get_votes(self):
        votes = self.__str_to_int(self.__load_data('votes.json'))
        votes = self.__sort_votes(votes)
        return votes

    def __sum_votes(self):
        return sum(self.votes.values())



if __name__ == '__main__':
    resultado = PollsResult()
    print(f'votes: {resultado.votes}')
    print(f'abstention: {resultado.abstention}')
    print(f'valid_votes: {resultado.valid_votes}')
    print(f'total_votes: {resultado.total_votes}')
    print(f'n_seats: {resultado.n_seats}')
    print(f'sort: {resultado.sort}')
    