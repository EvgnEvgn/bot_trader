const binance = require('node-binance-api')().options({
    APIKEY: 'F95r3yBjC0q5vblzgqo8WUqwOsfqNBNbSoHTRg23bjPmoReKLBsMjId4C5s0dgHT',
    APISECRET: 'whYmJzFzObWvkfI38pGNFyTdTeejxr8dimpS5sHxQXBHXx04RtjIV9fX8sc8mPqf',
    useServerTime: true // If you get timestamp errors, synchronize to server time at startup
});


// function _parseTick(arr){
//     return {
//         time: arr[0],
//         open: parseFloat(arr[1]),
//         high: parseFloat(arr[2]),
//         low: parseFloat(arr[3]),
//         close: parseFloat(arr[4]),
//         volume: parseFloat(arr[5]),
//         closeTime: arr[6],
//         assetVolume: parseFloat(arr[7]),
//         trades: arr[8],
//         buyBaseVolume: parseFloat(arr[9]),
//         buyAssetVolume: parseFloat(arr[10]),
//         ignored: parseFloat(arr[11])
//     }
// }

function _parseTick(arr) {
    return {
        time: arr[0],
        open: arr[1],
        high: arr[2],
        low: arr[3],
        close: arr[4],
        volume: arr[5],
        closeTime: arr[6],
        assetVolume: arr[7],
        trades: arr[8],
        buyBaseVolume: arr[9],
        buyAssetVolume: arr[10],
        ignored: arr[11]
    }
}


const internals = {
    getCandlesticksAsync: async (symbol, interval, startTime, endTime = undefined, limit = 1000) => {
        return await new Promise((resolve, reject) => {
            binance.candlesticks(symbol, interval, (error, ticks, symbol) => {
                if (error) {
                    return reject(error);
                }
                resolve(ticks.map(_parseTick));
            }, {startTime, endTime, limit});
        })
    }
};

function intervalToMilliseconds(interval) {
    const seconds_per_unit = {
        m: 60,
        h: 60 * 60,
        d: 24 * 60 * 60,
        w: 7 * 24 * 60 * 60
    };
    const unit = interval[interval.length - 1];
    const count = parseInt(interval.slice(0, interval.length - 1));

    return seconds_per_unit[unit] * count * 1000;
}

module.exports = {
    getKline: async (symbol, interval, startTime, endTime = undefined, limit = 1000) => {
        if (typeof startTime === 'string') {
            startTime = new Date(startTime).getTime()
        }
        if (typeof endTime === 'string') {
            endTime = new Date(endTime).getTime()
        }

        const timeframe = intervalToMilliseconds(interval);
        let result = [];
        const first_valid_ts = await internals.getCandlesticksAsync(symbol, interval, 0, undefined, 1);
        startTime = Math.max(startTime, first_valid_ts[0].time);

        while (true) {
            const partTicket = await internals.getCandlesticksAsync(symbol, interval, startTime, endTime, limit);
            if (partTicket.length === 0) break;

            result = result.concat(partTicket);
            startTime = partTicket.slice(-1)[0].time;
            if (partTicket < limit) break;
            startTime += timeframe;
        }

        return result;
    }
};