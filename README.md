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

![General fragment notation](https://i.imgur.com/hYmRZaw.png)

#### CENTER

Fix $(1, 1)$ in $\mathcal{F}$ with $t\_i$

![Fixed center fragment](https://i.imgur.com/neGHmd4.png)

The $CENTER$ algorithm expands a fragment of the form $\mathcal{F}\_{(1, 1, t)}$

![Compact description of the CENTER algorithm](https://imgur.com/uGglv8O.png)

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

![Fixed side fragment](https://i.imgur.com/dYE0thP.png)

The $CORNER$ algorithm expands a fragment of the form $\mathcal{F}\_{(1, 0, t)}$
(or any of its symmetries, $(0, 1), (2, 1), (1, 2)$).

![Compact description of the SIDE algorithm](https://imgur.com/nzawvgs.png)

The $SIDE$ algorithm takes three steps:

1. Compute $\\{A, B, C\\}$ directly from $t\_i$,
    1. select $\\{a, b, c\\}$ from $\\{A, B, C\\}$ respectively.
2. Compute $\\{D, E\\}$ from $\mathcal{N}(d, 3)\cap\mathcal{N}(f, 2)$ and
   $\mathcal{N}(f, 0)\cap\mathcal{N}(e, 2)$ respectively, compute $F$ directly
   from $c$
    1. select $\\{e, d, f\\}$ from $\\{E, D, F\\}$ respectively.
3. Compute $\\{H, G\\}$ from $\mathcal{N}(d, 3)\cap\mathcal{N}(f, 2)$ and
   $\mathcal{N}(f, 0)\cap\mathcal{N}(e, 2)$ respectively
    1. select $\\{h, g\\}$ from $\\{H, G\\}$ respectively.

## tiled-image-tool

A command line tool written in rust for computing statistics from tiled images
and procedurally generating new images.

<!---
## Image Generation
## Python Modules

### pygen

A module to facilitate quick experimenting of image generation strategies.

### Fragments

A fragment is a 3x3 tiled image with a single fixed tile.

```
A B C
D E F
G H I
```

Center Fragment:

The center tile is fixed, {F, B, D, H} can be directly inferred from E via TIS.

```
  b
d E f
  h
```
  
The above is known as the set of core images of E where {f, b, d, h} vary over {F, B, D, H}.
For any core its corners are varied over the set intersections of it's neighbors.

```
A = B \intersection D
C = B \intersection F
G = D \intersection I
I = H \intersection F
```

### Questions

- Are all fragment generation strategies made equal? Does it matter if I fix the center or a corner?:
    - counter example says NO.

## Todo

- pursue image generation via fragment database. TIS -> DB -> Image GEN
    - can this be done without the database? TIS -> Image GEN 
--->
