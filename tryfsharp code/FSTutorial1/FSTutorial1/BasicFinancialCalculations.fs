namespace FSTutorial1 

module BasicFinancialCalculations = 

    /// Conversion rate representing 1 EUR in GBP
    let rateEurGbp = 0.783M
    /// Converts amount in EUR to GBP
    let euroToPounds eur = eur * rateEurGbp
    // Convert EUR 1000 to GBP
    let gbp = euroToPounds 1000.0M

    let convertCurrency rate value : decimal  = rate * value

    let rateUsdJpy = 79.428M

    // Convert USD 1000 to JPY
    let test1 = convertCurrency rateUsdJpy 1000M


    ///////////////////////////////////////////////////////////////////////////
    // Assign units of measure

    [<Measure>]
    type USD

    [<Measure>]
    type EUR

    [<Measure>]
    type GBP

    [<Measure>]
    type JPY

    let rateEurGbpU = 0.783M<GBP/EUR>

    // Converts amount in EUR to GBP
    let euroToPoundsU (eur:decimal<EUR>) = eur * rateEurGbp

    // Convert EUR 1000 to GBP
    let gbpU = euroToPoundsU 1000.0M<EUR>

    /////////// Wrong usage

    // Converts amount in EUR to GBP
    let euroToPoundsW (eur:decimal<EUR>) = eur * rateEurGbpU

    // Attempt to convert using the wrong currency
    let gbp2 = euroToPoundsW 1000.0M<USD>


    /////////////General Currency Conversion with Units of Measure
    let convertCurrencyG (rate:decimal<'r>) (value:decimal<'c>) = value * rate

    let rateUsdJpyG = 79.428M<JPY/USD>

    // Convert USD 1000 to JPY
    let testG2 = convertCurrencyG rateUsdJpyG 1000M<USD>

