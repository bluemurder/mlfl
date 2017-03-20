namespace FSTutorial1 

module Recurs = 

    // A simple recursive factorial function
    let rec factorial (n : int) =
        if n = 0 then
            1
        else
            n * factorial (n-1)

    // A simple recursive power function
    let rec power (x : float) (n : int) =
        if n = 0 then
            1.0
        else
            x * power x (n-1)

    // Using Exceptions to make sure we terminate a recursive function
    let rec powerSafe (x : float) (n : int) =
        if n < 0 then failwith "Invalid argument"
        if n = 0 then
            1.0
        else
            x * powerSafe x (n-1)

    powerSafe 5.0 (-1)

    powerSafe 5.0 3


    ////////////////////////////////////////////////////////
    // Newton method
    let newtonSqrt (x : float) (accuracy : float) =
        if x < 0.0 then
            failwith "Negative argument to newtonSqrt"
        let rec findSqrt a =
            if abs (x - a*a) < accuracy then
                a
            else
                findSqrt ( (a + x/a) / 2.0 )
        findSqrt (x / 2.0)

    printfn "sqrt(2.0) = %A" (newtonSqrt 2.0 0.00001)

    let showConvergence (x:float) (numSteps:int) =
        let sx = sqrt(x)  // the value computed by the library function
        printfn "Library function value for sqrt(%A) = %A" x sx
        let rec runExperiment accuracy n =
            let sxe = newtonSqrt 2.0 accuracy
            printfn "* Accuracy = %A" accuracy
            printfn "  Newton's method result = %A" sxe
            if n > 0 then
                runExperiment (accuracy / 10.0) (n - 1)
        runExperiment 0.1 numSteps

    showConvergence 2.0 10
