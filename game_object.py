from vec2 import Vec2

game_objects = []


class GameObject:
    next_proc_id = 0

    def __init__(self, pos=Vec2(0, 0), parent=None):
        self.parent = parent
        self._pos = Vec2(pos)
        self.processes = {}
        self.register()

    def destroy(self):
        game_objects.remove(self)

    def register(self):
        game_objects.append(self)

    @property
    def gpos(self):
        parent_pos = self.parent.gpos if self.parent else Vec2(0, 0)
        return self.pos + parent_pos

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, value):
        self._pos = Vec2(value)

    def animate_transition(self, dest, duration):
        velocity = (dest - self.pos) / duration
        time_left = duration

        def transpose_process(dtime):
            nonlocal dest
            nonlocal velocity
            nonlocal time_left
            self.pos += velocity * dtime
            time_left -= dtime
            if time_left <= 0:
                self.pos = dest
                return "DONE"
            return "INPROGRESS"

        GameObject.next_proc_id += 1
        self.processes[GameObject.next_proc_id] = transpose_process

    def draw(self, surface):
        pass

    def update(self, dtime):
        finished_procs = []
        for id, proc in self.processes.items():
            status = proc(dtime)
            if status == "DONE":
                finished_procs.append(id)
        for id in finished_procs:
            del self.processes[id]
