namespace FSTutorial1 

module MyDiscreteFourierTransform = 
    
    // The following defines a function dft that computes the Discrete Fourier Transform of a signal represented
    // by an array of Complex numbers, applying this function to two different signals:
    
    open MathNet.Numerics
    open System.Numerics

    let dft (zs : Complex []) =
      let n = zs.Length
      [|for i in 0..n-1 ->
          seq { for j in 0..n-1 ->
                  let t = zs.[j]
                  let w = 2.0 * System.Math.PI * float(i*j) / float n
                  t * Complex(cos w, sin w) }
          |> Seq.fold (+) Complex.Zero|]

    let toString (z: Complex) =
      let chop x = round(x * 1e3) / 1e3
      let i = z.Imaginary
      let op, i = if i >= 0.0 then "+", i else "-", -i
      string(chop z.Real) + op + string(chop i) + "i"

    let print zs =
      Seq.map toString zs
      |> String.concat ", "
      |> printfn "%s"

    [|for x in 0..15 ->
        Complex(sin(float x / 16.0 * 2.0 * System.Math.PI), 0.0)|]
    |> dft
    |> print

    Array.init 4 (fun i -> Complex(float i, 0.0))
    |> dft
    |> print
