open System
open System.Net

// URL of a service that generates price data
let url = "http://ichart.finance.yahoo.com/table.csv?s="

/// Returns prices (as tuple) of a given stock for a 
/// specified number of days (starting from the most recent)
let getStockPrices stock count =
    // Download the data and split it into lines
    let wc = new WebClient()
    let data = wc.DownloadString(url + stock)
    let dataLines = 
        data.Split([| '\n' |], StringSplitOptions.RemoveEmptyEntries) 

    // Parse lines of the CSV file and take specified
    // number of days using in the oldest to newest order
    seq { for line in dataLines |> Seq.skip 1 do
              let infos = line.Split(',')
              yield float infos.[1], float infos.[2], 
                    float infos.[3], float infos.[4] }
    |> Seq.take count |> Array.ofSeq |> Array.rev

getStockPrices "MSFT" 4

#load "FSharpChart.fsx"
open System.Drawing
open Samples.Charting

// Display chart
[ for o,h,l,c in getStockPrices "MSFT" 3000 do
        yield (o + c) / 2.0 ] |> FSharpChart.Line

// Candlestick
[ for o,h,l,c in getStockPrices "MSFT" 60 do
    yield h, l, o, c ]
|> FSharpChart.Candlestick
|> FSharpChart.WithArea.AxisY(Minimum = 60.0, Maximum = 70.0)

// Price range
[ for o, h, l, c in getStockPrices "MSFT" 60 -> l, h ]
|> FSharpChart.Range
|> FSharpChart.WithArea.AxisY(Minimum = 60.0, Maximum = 70.0)
|> FSharpChart.WithSeries.Style
     ( Color = Color.FromArgb(32, 135, 206, 250), 
       BorderColor = Color.SkyBlue, BorderWidth = 1)

// Combining Multiple Charts
let createPriceLine stock color =
  FSharpChart.Line
    ( [ for o,h,l,c in getStockPrices stock 60 -> o ], Name = stock)
  |> FSharpChart.WithSeries.Style(Color = color, BorderWidth = 2)

FSharpChart.Combine
  [ createPriceLine "MSFT" Color.SkyBlue
    createPriceLine "YHOO" Color.Red ]
|> FSharpChart.WithArea.AxisY(Minimum = 30.0, Maximum = 70.0)

// Add legend and visual style
open System.Windows.Forms.DataVisualization.Charting

let dashGrid = 
    Grid( LineColor = Color.Gainsboro, 
          LineDashStyle = ChartDashStyle.Dash )

FSharpChart.Combine
  [ createPriceLine "MSFT" Color.SkyBlue
    createPriceLine "YHOO" Color.Red ]
|> FSharpChart.WithArea.AxisY
    ( Minimum = 30.0, Maximum = 70.0, MajorGrid = dashGrid ) 
|> FSharpChart.WithArea.AxisX(MajorGrid = dashGrid)
|> FSharpChart.WithMargin(0.0f, 10.0f, 2.0f, 0.0f)
|> FSharpChart.WithLegend
    ( InsideArea = false, Font = new Font("Arial", 8.0f), 
      Alignment = StringAlignment.Center, Docking = Docking.Top)

// Separatre charts
let createPriceChart stock color (min, max) =
  createPriceLine stock color
  |> FSharpChart.WithArea.AxisX(MajorGrid = dashGrid)
  |> FSharpChart.WithArea.AxisY
       ( Minimum = min, Maximum = max, MajorGrid = dashGrid ) 

FSharpChart.Rows
  [ createPriceChart "MSFT" Color.SkyBlue (55.0, 70.0)
    createPriceChart "GOOG" Color.OliveDrab (560.0, 650.0)
    createPriceChart "YHOO" Color.Red (15.0, 18.0) ]
|> FSharpChart.WithMargin(0.0f, 8.0f, 2.0f, 0.0f)
|> FSharpChart.WithLegend
    ( InsideArea = false, Font = new Font("Arial", 8.0f), 
      Alignment = StringAlignment.Center, Docking = Docking.Top)