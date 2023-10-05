module.exports = {
  preset: "@vue/cli-plugin-unit-jest",
  transform: {
    "^.+\\.css$": "jest-transform-css"
  },
  moduleNameMapper: {
    "\\.(css|less|sass|scss)$": "identity-obj-proxy"
  },
  collectCoverage: true,
  coverageReporters: ["json", "lcov", "text", "html"],
  collectCoverageFrom: ['src/**/*.{js,vue}', '!src/main.js'],

};

