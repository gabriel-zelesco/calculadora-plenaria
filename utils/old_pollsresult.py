
class PollsResult():
    def __init__(self, votes, n_seats, abstention=True, sort='asc'):
        
        self.sort = sort
        self.abstention = abstention
        self.n_seats = self._str_to_int(n_seats).get('n_places')
        self.votes = self._format_votes(votes)
        self.total = self._total_votes()
        self.valid = self._valid_votes()
    
    def _str_to_int(self, data_dic):
        """Converts the votes from string to integer."""
        for key in data_dic:
            data_dic[key] = int(data_dic[key])
        return data_dic
    
    def _sort_votes(self, votes):
        """Sort the votes from the highest to the lowest or viceversa."""
        if self.sort == 'desc':
            ordered_votes = sorted(votes.items(), key=lambda x:x[1], reverse=True)
            return dict(ordered_votes)
        elif self.sort == 'asc':
            ordered_votes = sorted(votes.items(), key=lambda x:x[1], reverse=False)
            return dict(ordered_votes)
        elif self.sort == None:
            return votes
        else:
            raise ValueError("The sort parameter must be 'desc' or 'asc'.")
        
    def _format_votes(self, votes):
        votes = self._str_to_int(votes)
        votes = self._sort_votes(votes)
        return votes
    
    def _total_votes(self):
        """
        Returns the total number of votes.
        If abstention is True, it counts the abstention votes in the total.
        """
        if self.abstention:
            return sum(self.votes.values())
        else:
            return sum(self.votes.values()) - self.votes['abstention']
        
    def _valid_votes(self):
        """Returns a dictionary with the valid votes
        which are the votes without the abstention votes.
        """
        valid = self.votes.copy()
        del valid['abstention']
        return valid
    

if __name__ == '__main__': 
    n_seats = {"n_places": "10"}
    votes = {"chapa1": "30", "chapa3": "52", "abstention": "12", "chapa4": "45", "chapa5": "100", "chapa2": "60"}
    resultados = PollsResult(votes,n_seats)
    print(resultados.total)
    print(resultados.valid)
    print(resultados.n_seats)