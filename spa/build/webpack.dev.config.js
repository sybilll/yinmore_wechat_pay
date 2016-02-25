var config = require('./webpack.base.config')

config.devtool = 'eval-source-map'

config.devServer = {
    noInfo: true,
    proxy: {
        "/api_*": "http://localhost:8000",
        "/login": "http://localhost:8000",
        "/logout": "http://localhost:8000",
        "/static/*": "http://localhost:8000"
    }
}

module.exports = config
