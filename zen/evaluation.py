import datetime
import os
import random
import shlex
import subprocess
import sys
from typing import List
from blessings import Terminal

from conf import partitions, path
from evolution.individual_base import Individual
from objective_function import soft_maximum_worst_case
from parsing import parse_trades, args_for_strategy

term = Terminal()

def pct(x):
    return x / 100.0


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
        self.args = args_for_strategy(self.strategy)
        for _ in self.args:
            self.append(50 + (random.random() - 0.5) * 100)

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
        normalized = {param: self.normalize(value, period) if 'period' in param or param == 'trend_ema' else value for
                      param, value in
                      res.items()}
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

    def normalize(self, value: float, period: int):
        return (value / period)

    def convert(self, param, value):
        if param == 'period':
            if Andividual.strategy == 'macd':
                res = minutes(int(value * 2))
            elif '_macd' in Andividual.strategy:
                res = minutes(int(value))
            elif Andividual.strategy == 'speed':
                res = minutes(int(value / 10))
            else:
                res = minutes(int(value / 4))
        elif param == 'min_periods':
            if Andividual.strategy == 'speed':
                res = int(value * 1000)
            elif Andividual.strategy == 'srsi_macd':
                res = int(value * 250)
            else:
                res = int(value * 20)
        elif param == 'trend_ema':
            res = int(value*15 )
        elif param == 'ema_short_period':
            if Andividual.strategy == 'srsi_macd':
                res = int(value * 20)
            else:
                res = int(value * 10)
        elif param == 'ema_long_period':
            if Andividual.strategy == 'srsi_macd':
                res = int(value * 200)
            else:
                res = int(value * 20)
        elif param == 'signal_period':
            if Andividual.strategy == 'srsi_macd':
                res = int(value * 10)
            else:
                res = int(value * 8)
        elif param == 'neutral_rate':
            res = pct(value / 5)
        elif param == 'oversold_cci':
            res = int(value * -8)
        elif param == 'overbought_cci':
            res = int(value * 10)
        elif param == 'constant':
            res = value / 2000
        elif 'overbought_rsi' in param:
            res = int(value)
        elif 'oversold_rsi' in param:
            res = int(value)
        elif param == 'rsi_periods':
            res = int(value * 10)
        elif param == 'cci_periods':
            res = int(value * 10)
        elif param == 'rsi_recover':
            res = int(value / 10)
        elif param == 'rsi_drop':
            res = int(value / 10)
        elif param == 'rsi_divisor':
            res = int(value / 10)
        elif param == 'srsi_periods':
            res =(int(value * 10))
        elif param == 'srsi_k':
            res =(int(value / 2))
        elif param == 'srsi_d':
            res =(int(value / 2))
        elif param == 'baseline_periods':
            res = int(value * 3000)
        elif 'threshold' in param:
            res = value/1000.0
        elif param == 'sar_af':
            res = value / 100.0
        elif param == 'sar_max_af':
            res = pct(value)
        elif param == 'trigger_factor':
            res = float(value / 30.0)
        else:
            raise ValueError(term.red(f"I don't understand {param} please add it to evaluation.py"))
        return param, res




def evaluate_zen(cmdline:str, days: int):
    periods = time_params(days, partitions)
    try:
        fitness = []
        for period in periods:
            cmd = ' '.join([cmdline, period])
            f,t = runzen(cmd)
            fitness.append(f)
            if t==0:
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
