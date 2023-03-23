

class PollsResult():
    def __init__(self, votes, n_seats, abstention=True):
        
        self.votes = votes
        self.abstention = abstention
        self.n_seats = n_seats
        self.total = self._total_votes()
        self.valid = self._valid_votes()
            
        
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
    
    # TODO: sort the valid votes from the highest to the lowest or viceversa.

if __name__ == '__main__':
    n_seats = 8
    votes = {'a':168,'b':104,'c':72,'d':64,'e':40, 'abstention': 100}
    resultados = PollsResult(votes,n_seats)
    print(resultados.total)
    print(resultados.valid)
    