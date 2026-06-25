import pickle
from datetime import datetime
from pathlib import Path

from whittle.game import generate_whittle


def generate_n_whittles(amount):
    print('Generating whittles')
    script_dir = Path(__file__).resolve().parent
    directory = script_dir / 'out'
    f_name = f'gen_whittles_{datetime.today().strftime('%Y-%m-%d')}_count_{amount}'
    full_path = directory / f_name

    Path(directory).mkdir(parents=True, exist_ok=True)

    whittles = []
    for i in range(amount):
        print(i)
        whittles.append(generate_whittle())

    with open(full_path, 'ab') as f:
        pickle.dump(whittles, f)
        print('{amount} Whittles generated as pickle objects. Path: {full_path}')


if __name__ == '__main__':
    generate_n_whittles(98)


        