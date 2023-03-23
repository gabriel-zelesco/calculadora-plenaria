from heapq import nlargest

from pollsresult import PollsResult

class LargestRemainder(PollsResult):
    def __init__(self, votes, n_seats, abstention=True):
        PollsResult.__init__(self, votes, n_seats, abstention)
        self.quota = self._election_quota()
        self.party_quota = self._party_quota()
        self.distribution = self._quota_distribution()   
        self.remaining_seats = self.n_seats - sum(self.distribution.values())
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
        quota_remaining = {key: self.party_quota[key] - self.distribution[key] \
                      for key in set(self.party_quota) & set(self.distribution)}
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
        for key in self.distribution:
            result[key] = self.distribution[key] + self.remaining_distribution[key]
        return result
        


if __name__ == '__main__':
    n_seats = 8
    votes = {'a':168,'b':104,'c':72,'d':64,'e':40, 'abstention': 30}
    resultados = LargestRemainder(votes,n_seats)
    print(resultados.total)
    print(resultados.valid)
    print(resultados.quota)
    print(resultados.party_quota)
    print(resultados.distribution)
    print(resultados.remaining_seats)
    print(resultados.remaining_distribution)
    print(resultados.result)