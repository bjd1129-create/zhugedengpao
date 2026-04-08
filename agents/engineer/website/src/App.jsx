import { useState, useEffect } from 'react'
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, ComposedChart, Area } from 'recharts'

function App() {
  const [prices, setPrices] = useState(null)
  const [indicators, setIndicators] = useState(null)
  const [historicalData, setHistoricalData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [selectedSymbol, setSelectedSymbol] = useState('BTC')
  const [timeRange, setTimeRange] = useState('7d')

  useEffect(() => {
    fetchData()
    const interval = setInterval(fetchData, 60000)
    return () => clearInterval(interval)
  }, [])

  async function fetchData() {
    try {
      const [pricesRes, indicatorsRes, historicalRes] = await Promise.all([
        fetch('/data/futures_prices.json?t=' + Date.now()),
        fetch('/data/technical_indicators.json?t=' + Date.now()),
        fetch('/data/historical_prices.json?t=' + Date.now())
      ])
      const pricesData = await pricesRes.json()
      const indicatorsData = await indicatorsRes.json()
      const historicalData = await historicalRes.json()
      setPrices(pricesData)
      setIndicators(indicatorsData)
      setHistoricalData(historicalData)
      setLoading(false)
    } catch (e) {
      console.error('Failed to fetch data:', e)
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-900">
        <div className="text-xl">加载中...</div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-900 p-8">
      <div className="max-w-7xl mx-auto">
        <header className="mb-8">
          <h1 className="text-4xl font-bold text-white mb-2">诸葛灯炮</h1>
          <p className="text-gray-400">期货市场数据仪表盘</p>
          {prices?.update_time && (
            <p className="text-gray-500 text-sm mt-2">
              更新时间：{new Date(prices.update_time).toLocaleString('zh-CN')}
            </p>
          )}
        </header>

        <section className="mb-8">
          <h2 className="text-2xl font-semibold text-white mb-4">实时行情</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            {prices?.futures && Object.entries(prices.futures).map(([symbol, data]) => (
              <PriceCard key={symbol} symbol={symbol} data={data} indicators={indicators?.indicators?.[symbol]} />
            ))}
            {prices?.crypto && Object.entries(prices.crypto).map(([symbol, data]) => (
              <CryptoCard key={symbol} symbol={symbol} data={data} indicators={indicators?.indicators?.[symbol]} />
            ))}
          </div>
        </section>

        <section className="mb-8">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-2xl font-semibold text-white">历史走势</h2>
            <div className="flex gap-2">
              {['BTC', 'ETH', 'ES', 'NQ'].map(sym => (
                <button
                  key={sym}
                  onClick={() => setSelectedSymbol(sym)}
                  className={`px-4 py-2 rounded-lg font-medium transition ${
                    selectedSymbol === sym ? 'bg-blue-600 text-white' : 'bg-gray-800 text-gray-400 hover:bg-gray-700'
                  }`}
                >
                  {sym}
                </button>
              ))}
              <select
                value={timeRange}
                onChange={(e) => setTimeRange(e.target.value)}
                className="bg-gray-800 text-white px-4 py-2 rounded-lg border border-gray-700"
              >
                <option value="24h">24 小时</option>
                <option value="7d">7 天</option>
                <option value="30d">30 天</option>
              </select>
            </div>
          </div>
          
          {historicalData && historicalData[selectedSymbol] ? (
            <HistoricalChart data={historicalData[selectedSymbol]} symbol={selectedSymbol} timeRange={timeRange} />
          ) : (
            <div className="bg-gray-800 rounded-xl p-8 text-center text-gray-400">
              暂无历史数据
            </div>
          )}
        </section>

        <section className="mb-8">
          <h2 className="text-2xl font-semibold text-white mb-4">技术指标对比</h2>
          <div className="bg-gray-800 rounded-xl p-6">
            <TechnicalTable indicators={indicators?.indicators} />
          </div>
        </section>
      </div>
    </div>
  )
}

function PriceCard({ symbol, data, indicators }) {
  const isUp = data.change_pct > 0
  const isDown = data.change_pct < 0
  const changeClass = isUp ? 'bg-green-500/20 text-green-500' : isDown ? 'bg-red-500/20 text-red-500' : 'bg-gray-500/20 text-gray-500'
  
  return (
    <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
      <div className="flex justify-between items-start mb-4">
        <div>
          <h3 className="text-xl font-bold text-white">{symbol}</h3>
          <p className="text-gray-400 text-sm">价格</p>
        </div>
        <span className={`px-3 py-1 rounded-full text-sm font-medium ${changeClass}`}>
          {isUp ? '+' : ''}{data.change_pct?.toFixed(2)}%
        </span>
      </div>
      
      <div className="text-3xl font-bold text-white mb-4">
        {data.price.toLocaleString()}
      </div>

      <div className="grid grid-cols-2 gap-4 text-sm">
        <div>
          <p className="text-gray-500">成交量</p>
          <p className="text-white">{data.volume?.toLocaleString() || '-'}</p>
        </div>
        <div>
          <p className="text-gray-500">趋势</p>
          <p className={data.trend === '上涨' ? 'text-green-500' : data.trend === '下跌' ? 'text-red-500' : 'text-gray-500'}>
            {data.trend || '-'}
          </p>
        </div>
      </div>

      {indicators && (
        <div className="mt-4 pt-4 border-t border-gray-700">
          <p className="text-gray-500 text-xs mb-2">技术指标</p>
          <div className="grid grid-cols-2 gap-2 text-xs">
            <div>
              <span className="text-gray-500">RSI: </span>
              <span className={indicators.rsi_14 > 70 ? 'text-red-500' : indicators.rsi_14 < 30 ? 'text-green-500' : 'text-white'}>
                {indicators.rsi_14?.toFixed(2) || '-'}
              </span>
            </div>
            <div>
              <span className="text-gray-500">MACD: </span>
              <span className="text-white">{indicators.macd?.toFixed(2) || '-'}</span>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

function CryptoCard({ symbol, data, indicators }) {
  const trendClass = indicators?.trend === '上涨' ? 'bg-green-500/20 text-green-500' : indicators?.trend === '下跌' ? 'bg-red-500/20 text-red-500' : 'bg-gray-500/20 text-gray-500'
  
  return (
    <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
      <div className="flex justify-between items-start mb-4">
        <div>
          <h3 className="text-xl font-bold text-white">{symbol}</h3>
          <p className="text-gray-400 text-sm">价格</p>
        </div>
        {indicators?.trend && (
          <span className={`px-3 py-1 rounded-full text-sm font-medium ${trendClass}`}>
            {indicators.trend}
          </span>
        )}
      </div>
      
      <div className="text-3xl font-bold text-white mb-4">
        ${data.price.toLocaleString()}
      </div>

      <div className="grid grid-cols-2 gap-4 text-sm">
        <div>
          <p className="text-gray-500">资金费率</p>
          <p className="text-white">{(data.funding_rate * 100).toFixed(4)}%</p>
        </div>
        <div>
          <p className="text-gray-500">RSI(14)</p>
          <p className={indicators?.rsi_14 > 70 ? 'text-red-500' : indicators?.rsi_14 < 30 ? 'text-green-500' : 'text-white'}>
            {indicators?.rsi_14?.toFixed(2) || '-'}
          </p>
        </div>
      </div>

      {indicators && (
        <div className="mt-4 pt-4 border-t border-gray-700">
          <p className="text-gray-500 text-xs mb-2">MACD</p>
          <div className="grid grid-cols-3 gap-2 text-xs">
            <div>
              <span className="text-gray-500">MACD: </span>
              <span className="text-white">{indicators.macd?.toFixed(2) || '-'}</span>
            </div>
            <div>
              <span className="text-gray-500">Signal: </span>
              <span className="text-white">{indicators.macd_signal?.toFixed(2) || '-'}</span>
            </div>
            <div>
              <span className="text-gray-500">Hist: </span>
              <span className={indicators.macd_hist > 0 ? 'text-green-500' : 'text-red-500'}>
                {indicators.macd_hist?.toFixed(2) || '-'}
              </span>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

function HistoricalChart({ data, symbol, timeRange }) {
  const chartData = data.map(d => ({
    ...d,
    time: new Date(d.timestamp).toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
  }))

  return (
    <div className="bg-gray-800 rounded-xl p-6">
      <ResponsiveContainer width="100%" height={400}>
        <ComposedChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
          <XAxis dataKey="time" stroke="#9CA3AF" />
          <YAxis stroke="#9CA3AF" domain={['auto', 'auto']} />
          <Tooltip 
            contentStyle={{ backgroundColor: '#1F2937', border: 'none', borderRadius: '8px' }}
            labelStyle={{ color: '#F3F4F6' }}
          />
          <Area type="monotone" dataKey="price" stroke="#3B82F6" fill="#3B82F6" fillOpacity={0.1} />
          <Line type="monotone" dataKey="ma_20" stroke="#10B981" strokeWidth={2} dot={false} />
          <Line type="monotone" dataKey="ma_50" stroke="#EF4444" strokeWidth={2} dot={false} />
          <Bar dataKey="volume" yAxisId="right" fill="#6B7280" opacity={0.3} />
        </ComposedChart>
      </ResponsiveContainer>
      <div className="flex justify-center gap-6 mt-4 text-sm">
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 rounded-full bg-blue-500"></div>
          <span className="text-gray-400">价格</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 rounded-full bg-green-500"></div>
          <span className="text-gray-400">MA20</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 rounded-full bg-red-500"></div>
          <span className="text-gray-400">MA50</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 rounded-full bg-gray-500"></div>
          <span className="text-gray-400">成交量</span>
        </div>
      </div>
    </div>
  )
}

function TechnicalTable({ indicators }) {
  if (!indicators) return null

  const symbols = Object.keys(indicators)
  
  return (
    <div className="overflow-x-auto">
      <table className="w-full text-left">
        <thead>
          <tr className="border-b border-gray-700">
            <th className="pb-3 text-gray-400 font-medium">品种</th>
            <th className="pb-3 text-gray-400 font-medium">RSI(14)</th>
            <th className="pb-3 text-gray-400 font-medium">MACD</th>
            <th className="pb-3 text-gray-400 font-medium">Signal</th>
            <th className="pb-3 text-gray-400 font-medium">Histogram</th>
            <th className="pb-3 text-gray-400 font-medium">MA20</th>
            <th className="pb-3 text-gray-400 font-medium">MA50</th>
            <th className="pb-3 text-gray-400 font-medium">趋势</th>
          </tr>
        </thead>
        <tbody>
          {symbols.map(symbol => {
            const ind = indicators[symbol]
            const rsiClass = ind.rsi_14 > 70 ? 'text-red-500' : ind.rsi_14 < 30 ? 'text-green-500' : 'text-white'
            const histClass = ind.macd_hist > 0 ? 'text-green-500' : 'text-red-500'
            const trendClass = ind.trend === '上涨' ? 'text-green-500' : ind.trend === '下跌' ? 'text-red-500' : 'text-gray-500'
            
            return (
              <tr key={symbol} className="border-b border-gray-800">
                <td className="py-3 font-bold text-white">{symbol}</td>
                <td className={`py-3 ${rsiClass}`}>{ind.rsi_14?.toFixed(2) || '-'}</td>
                <td className="py-3 text-white">{ind.macd?.toFixed(2) || '-'}</td>
                <td className="py-3 text-white">{ind.macd_signal?.toFixed(2) || '-'}</td>
                <td className={`py-3 ${histClass}`}>{ind.macd_hist?.toFixed(2) || '-'}</td>
                <td className="py-3 text-white">{ind.ma_20?.toFixed(2) || '-'}</td>
                <td className="py-3 text-white">{ind.ma_50?.toFixed(2) || '-'}</td>
                <td className={`py-3 ${trendClass}`}>{ind.trend || '-'}</td>
              </tr>
            )
          })}
        </tbody>
      </table>
    </div>
  )
}

export default App
