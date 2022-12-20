import csv


class Trainer:
    def __init__(self, name):
        with open('trainer_data/' + name + '.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            status_by_id = {}
            for row in reader:
                id = int(row["pokemon_id"])
                candy_count = row["candy_count"]
                if candy_count:
                    row["candy_count"] = int(row["candy_count"])
                else:
                    row["candy_count"] = None
                status_by_id[id] = row
            self.status_by_id = status_by_id

    def is_caught(self, pokemon_id):
        if pokemon_id not in self.status_by_id:
            return False
        data = self.status_by_id[pokemon_id]
        status = data["status"]
        if status == '':
            return False
        if status == 'X':
            return True
        if status == 'Caught':
            return True
        if status == 'Missing':
            return False
        print("Unknown trainer status", pokemon_id, status)
        assert False

    def normalize_status(self):
        for data in self.status_by_id.values():
            if data["status"] == "":
                data["status"] = "Caught"

    def save(self, name):
        with open('trainer_data/' + name + '.csv', 'w', newline='') as csvfile:
            fieldnames = ['pokemon_id', 'form', 'candy_count', 'status']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            self.normalize_status()
            for row in self.status_by_id.values():
                writer.writerow({k: v for k, v in row.items() if k in fieldnames})