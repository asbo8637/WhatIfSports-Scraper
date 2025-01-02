import pandas as pd


class excel_editor:
    def read_considering(self):
        



# Create a DataFrame
data = {
    "ID": [1, 2, 3],
    "Name": ["Alice", "Bob", "Charlie"],
    "Age": [25, 30, 35]
}
df = pd.DataFrame(data)

# Save the DataFrame to an Excel file
df.to_excel("example.xlsx", index=False)

print("Excel file created: example.xlsx")
