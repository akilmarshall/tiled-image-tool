# Procedural Image Generation

How can I turn a single image into more images that are somewhat like it?

## Theory

$\mathbb{I}$ denotes a tiled image, that is an image composed of a **tile sheet**
also known as a **tile set**.

![A tile sheet generates an image](https://imgur.com/suCdR2N.png)

$\mathbb{T}$ denotes the tile sheet of $\mathbb{I}$,

$$
    \mathbb{T} = \\{t_1, t_2, \cdots{}, t_n\\}
$$

each tile set $\mathbb{T}$ contains $n$ items each denoted $t\_i$ where
$1\leq i \leq n$.


Each image $\mathbb{I}$ also has an associated **neighbor** function,

$$
    \mathcal{N}_{\mathbb{I}}::t\to d\to \[t\],
$$

![Example of the neighbor function](https://imgur.com/8reI0hs.png)

that takes a tile and a direction and returns a list of the tiles seen adjacent
in the specified direction $\\{0, 1, 2, 3\\}$.

![Neigbor directions](https://imgur.com/9MSJKR7.png)

Together $(\mathbb{I}, \mathbb{T}, \mathcal{N})$ can be called
**tiled image statistics** (TIS).

## Procedures

Here I describe a variety of data structures and algorithms for procedural image
generation using TIS.

### Fragment

A set of $3\times 3$ tiled images generated by a single tile and a specific
expansion algorithm.

$$
   \mathcal{F}={\left\lbrack \matrix{t & t & t \cr t & t & t \cr t & t & t} \right\rbrack}
$$

#### CENTER

Fix $(1, 1)$ in $\mathcal{F}$ with $t\_i$

$$
    \mathcal{F}\_{(1, 1, t\_i)}=
    {\left\lbrack \matrix{  &   &   \cr   & t\_i &   \cr   &   &  } \right\rbrack}
$$

The $CENTER$ algorithm expands a fragment of the form $\mathcal{F}\_{(1, 1, t)}$

$$
    CENTER\langle\mathcal{F}_{(1, 1, t)}\rangle={\left\lbrack \matrix{
    G=\mathcal{N}(c, 1)\cap \mathcal{N}(b, 2)  & B=\mathcal{N}(t,1) & F=\mathcal{N}(b, 0)\cap \mathcal{N}(a, 1) \cr
    C=\mathcal{N}(t,2) & t & A=\mathcal{N}(t,0) \cr
    H=\mathcal{N}(c, 3)\cap \mathcal{N}(d, 2) & D=\mathcal{N}(t,3) & E=\mathcal{N}(d, 0)\cap \mathcal{N}(a, 3) 
    } \right\rbrack}
$$

The $CENTER$ algorithm takes two steps:

1. Compute $\\{A, B, C, D\\}$ from $t\_i$ directly
    1. select $\\{a, b, c, d\\}$ from $\\{A, B, C, D\\}$ respectively.
2. Compute $\\{E, F, G, H\\}$ from $\mathcal{N}(d, 0)\cap\mathcal{N}(a, 3)$,
   $\mathcal{N}(b, 0)\cap\mathcal{N}(a, 1)$,
   $\mathcal{N}(c, 1)\cap\mathcal{N}(b, 2)$ and,
   $\mathcal{N}(c, 3)\cap\mathcal{N}(d, 2)$ respectively
    1. select $\\{e, f, g, h\\}$ from $\\{E, F, G, H\\}$ respectively.

![Expanded description of the CENTER algorithm](https://imgur.com/3a8AQ2M.png)

#### SIDE

Fix $(1, 0)$ in $\mathcal{F}$ with $t\_i$

$$
\mathcal{F}\_{(1, 0, t\_i)}=
{\left\lbrack \matrix{  & t\_i  &   \cr  &  &   \cr   &   &  } \right\rbrack}
$$

The $SIDE$ algorithm expands a fragment of the form $\mathcal{F}\_{(1, 0, t)}$
(or any of its symmetries, $(0, 1), (2, 1), (1, 2)$).

$$
    CENTER\langle\mathcal{F}_{(1, 1, t)}\rangle={\left\lbrack \matrix{
    B=\mathcal{N}(t, 2) & t & A=\mathcal{N}(t, 0) \cr
    D=\mathcal{N}(b, 3)\cap\mathcal{N}(c, 2) & C=\mathcal{N}(t, 3) & E=\mathcal{N}(a, 3)\cap\mathcal{N}(c, 0) \cr
    H=\mathcal{N}(d, 3)\cap\mathcal{N}(f, 2) & F=\mathcal{N}(c, 3) & G=\mathcal{N}(f, 0)\cap\mathcal{N}(e, 2)
    } \right\rbrack}
$$

The $SIDE$ algorithm takes three steps:

1. Compute $\\{A, B, C\\}$ directly from $t\_i$,
    1. select $\\{a, b, c\\}$ from $\\{A, B, C\\}$ respectively.
2. Compute $\\{D, E\\}$ from $\mathcal{N}(d, 3)\cap\mathcal{N}(f, 2)$ and
   $\mathcal{N}(f, 0)\cap\mathcal{N}(e, 2)$ respectively, compute $F$ directly
   from $c$
    1. select $\\{d, e, f\\}$ from $\\{E, D, F\\}$ respectively.
3. Compute $\\{H, G\\}$ from $\mathcal{N}(d, 3)\cap\mathcal{N}(f, 2)$ and
   $\mathcal{N}(f, 0)\cap\mathcal{N}(e, 2)$ respectively
    1. select $\\{h, g\\}$ from $\\{H, G\\}$ respectively.

![Expanded description of the SIDE algorithm](https://imgur.com/9pCNOWH.png)

#### CORNER

Fix $(0, 0$ in $\mathcal{F}$ with $t\_i$

![Fixed corner fragment](https://i.imgur.com/47VGTuz.png)

The $CORNER$ algorithm expands a fragment of the form $\mathcal{F}\_{(0, 0, t)}$
(or any of its symmetries, $(2, 0), (0, 2), (2, 2)$).

![Compact description of the CORNER algorithm](https://imgur.com/rFC2iIA.png)

The $CORNER$ algorithm takes 4 steps:

1. Compute $\\{A, B\\}$ directly from $t$
    1. select $\\{a, b\\}$ from $\\{A, B\\}$ respectively.
2. Compute $C$ from $\mathcal{N}(b,0)\cap\mathcal{N}(a, 3)$
    1. select $c$ from $C$.
3. Compute $\\{D, E\\}$ from $c$ directly
    1. select $\\{d, e\\}$ from $\\{D, E\\}$ respectively.
4. Compute $\\{G, H\\}$ from $\mathcal{N}(e, 0)\cap\mathcal{N}(d, 3)$ and
   $\mathcal{N}(b, 3)\cap\mathcal{N}(e, 2)$ respectively
    1. select $\\{g, h\\}$ from $\\{G, H\\}$ respectively.

![Explanded description of the CORNER algorithm](https://imgur.com/IRQ4Ppm.png)

### Edge Expansion

Considering a fragment member how can it's edge's be expanded?

![Fragment member in a larger undefined tile space](https://i.imgur.com/UizrRbB.png)

Considering a fragment member is $D\_4$ (symmetry group of the square) any
algorithm written to expand a specific edge can be transformed into an
equivalent algorithm for another edge. There for all expansion algorithms
described will be described for a single edge only.


I propose 3 algorithms, 2 of which are mirrored for computing the edge expansion
of 
$$
\begin{bmatrix}
    t\_0\\t\_1\\t\_2
\end{bmatrix}
$$,

$CENTERX$ and $CORNERX$ (and it's mirror).

#### CENTERX

![CENTERX algorithm compact description](https://i.imgur.com/kVaGKgF.png)

#### CORNERX

![CORNERX algorithm compact description](https://i.imgur.com/J76wjP9.png)

## tiled-image-tool

A command line tool written in rust for computing statistics from tiled images
and procedurally generating new images.
