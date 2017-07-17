import datetime
import os
import random
import shlex
import subprocess
import sys
from typing import List
from blessings import Terminal

from conf import partitions, path, rnddev
from evolution.individual_base import Individual
from objective_function import soft_maximum_worst_case
from parsing import parse_trades, args_for_strategy

term = Terminal()

def minutes(x):
    return str(int(x)) + 'm'

def runzen(cmdline):
    with open(os.devnull, 'w') as devnull:
        a = subprocess.check_output(shlex.split(cmdline), stderr=devnull)
    profit = a.split(b'}')[-1].splitlines()[3].split(b': ')[-1][:-1]
    trades = parse_trades(a.split(b'}')[-1].splitlines()[4])
    return float(profit), float(trades)

class Andividual(Individual):
    BASE_COMMAND = '{path}/zenbot.sh sim --filename temp.html {instrument} --strategy {strategy} --avg_slippage_pct 0.33'
    def __init__(self, *args,**kwargs):
        super(Andividual, self).__init__(*args, **kwargs)
        self.args = dict(args_for_strategy(self.strategy))
        if self.strategy == 'trend_ema':
            del self.args['neutral_rate']
        for __ in self.args:
            dmin = float(self.args[__]) - (float(self.args[__]) / 100 * rnddev)
            dmax = float(self.args[__]) + (float(self.args[__]) / 100 * rnddev)
            self.args[__] = random.uniform(dmin, dmax)
            self.append(self.args[__])
        self.args = self.args.keys()

    def __repr__(self):
        return f"{self.cmdline} {super(Andividual, self).__repr__()}"

    @property
    def instrument(self):
        return random.choice(self.instruments)

    @property
    def objective(self):
        return soft_maximum_worst_case(self)

    def compress(self):
        res = dict(zip(self.args, self))
        period = res['period']
        del res['period']
        normalized = {param: value for param, value in res.items()}
        normalized['period'] = period
        output = dict(self.convert(param, value) for param, value in normalized.items())
        return output.items()

    @property
    def params(self) -> List[str]:
        def format(key, value):
            if isinstance(value, float):
                return f'--{key} {value:.6f}'
            else:
                return f'--{key} {value}'

        params = [format(key, value) for key, value in self.compress()]
        return params

    @property
    def cmdline(self) -> str:
        base = self.BASE_COMMAND.format(path=self.path, instrument=self.instrument, strategy=self.strategy)
        result = ' '.join([base] + self.params)
        return result

    def convert(self, param, value):
        if param == 'period':
            res = minutes(int(value))
        elif param == 'neutral_rate':
            res = float(value)
        elif param == 'trigger_factor':
            res = float(value)
        elif param == 'constant':
            res =float(value)
        elif 'sar_' in param:
            res = float(value)
        elif 'treshold' in param:
            res = float(value)
        else:
            res = int(value)
        return param, res

def evaluate_zen(cmdline:str, days: int):
    periods = time_params(days, partitions)
    try:
        fitness = []
        for period in periods:
            cmd = ' '.join([cmdline, period])
            f,t = runzen(cmd)
            fitness.append(f)
            if t<=0.2:
                raise subprocess.CalledProcessError(-1,'TooFewTrades')
        sys.stdout.write('.')
    except subprocess.CalledProcessError:
        fitness = [-100 for _ in periods]
        sys.stdout.write('x')
    sys.stdout.flush()
    return tuple(fitness)


def time_params(days: int, partitions: int) -> List[str]:
    now = datetime.date.today()
    delta = datetime.timedelta(days=days)
    splits = [now - delta / partitions * i for i in range(partitions + 1)][::-1]
    return [f' --start {start} --end {end}' for start, end in zip(splits, splits[1:])]
