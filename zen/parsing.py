import shlex
import subprocess
from conf import path

def parse_trades(stuff):
    """
    >>> parse_trades("1 trades over 17 days (avg 0.06 trades/day)")
    '0.06'
    :param stuff:
    :return:
    """
    return stuff.split(b'avg')[-1].strip().split()[0]


def args_for_strategy(strat):
    available = subprocess.check_output(shlex.split(f'{path}/zenbot.sh list-strategies'))
    strats = [strat.strip() for strat in available.split(b'\n\n')]
    groups = [group.splitlines() for group in strats]
    output = {split[0].split()[0]: split[1:] for split in groups if split}
    result = {strategy: [(line.strip().strip(b'-').split(b'=')[0], line.split(b':')[-1].strip().split(b'auto)')[0].split(b'm)')[0].split(b')')[0])
    for line in lines if b'--' in line] for strategy, lines in output.items()}
    result = {key.decode(): [map(lambda p: p.decode(), p) for p in val] for key, val in result.items()}
    return result[strat]
