// const { defineConfig } = require("@vue/cli-service");
// module.exports = defineConfig({
//   transpileDependencies: true,

//   pluginOptions: {
//     vuetify: {
// 			// https://github.com/vuetifyjs/vuetify-loader/tree/next/packages/vuetify-loader
// 		}
//   }
// });
// eslint-disable-next-line no-undef
module.exports = {
    css: {
        loaderOptions: {
            sass: {
                additionalData: ``
            },
        },
    },
};