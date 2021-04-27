module.exports = {
  apps : [{
    name: 'mail2slack',
    cmd: 'mail2slack.py',
    args: '',
    autorestart: true,
    watch: true,
    pid: '~/.local/share/m2s.pid',
    instances: 1,
    max_memory_restart: '1G', 
    interpreter: '/usr/bin/python3.6',
    time: true
    env: {
        NODE_ENV: 'development'
      },
      env_production: {
        NODE_ENV: 'production'
      }    
  }, 
 ]
};
