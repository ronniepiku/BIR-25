import gspread


def shareholder_yield(file_name, sh_name):
    gc = gspread.service_account(filename=file_name)
    sh = gc.open(sh_name)
    worksheet = sh.sheet1

    # Set the batch size
    batch_size = 60

    # Loop through the rows in batches of size batch_size
    for start_row in range(2, worksheet.row_count, batch_size):
        end_row = min(start_row + batch_size - 1, worksheet.row_count)

        # Get the batch of rows
        rows = worksheet.get(f'M{start_row}:N{end_row}')

        # Loop through each row in the batch and update the cell values
        body = []
        for i, row in enumerate(rows):
            value_m = row[0]  # Column J
            value_n = row[1]  # Column K

            # Check for n/a values
            if value_m == 'n/a' and value_n == 'n/a':
                value_sum = 'n/a'
            elif value_m == 'n/a':
                value_sum = float(value_n)
            elif value_n == 'n/a':
                value_sum = float(value_m)
            else:
                value_sum = float(value_m) + float(value_n)

            # Add the update request to the batch update body
            body.append({
                'range': f'O{start_row + i}',
                'values': [[value_sum]]
            })

        # Batch update the values
        worksheet.batch_update(body)
