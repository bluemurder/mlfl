namespace FSTutorial1 

module MyRandom = 
    open MathNet.Numerics.Random
    open MathNet.Numerics.Statistics

    let rollDieWithGen (gen:RandomSource) = gen.Next(6) + 1

    // create some generators
    let mcg31m1 = Mcg31m1()
    let palf = Palf()
    let wh2006 = WH2006()

    // generate some rolls using the different generators
    let roll1 = rollDieWithGen mcg31m1
    let roll2 = rollDieWithGen palf
    let roll3 = rollDieWithGen wh2006

    // put all three generators into a list
    let generators : RandomSource list = [mcg31m1; palf; wh2006]

    // Create a histogram for the given random number generator and number of rolls
    let histogram gen n =
        let rolls = [for i in 1 .. n -> rollDieWithGen gen]
        let counts = Seq.countBy (fun i -> i) rolls
        Chart.Point(counts, Name = gen.ToString())

    // plot histograms for 100 rolls with each generator
    Chart.Combine([for gen in generators -> histogram gen 100])


    // create an observable sequence of roll statistics from a generator
    let rollObservable gen =
        let rolls = ResizeArray()
        seq {
            while true do
                rolls.Add(float(rollDieWithGen gen))
                yield DescriptiveStatistics rolls
                // sleep for .1 seconds to maintain a reasonable pace
                System.Threading.Thread.Sleep 100
        } |> Seq.observe

    // plot the cumulative statistics for rolls based on the mcg31m1 generator
    let liveStats =
        let rollStats = rollObservable mcg31m1 
        [UpdatingChart.Line(rollStats |> Observable.map (fun ds -> ds.Count, ds.Mean), Name = "Mean")
         UpdatingChart.Line(rollStats |> Observable.map (fun ds -> ds.Count, ds.StandardDeviation), Name = "Std. Dev.")
         UpdatingChart.Line(rollStats |> Observable.map (fun ds -> ds.Count, ds.Variance), Name = "Variance")]
        |> Chart.Combine
