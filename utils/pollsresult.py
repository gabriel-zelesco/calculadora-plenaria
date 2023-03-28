

class PollsResult():
    def __init__(self, votes, n_seats, abstention=True, sort='asc'):
        
        self.sort = sort
        self.abstention = abstention
        self.n_seats = n_seats
        self.votes = self._sort_votes(votes)
        self.total = self._total_votes()
        self.valid = self._valid_votes()
            
    
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
    n_seats = 8
    votes = {'a':168,'b':233,'c':72,'d':64,'e':40, 'abstention': 100}
    resultados = PollsResult(votes,n_seats)
    print(resultados.total)
    print(resultados.valid)