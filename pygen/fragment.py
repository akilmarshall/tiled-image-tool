from itertools import product
from os import mkdir
from os.path import exists
from shutil import rmtree
from itertools import chain
from .util import TIS

from tqdm import tqdm


class Fragment:
    """
    A set of 3x3 tiled images generated by a single tile
    """

    def __init__(self, tid):
        self.tid = tid

    def n_fragmaent(self, i):
        """
        for the tile i, how many fragments can it generate?
        """
        assert 0 <= i < self.tid.n
        A = self.tid.nids(i, 0)
        B = self.tid.nids(i, 1)
        C = self.tid.nids(i, 2)
        D = self.tid.nids(i, 3)
        a = len(A)
        b = len(B)
        c = len(C)
        d = len(D)
        print(a, b, c, d, a * b * c * d)

    def _core(self, i):
        """
        generator for the cores seeded with i, i.e. only the primary infered tiles are generated
        _ 1 _
        2 i 0
        _ 3 _
        """
        assert 0 <= i < self.tid.n
        A = self.tid.nids(i, 0)
        B = self.tid.nids(i, 1)
        C = self.tid.nids(i, 2)
        D = self.tid.nids(i, 3)
        for a, b, c, d in product(A, B, C, D):
            img = [
                [None, c, None],
                [b, i, d],
                [None, a, None],
            ]
            yield img

    def _yield(self, a, b, c, d, e, f, g, h, i):
        """
              left
               adg
        right  beh  top
               cfi
              right
        """
        return [
            [a, d, g],
            [b, e, h],
            [c, f, i],
        ]

    def CENTER(self, t):
        """
        Implementation of the CENTER algorithm
        """

        def intersect(u, x, v, y):
            A = set(self.tid.nids(u, x))
            B = set(self.tid.nids(v, y))
            return A.intersection(B)

        assert 0 <= t < self.tid.n

        A = self.tid.nids(t, 0)
        B = self.tid.nids(t, 1)
        C = self.tid.nids(t, 2)
        D = self.tid.nids(t, 3)

        for a, b, c, d in product(A, B, C, D):
            E = intersect(d, 0, a, 3)
            F = intersect(b, 0, a, 1)
            G = intersect(c, 1, b, 2)
            H = intersect(c, 3, d, 2)
            for e, f, g, h in product(E, F, G, H):
                yield self._yield(g, b, f, c, t, a, h, d, e)

    def CORNER(self, t):
        """
        Implementation of the CORNER algorithm
        """
        assert 0 <= t < self.tid.n
        B = self.tid.nids(t, 0)
        D = self.tid.nids(t, 3)

        for b, d in product(B, D):
            for e in self.tid.intersect(b, 3, d, 0):
                F = self.tid.nids(e, 0)
                H = self.tid.nids(e, 3)
                for f, h in product(F, H):
                    I = self.tid.intersect(h, 0, f, 3)
                    G = self.tid.intersect(d, 3, h, 2)
                    C = self.tid.intersect(b, 0, f, 1)
                    for i, g, c in product(I, G, C):
                        yield self._yield(t, b, c, d, e, f, g, h, i)

    def SIDE(self, t):
        """
        Implementation of the SIDE algorithm
        """
        C = self.tid.nids(t, 0)
        A = self.tid.nids(t, 2)
        E = self.tid.nids(t, 3)
        for a, c, e in product(A, C, E):
            D = self.tid.intersect(a, 3, e, 2)
            F = self.tid.intersect(e, 0, c, 3)
            H = self.tid.nids(e, 3)
            for d, f, h in product(D, F, H):
                G = self.tid.intersect(d, 3, h, 2)
                I = self.tid.intersect(h, 0, f, 3)
                for g, i in product(G, I):
                    yield self._yield(a, t, c, d, e, f, g, h, i)

    def _dump_all(self, f, name: str):
        """
        abstracted helper function for dumping fragment members

        f       {center_fragment, corner_fragment, side_fragment}
        name    name of the procedure, names the output directory and prints for debug purposes
        """
        print(name)
        if exists(name):
            rmtree(name)
        mkdir(name)
        for i in tqdm(range(self.tid.n)):
            local = f"{name}/{i}"
            mkdir(local)
            for n, frag in enumerate(f(i)):
                self.tid.to_image(frag).save(f"{local}/{n}.png")

    def dump_all_center_fragment(self):
        self._dump_all(self.CENTER, "Center Fragments")

    def dump_all_corner_fragment(self):
        self._dump_all(self.CORNER, "Corner Fragments")

    def dump_all_side_fragment(self):
        self._dump_all(self.SIDE, "Side Fragments")

    def dump_all_center_core(self):
        self._dump_all(self._core, "Center Core")


class Store:
    """
    A collection of fragments
    """

    def __init__(self, tis: TIS):
        self.store = []
        fragment = Fragment(tis)
        for i in range(tis.n):
            for frag in chain(fragment.CENTER(i), fragment.CORNER(i), fragment.SIDE(i)):
                self.store.append(frag)

    def query(self, strip: list[int], edge: int):
        assert 0 <= edge < 4
        assert len(strip) == 3
        for frag in self.store:
            match edge:
                case 0:
                    if frag[0] == strip:
                        yield frag
                case 2:
                    if frag[2] == strip:
                        yield frag
                case 1:
                    if [frag[0][0], frag[1][0], frag[2][0]] == strip:
                        yield frag
                case 3:
                    if [frag[0][2], frag[1][2], frag[2][2]] == strip:
                        yield frag


class Expander:
    def __init__(self, tis: TIS):
        self.tis = tis

    def centerx(self, strip):
        assert len(strip) == 3
        # orientation is assumed,
        # probably should be described as an enum
        # to dictate the generation of the expanded vector
        out = [None] * 3
        for a in self.tis.nids(strip[1], 0):
            out[1] = a
            B = set(self.tis.nids(strip[0], 0)).intersection(set(self.tis.nids(a, 1)))
            C = set(self.tis.nids(strip[2], 0)).intersection(set(self.tis.nids(a, 3)))
            for b, c in zip(B, C):
                out[0] = b
                out[2] = c
                yield out

    def cornerx(self, strip, mirror=None):
        assert len(strip) == 3
        if mirror:
            return self._cornerx_L(strip)
        else:
            return self._cornerx_R(strip)

    def _cornerx_L(self, strip):
        out = [None] * 3
        for a in self.tis.nids(strip[0], 0):
            out[0] = a
            B = set(self.tis.nids(strip[1], 0)).intersection(set(self.tis.nids(a, 3)))
            for b in B:
                out[1] = b
                C = set(self.tis.nids(strip[2], 0)).intersection(
                    set(self.tis.nids(b, 3))
                )
                for c in C:
                    out[2] = c
                    yield out

    def _cornerx_R(self, strip):
        out = [None] * 3
        for a in self.tis.nids(strip[2], 0):
            out[2] = a
            B = set(self.tis.nids(strip[1], 0)).intersection(set(self.tis.nids(a, 1)))
            for b in B:
                out[1] = b
                C = set(self.tis.nids(strip[0], 0)).intersection(
                    set(self.tis.nids(b, 1))
                )
                for c in C:
                    out[0] = c
                    yield out
