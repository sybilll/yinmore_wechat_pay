module.exports = {
  entry: './src/main.js',
  entry: {
        main: './src/main.js',
        admin: "./src/admin.js",
  	},
  output: {
    path: './dist',
    publicPath: 'dist/',
    filename: "[name].js"
  },
  module: {
    loaders: [
      { test: /\.coffee$/, loader: "coffee-loader" },
      { test: /\.less$/, loader: "style!css!less" },
      { test: /\.(html|tpl)$/, loader: "html?attrs=img:requir-src" },
      { test: /\.vue$/, loader: 'vue' },
      {
        test: /\.js$/,
        loader: 'babel!eslint',
        // make sure to exclude 3rd party code in node_modules
        exclude: /node_modules/
      },
      {
        // edit this for additional asset file types
        test: /\.(png|jpg|gif)$/,
        loader: 'url',
        query: {
          // inline files smaller then 10kb as base64 dataURL
          limit: 10000,
          // fallback to file-loader with this naming scheme
          name: '[name].[ext]?[hash]'
        }
      }
    ]
  },
  resolve: {
    extensions: ["", ".web.coffee", ".web.js", ".coffee", ".js"],
    alias: {
        'lib': process.env.LIB_BZ_PATH
      }
  },
  // vue-loader config:
  // lint all JavaScript inside *.vue files with ESLint
  // make sure to adjust your .eslintrc
  vue: {
    loaders: {
      js: 'babel!eslint'
    }
  },
  externals: {
    // vue: 'vue', //73.4kb
    //vuex: 'vuex', // 56kb
    //'vue-moment': 'vue-moment', // 177.4kb
    //underscore: 'underscore'
    jquery: 'jQuery'
  }
}
