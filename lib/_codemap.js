module.exports = {
  _ns: 'zenbot',
  _folder: 'lib',
  _maps: [
    require('./talib/_codemap')
  ],

  'cci': require('./cci'),
  'ema': require('./ema'),
  'engine': require('./engine'),
  'normalize-selector': require('./normalize-selector'),
  'rsi': require('./rsi'),
  'sma': require('./sma'),
  'srsi': require('./srsi'),
  'ema': require('./ema'),
  'sma': require('./sma'),
  'stddev': require('./stddev')
}
