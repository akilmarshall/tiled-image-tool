# Procedural Image Generation

How can I turn a single image into more images that are somewhat like it?

## Theory

$\mathbb{I}$ denotes a tiled image, that is an image composed of a **tile sheet**
also known as a **tile set**.

![An image composed of a tile set](https://imgur.com/kyV0x5N.png)

$\mathbb{T}$ denotes the tile sheet of $\mathbb{I}$,

$$
    \mathbb{T} = \\{t_0, t_1, \cdots{}, t_n\\}
$$

each tile set $\mathbb{T}$ contains $n$ items each denoted $t_i$ where
$0\leq i \lt n$.


Each image $\mathbb{I}$ also has an associated **neighbor** function,

$$
    \mathcal{N}_{\mathbb{I}}::t\to d\to \[t\],
$$

that takes a tile and a direction and returns a list of the tiles seen adjacent
in the specified direction $\\{0, 1, 2, 3\\}$.

![Neigbor directions](https://imgur.com/9MSJKR7.png)

Together $(\mathbb{I}, \mathbb{T}, \mathcal{N})$ can be called
**tiled image statistics**.

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
