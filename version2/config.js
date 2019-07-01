'use strict';

const config = {
    amqp:{
        reconnectTime: 7000,
        rabbitMQ:{
            url: 'amqp://localhost'
        },
        channels:{
            NEED_ANALYZE_PAIR: 'NEED_ANALYZE_PAIR',
            RESULT_ANALYZE_PAIR: 'RESULT_ANALYZE_PAIR'
        }
    }
};

module.exports = config;