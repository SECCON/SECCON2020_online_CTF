module.exports = {
  apps: [{
    name: 'capsule',
    cwd: 'files',
    script: 'node_modules/ts-node/dist/bin.js',
    args: 'server.ts',
    env: {
      'FLAG': 'SECCON{HighCollarGirl_CutieCinem@Replay_PhonyPhonic_S.F.SoundFurniture}',
      'RECAPTCHA_SECRET': '6LcpzNMZAAAAACuS6UfCBdrf1ENSrs45V_Po1yia',
    },
    error_file: '../error.log',
    out_file: '../access.log',
  }],
};
