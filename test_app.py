import os
import random
import socket
import threading

import pytest


def maybe_flake(flake_type: str, probability: float = 0.7) -> None:
    if os.environ.get(f"FLAKE_{flake_type.upper()}", "0") == "1":
        if random.random() < probability:
            raise RuntimeError(f"Simulated flake: {flake_type}")


def test_race_condition():
    maybe_flake("RACE")
    shared = []

    def add():
        shared.append(1)

    def pop():
        if shared:
            shared.pop()

    t1 = threading.Thread(target=add)
    t2 = threading.Thread(target=pop)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    assert len(shared) == 1


def test_network_timeout():
    maybe_flake("NETWORK")
    try:
        socket.create_connection(("10.255.255.1", 80), timeout=0.1)
    except (socket.timeout, OSError):
        pytest.fail("Network timeout: could not reach external service")


def test_infra_blip():
    maybe_flake("INFRA")
    if random.random() < 0.3:
        raise OSError("No space left on device")
    assert True


def test_dependency():
    maybe_flake("DEPENDENCY")
    import nonexistent_module_xyz  # noqa: F401
