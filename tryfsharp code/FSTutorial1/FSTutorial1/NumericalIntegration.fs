namespace FSTutorial1 

module NumericalIntegration =
    // The following lerp function linearly interpolates from x0 to x1 by a parameter p expected to be in the range 0..1:
    let lerp (x0, x1) p = x0 * (1.0 - p) + x1 * p
    
    // The following sample function creates a sequence of (x,y) coordinates of n+1 samples of f(x) from x0 to x1:
    let sample n x0 x1 (f: float -> float) =
      seq { for i in 0..n ->
            let x = lerp (x0, x1) (float i / float n)
            x, f x }

    // The simplest way to approximate the value of a definite integral is to calculate the area of a rectangle of 
    // width between the limits and height of the average of the samples taken from within those limits.
    // This may be implemented using the Seq.averageBy to average the heights of the samples as follows:
    let directSummation x0 x1 f =
        sample 1000 x0 x1 f
        |> Seq.averageBy snd
        |> fun s -> (x1 - x0) * s

    // For example, this directSummation function can be used to integrate a definite integral that is known to give the value of pi (3.141592654):
    let f y = (16.0 * y - 16.0)/(pown y 4 - 2.0 * pown y 3 + 4.0 * y - 4.0)
    
    printfn "True pi = 3.141592654"
    printfn "Direct sum = %f" (directSummation 0.0 1.0 f)

    // A slightly more sophisticated solution is to sum the areas of the trapeziums formed between each pair of samples.
    let trapeziumRule x0 x1 f =
        sample 1000 x0 x1 f
        |> Seq.pairwise
        |> Seq.sumBy (fun ((x0, f0), (x1, f1)) ->
            0.5 * (x1 - x0) * (f0 + f1))

    printfn "Trapezium rule = %f" (trapeziumRule 0.0 1.0 f)

    // An even more accurate algorithm for smooth functions sums the areas under quadratic curves fitted to three samples at a time.
    // This is most simply implemented by taking 500 samples and then taking another sample between each of them, as follows
    let simpsonsRule x0 x1 f =
        sample 500 x0 x1 f
        |> Seq.pairwise
        |> Seq.sumBy (fun ((x0, f0), (x2, f2)) ->
            let x1 = x0 + 0.5 * (x2 - x0)
            (x2 - x0) / 6.0 * (f0 + 4.0 * f x1 + f2))

    printfn "Simpson rule = %.10f" (simpsonsRule 0.0 1.0 f)


    // A trickier test is to use a less smooth function. For example, the value of pi can also be obtained by integrating the area of a circle but the derivative of this function is infinite at the limits of the integral:
    let g x = 2.0 * sqrt(1.0 - x * x)

    let s = directSummation -1.0 1.0 g,
            trapeziumRule -1.0 1.0 g,
            simpsonsRule -1.0 1.0 g

    // Romberg's method is one such approach, typically expressed as a recurrence relation containing a sum.
    // The recurrence relation is a dynamic programming algorithm, i.e. one that divides a large problem into smaller problems that overlap.
    let sum i0 i1 f =
      let mutable t = 0.0
      for i in i0..i1 do
        t <- t + f i
      t

    let memoize f =
      let d = System.Collections.Generic.Dictionary(HashIdentity.Structural)
      fun k ->
        let mutable v = Unchecked.defaultof<_>
        if d.TryGetValue(k, &v) then v else
          let v = f k
          d.[k] <- v
          v

    let rombergMethod x0 x1 f =
      let h n = (x1 - x0) * pown 2.0 -n
      let rec R = memoize(function
        | 0, 0 -> 0.5 * (x1 - x0) * (f x0 + f x1)
        | n, 0 -> 0.5 * R(n-1, 0) + h n * sum 1 (pown 2 (n-1)) (fun k -> f(x0 + float(2*k-1) * h n))
        | n, m -> (pown 4.0 m * R(n, m-1) - R(n-1, m-1)) / (pown 4.0 m - 1.0))
      R(10, 10)

    printfn "romberg 0 1 -> %.15f" (rombergMethod 0.0 1.0 f)
    printfn "romberg -1 1 -> %.15f" (rombergMethod -1.0 1.0 g)

    // Now work with gaussian
    printfn "Now work with gaussian" 

    // Attempting to use our existing implementations with infinite limits results in the special value nan meaning "not a number":
    let gaussian x = exp(-0.5 * x * x) / sqrt(2.0 * System.Math.PI)

    printfn "simpson -inf inf -> %.15f" (simpsonsRule -infinity infinity gaussian)

    // The easiest way to handle infinite limits is to include a new preprocessing step that uses a substitution of variables to 
    // replace infinite limits with a different integral over finite limits. This may be accomplished as follows:
    let handleInfiniteLimits x0 x1 f =
      let x0, x1, f = if x0<=x1 then x0, x1, f else x1, x0, fun x -> -f x
      let delta = 1e-5
      let g1 t = f(x1 - (1.0 - t) / t) / (t*t)
      let g2 t = f(x0 + t / (1.0 - t)) / pown (1.0 - t) 2
      let g3 t = (1.0 + t*t) / pown (1.0 - t*t) 2 * f(t / (1.0 - t*t))
      match x0 = -infinity, x1 = infinity with
      | false, false -> x0, x1, f
      | true, false -> delta, 1.0 - delta, g1
      | false, true -> delta, 1.0 - delta, g2
      | true, true -> -1.0 + delta, 1.0 - delta, g3

    let integrate1D x0 x1 f =
      let x0, x1, f = handleInfiniteLimits x0 x1 f
      simpsonsRule x0 x1 f

    printfn "integrate -inf inf -> %.15f" (integrate1D -infinity infinity gaussian)
