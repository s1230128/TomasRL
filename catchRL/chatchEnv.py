#
class TomasEnv:
    #
    def __init__(self):

        self.reset()

    #
    def reset(self):

        return self.__obs()

    #
    def step(self, action):
        return obs, reward, done

    #
    def __obs(self):


    #
    def render(self):


    #
    def random_act(self):
        return np.random.choice([0, 1, 2])



# main
if __name__ == '__main__':
    env = TomasEnv()

    clock = pg.time.Clock()
    framerate = 60
    done = False

    while not done:
        # フレームレート
        clock.tick(framerate)

        # 終了判定
        for e in pg.event.get():
            if e.type == QUIT: sys.exit()

        act = 0
        if pg.key.get_pressed()[K_LEFT ]: act = 1
        if pg.key.get_pressed()[K_RIGHT]: act = 2

        obs, reward, done, info = env.step(act)
        env.render()
