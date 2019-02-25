from ._Scene import _Scene

class Scene_Stack(object):
    the_stack = []

    @classmethod
    def add_scene(cls, scene):
        assert isinstance(scene, _Scene), "add_scene: {} is of class {} which inherits not from {}".format(scene, scene.__class__, _Scene)
        cls.the_stack.append(scene)
        #print(cls.the_stack)

    @classmethod
    def pop_scene(cls):
        cls.the_stack.pop()
        #print(cls.the_stack)

    @classmethod
    def change_scene(cls, scene):
        cls.pop_scene()
        cls.add_scene(scene)

    @classmethod
    def below(cls, scene):
        i = cls.the_stack.index(scene)
        return cls.the_stack[i-1] if i > 0 else None

    @classmethod
    def get_current(cls):
        return cls.the_stack[-1] if cls.the_stack else None
