from utils.dhontmethod import DhontMethod

n_seats = 10
votes = {"chapa1": "210", "chapa2": "345", "chapa3": "415", "chapa4": "100", "chapa5": "555", "chapa6": "123", "abstention": "0"}
resultados = DhontMethod(votes,n_seats, largest_remainder=True)
resultados.dhont()
#resultados.print_report()
print(resultados.seats)
print(resultados.text_report())