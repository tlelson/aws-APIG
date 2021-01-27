/**
 * This file needs to Vanilla JavaScript that can be executed in the current Node environment as Babel cannot know what
 * transformations it would need to apply before reading this file
 */

module.exports = {
  presets: [
    '@babel/preset-env',
    '@babel/preset-typescript',
  ],
  plugins: [
    'babel-plugin-lodash',
  ],
  env: {
    test: {
      plugins: [
        'babel-plugin-istanbul',
      ],
    },
  },
};

