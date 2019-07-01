'use strict';
const uuid = require('uuid/v4');
const events = require('events');
const eventEmitter = new events.EventEmitter();
const amqp = require('amqplib/callback_api');
const config = require('../config');


const RECONNECT_TIME = config.amqp.reconnectTime;
let channel = null;


function createChannel(connection) {
    connection.createChannel((err, ch) => {
        channel = ch;
        ch.on('error', err => {
            console.error('[AMQP] channel error', err.message);
        });
        ch.on('close', () => {
            console.error('[AMQP] channel closed');
            createChannel(connection);
        });
        // создаем необходимые очереди
        for (let nameChannelKey in config.amqp.channels) {
            const nameChannel = config.amqp.channels[nameChannelKey];
            ch.assertQueue(nameChannel, {durable: true});
        }
        // подписываемся на получения результатов анализа пар
        ch.consume(config.amqp.channels.RESULT_ANALYZE_PAIR, msg => {
            const message = JSON.parse(msg.content);
            if (message.messageId) {
                console.log('Получили результат транзакции', message);
                return eventEmitter.emit(message.messageId, message, msg);
            }
        }, {noAck: true});
    });
}

/**
 * Функция подключения к rabbitMQ
 */
function connect() {
    amqp.connect(config.amqp.rabbitMQ.url + '?heartbeat=60', (err, conn) => {
        if (err) {
            console.error('[AMQP]', err.message);
            return setTimeout(connect, RECONNECT_TIME);
        }
        // Подписываемся на событие ошибок
        conn.on('error', err => {
            if (err.message !== 'Connection closing') {
                console.error('[AMQP] conn error', err.message);
            }
        });
        // Подписываемся событие закрытия соединения
        conn.on('close', () => {
            console.error('[AMQP] reconnecting');
            return setTimeout(connect, RECONNECT_TIME);
        });
        // создаем каналы
        createChannel(conn);
    });
}

connect();

module.exports = {
    /**
     * Ф-я публикует транзакции, которые необходимо выполнить
     * @param {Object} data сообщение, которое публицируем
     * @return {Promise<boolean>}
     */
    pushForAnalyzePair: async data => {
        if (!channel) {
            console.error(`Channel for connect ampq server not created`);
            return false;
        }

        try {
            console.log(`Отправляем сообщение в очередь ${config.amqp.channels.NEED_ANALYZE_PAIR}`, data);
            return await channel.sendToQueue(config.amqp.channels.NEED_ANALYZE_PAIR, Buffer.from(JSON.stringify(data)), {persistent: true});
        } catch (err) {
            console.error(`Не удалось записать ${JSON.stringify(data)} в очередь ${config.amqp.channels.NEED_ANALYZE_PAIR} ${err}`);
        }
        return false;
    },
    analyzePair: async (firstCurrencyData, secondCurrencyData, operation) => {
        if (!channel) {
            console.error(`Channel for connect ampq server not created`);
            return false;
        }

        try {
            const data = {
                firstCurrencyData,
                secondCurrencyData,
                messageId: uuid()
            };

            console.log(`Отправляем сообщение в очередь ${config.amqp.channels.NEED_ANALYZE_PAIR}`, data);
            await channel.sendToQueue(config.amqp.channels.NEED_ANALYZE_PAIR, Buffer.from(JSON.stringify(data)), {persistent: true});
            return await new Promise((resolve, reject) => {
                eventEmitter.on(data.messageId, (res, origMsg) => {
                    return resolve(res);
                });
            })
        } catch (err) {
            console.error(`Не удалось записать ${JSON.stringify(data)} в очередь ${config.amqp.channels.NEED_ANALYZE_PAIR} ${err}`);
        }
        return null;
    },
    /**
     * Ф-я подписки на очередь результатов транзакциий
     * @param {String} event название события подписки
     * @param {Function} cb ф-я обратного вызова, вызывается по наступлению события event
     */
    listenResultAnalyzePair: (event, cb) => {
        eventEmitter.on(event, cb);
    }
};

