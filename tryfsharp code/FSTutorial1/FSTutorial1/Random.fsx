namespace Random

type Random() = 
    member this.X = "F#"
    member this.SetSeed seed = 
        this:seed = seed
