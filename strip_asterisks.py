import csv
import pandas as pd

# def strip_asterisks(text):
#     return text.replace("*","")
    

# df = pd.read_csv("2020_team_per_game_stats.csv")
# df["Team"] = df["Team"].map(strip_asterisks)

# df.to_csv("2020_team_per_game_stats.csv")

file_name = "2019_team_per_game_stats.csv"

with open(file_name, "r") as in_file:
        reader = csv.reader(in_file, delimiter=',')
        
        all_rows = []
        for row in reader:
            row_elements = []
            for element in row:
                row_elements.append(element)
            row_elements[1] = row_elements[1].replace("*","")
            all_rows.append(row_elements)

# print(all_rows)

with open(file_name, "w") as out_file:
        writer = csv.writer(out_file, delimiter=',')
        for row in all_rows:
            writer.writerow(row)