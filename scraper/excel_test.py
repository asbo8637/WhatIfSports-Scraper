from excel_creator import excel_editor

excel = excel_editor()


data = [["UAB", "Sim AI", "DI", "B+", "Very High", "Yes"], ["UAB", "coach1", "DI", "B+", "Very High", "Yes"], ["UAB", "coach1", "DI", "B+", "Very High", "Yes"], ["UAB", "coach2", "DII", "B+", "Very High", "Yes"]]
excel.add_player("Tom", "Tester", 30, "CO", 'A', 'A', "A", "13", "T", data)
excel.print_players()
excel.create_sheet()