

const chart = LightweightCharts.createChart(document.getElementById('chart0'), {
    width: 1000,
    height: 400,

    PriceScale: {
        mode: 2,
        borederColor: '#563B35',
    },
    timeScale: {
        timeVisible: true,
        borderColor: '#33',
    },
    layout: {
        background: { color: "#333" },
        textColor: "#C3BCDB",
      },
    grid: {
        vertLines: { color: "#CD853F" },
        horzLines: { color: "#563B35" },
      },
});


const candlestickSeries = chart.addCandlestickSeries({
    upColor: '#26a69a', downColor: '#ef5350', borderVisible: false,
    wickUpColor: '#26a69a', wickDownColor: '#ef5350',
});


const volumeSeries = chart.addHistogramSeries({
    priceFormat: {
        type: 'volume',
    },


    priceScaleId: '', // set as an overlay by setting a blank priceScaleId
});
volumeSeries.priceScale().applyOptions({
    timeScale: {
        timeVisible: true,
    },

    scaleMargins: {
        top: 0.7,
        bottom: 0,
    },
});

document.getElementById('block').addEventListener('click', () => {

    let pair = document.querySelector('.pair_select');
    let time = document.querySelector('.time');


    fetch(`http://127.0.0.1:5000/history/${pair.value}/${time.value}`)
    .then(r => r.json())
    .then(response => {
        candlestickSeries.setData(response);

        console.log(response[0]);

    });


    let socket = new WebSocket(`wss://stream.binance.com:9443/ws/${pair.value}@${time.value}`);

    socket.onmessage = function(event) {
      let message = JSON.parse(event.data);

      let candle = message.k;

      candlestickSeries.update(
        {time: candle.t,
        open: candle.o,
        high: candle.h,
        low: candle.l,
        close: candle.c
        });

    //   volumeSeries.update(
    //     {
    //     time: candle.t,
    //     value: candle.v,
    //     color: '#26a69a',
    //     });

    };

})
