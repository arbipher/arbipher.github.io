---
layout: post
title: Everything is Number (clickbait) (in writing)
comments: true
category:
- english
- programming-languages
---

I am working towards a holistic understanding and explainaion of the essence of functional programming from the perspective of category theory especially adjunctions.

Here is the list of what I have done recent days:

1. fish shell variable scope revisited. In short, fish has four scopes: **universal**, **global**,  **local**, and **function**. The default `fish_add_path` uses the **universal** scope, which is permenant. It's not the best choice for the shell initialization script, since many path related settings need to be updated from time to time. However, changing the universal scope needs to manual unset a variable using `set -e`

2. fish uses two path variables: [`fish_user_paths`](https://fishshell.com/docs/current/cmds/fish_add_path.html) and `PATH`. The former is prepended to the latter at the end of fish loading. `fish_user_paths` is a shell array. To remove a path from it, you need to use `set -e $fish_user_paths[i]`, which is [1-index](https://unix.stackexchange.com/questions/252368/is-there-a-reason-why-the-first-element-of-a-zsh-array-is-indexed-by-1-instead-o/252405#252405).

3. Both 1 and 2 are related to the fish. It should be necessary to also review bash and zsh to make an even compare

4. The four scopes don't cover one important use case: process creation. **Global** scope is valid for one process, while what the child process inherits is determined by whether one global variable is exported. `Exported` is a variable property rather than a scope. Linux provides `exec` and `execve` to configurate the environment for the new process. Each language provides eparate API to choose.

5. The point til 4 is the varible scopeing problem should be clearly specified in a dedicated language. Also, their behavior should be decribed in an interpreter. We should also compare or encode their behavior in a lambda calculus.

6. A related question is what after all is the variable substituion. It should be an algebra. More deeply, a lambda calculus(LC)'s essences are (1) functions as first-class citizens, (2) beta reduction. In a substituted-LC, functions are evaluated to functions themselves and the whole substituion is done in beta reduciton. In environment-based LC, function are evaluated to closures and the beta reduction is started with environment extension. My obversation here is environments in concepts are _first-class_ substituition (see 7).

7. This principle can be stated in many forms. I should name it as **Programming Laws of Potential**:
  - Computating action and the action name form an adjunction.
  - Computations and numbers form an adjunction.
  - first-class computation can be treated as a number.

8. Then I changed my interest to adjunction itself with Bartosz's [Dao of FP](https://github.com/BartoszMilewski/Publications/blob/master/TheDaoOfFP/DaoFP.pdf). I don't finish the chapter for adjunctions since it may take another one day. I paused before the limit and colimit, with the conclusion of the previous section `(+) -| Δ -| (x)`. I don't fully get the adjunctions here: given the general form `Lx -> y <-> x -> Ry`, why sum object `(+)` works as a left adjoint to const functor `Δ` and product object `(x)` works as a right adjoint to const functor `Δ`? It may be related to _left adjoint preserves colimits_ and _right adjoint preserves limits_, while limits include terminal object, product object, equalizer, and pullback (colimit include sum object).

9. A vague thought that programability is a derived feature from an algebra.

10. My other trying is to reason PLP before shifting my interest to pure adjunctions. I think I have a good analogy as either of _Addition_, _Substituion_ can be understood as categories. Here is some chat logs with Brandon:

```md
For fun I reviewed the idea that making the arrow as an object for several categories. It works naturally for
1. Addition Cat where objects are numbers and arrows are _increasing k_.
2. *Set* or *Type*, which are are familiar.
3. Term Cat where the objects are open terms and arrows are substitution of one variable `a+1 -- [2/a]-> 2+1`.

I have one thought that the Modulo Cat, that objects are numbers and arrows are _is divisible_ is not capable to achieve this because of the arrow is (in my word) not information losing. `3 --f--> 6`, if the `f` is the arrow, we cannot use `3` and `f` to construct `6`. In every above successful categories, we can do this (`ap` has specific meaning in separate category):
1. ap (1) (+3) == 4
2. ap (x) (x -> y) == y
3. ap (a+1) ([2/a]) == 2+1

I am thinking `m` as `incr (b-a)` e.g. 1 ---> 4 where the arrow is `+3`

No, the arrow object is literal `+3`. You can think

objects: 0, 1, 2, 3, ...
arrows: +0, +1, +2, +3, ...

The vanilla **Add** has the objects (0...), arrows (+0,...)

The **AddWithExponentObj** will has objects (0...), and objects(+0,...), also their product object (0, +0). Some meaningful arrow in the cat is e.g. `(1,+2) ---> 3` where `+2` represents the arrow in the **Add**.

By analogy of 
`(a, (a->b)) ---> b` the `--->` (in CatWithEO) is to apply `a->b` on `a`, which have to be an arrow in the  `a ---> b` (In the Cat where the arrow is `a->b`)

`(1, +2) ---> 3`, the `--->` is to apply `+2` on `1`, which +2 is the arrow in the **Add**.

Sure. This is some precursor thought that I am trying to make that
first-class functions is no much difference from a (first-class) negative numbers _algebraically_, where in math we have already done a lot treating computation as _numbers_.

I am thinking to write a blog post that this so here is some early thought.
```

10. Revisiting 6, (1) 1st functions and application is an adjunction with product object with. (1.2) higher-order functions are derived from 1st functions and the closure of objects. With function, a function language can be _defunctionalized_ to a new raw algebra (non-functional language). The mess between substituion, environment, lazy evaluation should be reasoned in one frame. One perspective to think about it is to combine Substitution with a non computatable function e.g. integer algebra or System T.

11. Following 10, how can make non-functional language but with funciton, like some intro math?

A. This definitely worths a series of blogs and let me first work on the `shell variable`.

