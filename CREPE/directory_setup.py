### Dicrectory setup
import os
import sys


###### Date due to running
current_date = os.getenv('current_date')

##  Condition relate to bash setup

mode = sys.argv[1] if len(sys.argv) > 1 else 'Single_PWN'

if mode == 'Single_PWN':
    save_dir = f'./Results/{mode}/{current_date}'
    os.makedirs(save_dir, exist_ok=True)
    print(f"Created: {save_dir}")
elif mode == 'Multiple_PWNe':
    save_dir_Multi = f'./Results/{mode}/{current_date}'
    os.makedirs(save_dir_Multi, exist_ok=True)
    print(f"Created: {save_dir_Multi}")
