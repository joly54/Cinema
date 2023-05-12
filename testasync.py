from datetime import datetime

date1 = '2023.05.08'
date2 = '2023.05.09'

date1_obj = datetime.strptime(date1, '%Y.%m.%d')
date2_obj = datetime.strptime(date2, '%Y.%m.%d')

if date1_obj > date2_obj:
    print(f'{date1} is greater than {date2}')
else:
    print(f'{date2} is greater than {date1}')