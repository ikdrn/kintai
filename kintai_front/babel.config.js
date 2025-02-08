// vue.config.js
module.exports = {
  devServer: {
    proxy: {
      '/api': {
        target: 'http://localhost:8000', // Django サーバーのアドレスとポート
        changeOrigin: true,
        secure: false,
      },
    },
  },
};
