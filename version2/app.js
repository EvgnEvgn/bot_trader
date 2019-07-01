const amqpManager = require('./services/amqpManager');
const websocket = require('./services/websocket');
const {getKline} = require('./services/binance');


async function analyze() {
    const majorCurrency = 'USDT';
    const firstCurrency = 'XMR';
    const secondCurrency = 'ZEC';
    const firstCurrencyData = await getKline(firstCurrency + majorCurrency, "1m", Date.now() - 70000000);
    const secondCurrencyData = await getKline(secondCurrency + majorCurrency, "1m", Date.now() - 70000000);

    const result = await amqpManager.analyzePair(firstCurrencyData, secondCurrencyData);
    websocket.sendAll({z_data: result.z_data});
}
setInterval(analyze, 10000);
