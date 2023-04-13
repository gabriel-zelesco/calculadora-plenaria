from heapq import nlargest

from utils.pollsresult import PollsResult

class LargestRemainder(PollsResult):
    def __init__(self, votes, n_seats, abstention=True):
        PollsResult.__init__(self, votes, n_seats, abstention)
        self.quota = self._election_quota()
        self.party_quota = self._party_quota()
        self.first_distribution = self._quota_distribution()   
        self.remaining_seats = self.n_seats - sum(self.first_distribution.values())
        self.remaining_distribution = self._remaining_distribution()
        self.result = self._result()
            
    def _election_quota(self):
        """Returns the election quota."""
        return self.total / (self.n_seats)
    
    def _party_quota(self):
        """Returns the party quota."""
        party_quota = {}
        for key, value in self.valid.items():
           party_quota[key] = value / self.quota
        return party_quota
    
    def _quota_distribution(self):
        """Returns the quota distribution."""
        distribution = {}
        for key, value in self.party_quota.items():
            distribution[key] = int(value)
        return distribution
    
    def _remaining_distribution(self):
        """Returns the remaining distribution."""
        quota_remaining = {key: self.party_quota[key] - self.first_distribution[key] \
                      for key in set(self.party_quota) & set(self.first_distribution)}
        largest_remainders = nlargest(self.remaining_seats, quota_remaining, key=quota_remaining.get)
        
        remaining = {}
        for key in self.party_quota:
            if key in largest_remainders:
                remaining[key] = 1
            else:
                remaining[key] = 0
        
        return remaining
    
    def _result(self):
        """Sum the quota distribution and the remaining distribution
        to get the final result."""
        result = {}
        for key in self.first_distribution:
            result[key] = self.first_distribution[key] + self.remaining_distribution[key]
        return result
        


if __name__ == '__main__':
    n_seats = 8
    votes = {'a':200,'b':400,'c':72,'d':64,'e':40, 'abstention': 30}
    resultados = LargestRemainder(votes,n_seats)
    print(resultados.first_distribution)
    print(resultados.remaining_distribution)
    print(resultados.result)