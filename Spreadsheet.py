import gspread
import subprocess


def spreadsheet(file_name, sh_name):
    gc = gspread.service_account(filename=file_name)
    sh = gc.open(sh_name)
    worksheet = sh.sheet1
    all_values = worksheet.get_all_values()[1:]
    picks = []

    def price_book():
        sort_ptb = sorted(all_values, key=lambda x: float(x[2]) if x[2] != "n/a" else 0, reverse=True)
        updates = []
        n = 6  # Number of values per score
        score = 1  # Initial score

        for i, row in enumerate(sort_ptb):
            original_index = all_values.index(row) + 2
            if row[2] == "n/a":
                updates.append({
                    'range': f'D{original_index}',
                    'values': [[50]]
                })
            else:
                updates.append({
                    'range': f'D{original_index}',
                    'values': [[score]]
                })

            if (i + 1) % n == 0:  # Check if the current index is a multiple of n
                score += 1  # Increment the score

        worksheet.batch_update(updates)

    def price_earnings():
        sort_pte = sorted(all_values, key=lambda x: float(x[4].replace(',', '')) if x[4] != "n/a" else 0, reverse=True)
        updates = []
        n = 5  # Number of values per score
        score = 1  # Initial score

        for i, row in enumerate(sort_pte):
            original_index = all_values.index(row) + 2  # Shifted down one row
            if row[4] == "n/a":
                updates.append({
                    'range': f'F{original_index}',
                    'values': [[50]]
                })
            else:
                updates.append({
                    'range': f'F{original_index}',
                    'values': [[score]]
                })

            if (i + 1) % n == 0:  # Check if the current index is a multiple of n
                score += 1  # Increment the score

        worksheet.batch_update(updates)

    def price_sales():
        sort_pts = sorted(all_values, key=lambda x: float(x[6].replace(',', '')) if x[6] != "n/a" else 0, reverse=True)
        updates = []
        n = 6  # Number of values per score
        score = 1  # Initial score

        for i, row in enumerate(sort_pts):
            original_index = all_values.index(row) + 2  # Shifted down one row
            if row[6] == "n/a":
                updates.append({
                    'range': f'H{original_index}',
                    'values': [[50]]
                })
            else:
                updates.append({
                    'range': f'H{original_index}',
                    'values': [[score]]
                })

            if (i + 1) % n == 0:  # Check if the current index is a multiple of n
                score += 1  # Increment the score

        worksheet.batch_update(updates)

    def ebitda():
        sort_e = sorted(all_values, key=lambda x: float(x[8].replace(',', '')) if x[8] != "n/a" else 0, reverse=True)
        updates = []
        n = 5  # Number of values per score
        score = 1  # Initial score

        for i, row in enumerate(sort_e):
            original_index = all_values.index(row) + 2  # Shifted down one row
            if row[8] == "n/a":
                updates.append({
                    'range': f'J{original_index}',
                    'values': [[50]]
                })
            else:
                updates.append({
                    'range': f'J{original_index}',
                    'values': [[score]]
                })

            if (i + 1) % n == 0:  # Check if the current index is a multiple of n
                score += 1  # Increment the score

        worksheet.batch_update(updates)

    def price_cash():
        sort_cash = sorted(all_values,
                           key=lambda x: float(x[10].replace(',', '')) if x[10] != "n/a" else 0, reverse=True)
        updates = []
        n = 5  # Number of values per score
        score = 1  # Initial score

        for i, row in enumerate(sort_cash):
            original_index = all_values.index(row) + 2  # Shifted down one row
            if row[10] == "n/a":
                updates.append({
                    'range': f'L{original_index}',
                    'values': [[50]]
                })
            else:
                updates.append({
                    'range': f'L{original_index}',
                    'values': [[score]]
                })

            if (i + 1) % n == 0:  # Check if the current index is a multiple of n
                score += 1  # Increment the score

        worksheet.batch_update(updates)

    def s_yield():
        sort_yield = sorted(all_values, key=lambda x: float(x[14].replace(',', '')) if x[14] != "n/a" else 0)
        updates = []
        n = 3  # Number of values per score
        score = 1  # Initial score

        for i, row in enumerate(sort_yield):
            original_index = all_values.index(row) + 2  # Shifted down one row
            if row[14] == "n/a":
                updates.append({
                    'range': f'P{original_index}',
                    'values': [[50]]
                })
            else:
                updates.append({
                    'range': f'P{original_index}',
                    'values': [[score]]
                })

            if (i + 1) % n == 0:  # Check if the current index is a multiple of n
                score += 1  # Increment the score

        worksheet.batch_update(updates)

    def calculate_sum():
        updates = []

        for i, row in enumerate(all_values):
            values = [row[3], row[5], row[7], row[9], row[11], row[15]]
            row_sum = sum(float(value) for value in values)

            updates.append({
                'range': f'Q{i+2}',  # Adjust the range accordingly
                'values': [[row_sum]]
            })

        worksheet.batch_update(updates)

    def decile():
        sort_rank = sorted(all_values, key=lambda x: float(x[16]) if x[16] != "n/a" else 0, reverse=True)
        updates = []
        n = 60  # Number of values per score
        score = 1  # Initial score

        for i, row in enumerate(sort_rank):
            original_index = all_values.index(row) + 2
            updates.append({
                'range': f'R{original_index}',
                'values': [[score]]
            })
            if (i + 1) % n == 0:  # Check if the current index is a multiple of n
                score += 1  # Increment the score

        worksheet.batch_update(updates)

    def result():
        nonlocal picks
        sort_decile = sorted(all_values, key=lambda x: float(x[17]) if x[17] != "n/a" else 0)
        decile_1 = [row for row in sort_decile if row[17] == '1.00']
        sort_momentum = sorted(decile_1, key=lambda x: float(x[18]) if x[18] != "n/a" else 0, reverse=True)
        temp_picks = sort_momentum[:35]

        for row in temp_picks:
            company_name = row[0]
            ticker = row[1]
            if row[18] != "n/a":
                value_s = str(float(row[18].replace('%', '')) * 100) + '%'
            else:
                value_s = "N/A"
            print(f"{company_name}, {ticker}, {value_s}")
            # Append picks to the list
            picks.append([company_name, ticker, value_s])

    price_book()
    price_earnings()
    price_sales()
    ebitda()
    price_cash()
    s_yield()
    calculate_sum()
    decile()
    result()

    with open(f'{sh_name}.txt', 'w') as txtfile:
        txtfile.write('Company Name                                Ticker   Momentum Value\n')
        txtfile.write('----------------------------------------------------------------------------------\n')

        for row in picks:
            company_name = row[0]
            ticker = row[1]
            value_s = row[2]
            txtfile.write(f'{company_name:45}{ticker:8}{value_s}\n')

    subprocess.run(['start', f'{sh_name}.txt'], shell=True)