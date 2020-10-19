module.exports = {
  apps: [{
    name: 'beginners-capsule',
    cwd: 'files',
    script: 'node_modules/ts-node/dist/bin.js',
    args: 'server.ts',
    env: {
      'FLAG': 'SECCON{Player_WorldOfFantasy_StereoWorXxX_CapsLock_WaveRunner}',
      'RECAPTCHA_SECRET': '6LcpzNMZAAAAACuS6UfCBdrf1ENSrs45V_Po1yia',
    },
    error_file: '../error.log',
    out_file: '../access.log',
  }],
};
