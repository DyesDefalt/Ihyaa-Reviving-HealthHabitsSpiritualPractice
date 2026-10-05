module.exports = function (api) {
  api.cache(true);
  if (!process.env.REACT_APP_BACKEND_URL) throw new Error('REACT_APP_BACKEND_URL is required');
  return {
    presets: ['babel-preset-expo'],
    plugins: [['transform-inline-environment-variables', { include: ['REACT_APP_BACKEND_URL'] }]],
  };
};