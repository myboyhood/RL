from gym.envs.registration import register

register(
    id='PlaneEnv-v3',
    entry_point='plane_env.envs:PlaneWorldEnv',
)
