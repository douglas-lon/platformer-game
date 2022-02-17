from csv import reader

def import_csv(path):
    layout = []
    with open(path) as csv_file:
        map = reader(csv_file,  delimiter=',')
        for row in map:
            layout.append(list(row))
        return layout
    
