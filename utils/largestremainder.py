from heapq import nlargest # Used to get the n largest values from a dictionary

from utils.pollsresult import PollsResult


class LargestRemainder(PollsResult):
    def __init__(self):
        PollsResult.__init__(self)
        self.quota = self.__election_quota()
        self.party_quota = self.__party_quota()
        self.first_distribution = self.__quota_distribution()
        self.remaining_seats = self.n_seats - sum(self.first_distribution.values())
        self.remaining_distribution = self.__remaining_distribution()
        self.result = self.__result()
    
    def __election_quota(self):
        """Returns the election quota."""
        return self.used_votes / (self.n_seats)
    
    def __party_quota(self):
        """Returns the party quota."""
        party_quota = {}
        for key, value in self.votes.items():
           party_quota[key] = round((value / self.quota),3)
        return party_quota
    
    def __quota_distribution(self):
        """Returns the quota distribution."""
        distribution = {}
        for key, value in self.party_quota.items():
            distribution[key] = int(value)
        return distribution
    
    def __remaining_distribution(self):
        """Returns the remaining distribution."""
        quota_remaining = {key: self.party_quota[key] - self.first_distribution[key] \
                      for key in set(self.party_quota) & set(self.first_distribution)}
        # Get the largest remainders based on the remaining seats
        largest_remainders = nlargest(self.remaining_seats, quota_remaining, key=quota_remaining.get)
        
        # Create a dictionary with the distribution of the remaining seats
        remaining = {}
        for key in self.party_quota:
            if key in largest_remainders:
                remaining[key] = 1
            else:
                remaining[key] = 0
        return remaining
    
    def __result(self):
        """Sum the quota distribution and the remaining distribution
        to get the final result."""
        result = {}
        for key in self.first_distribution:
            result[key] = self.first_distribution[key] + self.remaining_distribution[key]
        return result



if __name__ == '__main__':
    resultados = LargestRemainder()
    
    print(f'n_seats: {resultados.n_seats}')
    print(f'valid_votes: {resultados.valid_votes}')
    print(f'total_votes: {resultados.total_votes}')
    print(f'quota: {resultados.quota}')
    print(f'votes: {resultados.votes}')
    print(f'party_quota: {resultados.party_quota}')
    print(f'first_distribution: {resultados.first_distribution}')
    print(f'remaining_seats: {resultados.remaining_seats}')
    print(f'remaining_distribution: {resultados.remaining_distribution}')
    print(f'result: {resultados.result}')
