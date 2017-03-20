type MyRandom() = 

    // Seed
    let mutable seed = 1L
    // Local variables
    let aa = 16807L
    let mm = 2147483647L
    let qq = 127773L
    let rr = 2836L

    member this.SetSeed x = 
        seed <- x

    member this.GetValue() = 
        let hh = seed / qq
        let lo = seed - hh * qq
        let test = aa * lo - rr * hh
        
        if test > 0L then
            seed <- test
        else
            seed <- test + mm

        (float)seed / (float)mm 


let g = new MyRandom()
g.SetSeed(14L)
let test = g.GetValue()
let test2 = g.GetValue()
let test3 = g.GetValue()