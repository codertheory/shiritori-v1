import nanoid


def default_id_generator(size: int = 21):
    return nanoid.generate(size=size)


def generate_id(size: int = 21):
    return nanoid.generate(size=size)
