
// This trhread generates one random numner every second
open System.Threading

type Sensor(src:seq<float>) =
  let terminate = ref false
  let data = src.GetEnumerator()
  let sample = new Event<float>()
  let t = new Thread(fun () -> 
    while not !terminate && data.MoveNext() do
      sample.Trigger(data.Current)
      Thread.Sleep(1000)
  )  
  member x.DataAvailable = sample.Publish
  member x.Start () = t.Start()
  member x.Stop () = terminate := true

let values = seq { let rnd = new System.Random() in while true do yield rnd.NextDouble() }
let s = new Sensor(values)
s.DataAvailable.Add(fun v -> printfn "Generated %f" v)

// 
s.Start()
s.Stop()

////////////////////////////////////////////////////////////////////////////////////////
// Functions

let centToFahr1 t = 1.8 * t + 32.0
centToFahr1 15.4

let linear m (x:float) c = m * x + c
let centToFahr t = linear 1.8 t 32.0
centToFahr 0.0

let fahrToCent t = linear (1.0/1.8) t (-32.0/1.8)
fahrToCent 86.0


///////////// Units of measure
open Microsoft.FSharp.Data.UnitSystems.SI.UnitSymbols

let oneSecond = 1.0<s>
let fiveMeters = 5.0<m>

let g = 9.8<m/s^2>
let mass = 100.0<kg>
let force : float<N> = mass * g

// Newton's Second Law of Motion
let f (m:float<kg>) (a:float<m/s^2>) = m * a

// with imperial units
[<Measure>]
type lb

[<Measure>]
type ft

let imperialForce (m:float<lb>) (a:float<ft/s^2>) = m * a

// temp conversion with uniots of measure
open Microsoft.FSharp.Data.UnitSystems.SI.UnitSymbols

[<Measure>]
type C

[<Measure>]
type F

let centToFahrUM t = 1.8<F/C> * t + 32.0<F>
centToFahrUM 99.2<C>

// unit conv
open Microsoft.FSharp.Data.UnitSystems.SI.UnitSymbols

[<Measure>]
type km

let m2km (d:float<m>) = d * 0.001<km/m>
let km2m (d:float<km>) = d * 1000.0<m/km>

//////////////////////////////////////////////////////////////////////////////////////
// Random
let generator = System.Random()
let rollDie() = generator.Next(6) + 1
let result = rollDie()

#load "../packages/MathNet.Numerics.FSharp.3.17.0/MathNet.Numerics.fsx"
open MathNet.Numerics
open MathNet.Numerics.Random
open MathNet.Numerics.Statistics

let rollDieWithGen (gen:AbstractRandomNumberGenerator) = gen.Next(6) + 1

// create some generators
let mcg31m1 = Mcg31m1()
let palf = Palf()
let wh2006 = WH2006()

// generate some rolls using the different generators
let roll1 = rollDieWithGen mcg31m1
let roll2 = rollDieWithGen palf
let roll3 = rollDieWithGen wh2006