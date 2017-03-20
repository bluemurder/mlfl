namespace FSTutorial1 

module MyMatrices = 

    // One- and two-dimensional arrays are the simplest representations of vectors and matrices
    // in vanilla F# and the basic arithmetic operations on these mathematical entities are 
    // easily written using the built-in map, map2 and fold functions. For example, vector
    // addition requires the corresponding elements of two vectors to be added together to form 
    // a new vector and may be written using the map function as follows:
    let add u v = Array.map2 (+) u v
    
    let sum i0 i1 f =
        let mutable t = 0.0
        for i in i0..i1 do
            t <- t + f i
        t

    // Vector class definition
    type Vector(xs: float []) =
        let xs = Array.copy xs

        member this.Dim = xs.Length

        member this.Item i = xs.[i]

        override this.ToString() =
            sprintf "%A" xs

        static member init n f =
            Vector(Array.init n f)

        static member (~-) (u: Vector) =
            Vector.init u.Dim (fun i -> -u.[i])

        static member (+) (u: Vector, v: Vector) =
            Vector.init u.Dim (fun i -> u.[i] + v.[i])

        static member (-) (u: Vector, v: Vector) =
            Vector.init u.Dim (fun i -> u.[i] - v.[i])

        static member (*) (u: Vector, v: Vector) =
            sum 0 (u.Dim-1) (fun i -> u.[i] * v.[i])

    // Helper function
    let vector xs = Vector(Array.ofSeq xs)

    // Instances
    let test1 = vector [1.0..3.0]
    let test2 = vector [1.0..3.0] + vector [2.0..4.0]
    let test3 = vector [1.0..3.0] * vector [2.0..4.0]


    // Matrices
    type Matrix(xs: float [,]) =
      let xs = Array2D.copy xs

      member __.Rows = xs.GetLength 0

      member __.Columns = xs.GetLength 1

      member this.Item(i, j) = xs.[i, j]

      override this.ToString() = sprintf "%A" xs

      static member init m n f = Matrix(Array2D.init m n f)

      static member (~-) (a: Matrix) =
        Matrix.init a.Rows a.Columns (fun i j -> -a.[i, j])

      static member (+) (a: Matrix, b: Matrix) =
        Matrix.init a.Rows a.Columns (fun i j -> a.[i, j] + b.[i, j])

      static member (-) (a: Matrix, b: Matrix) =
        Matrix.init a.Rows a.Columns (fun i j -> a.[i, j] - b.[i, j])

      static member (*) (a: Matrix, b: Matrix) =
        Matrix.init a.Rows b.Columns (fun i j ->
          sum 0 (b.Rows-1) (fun k -> a.[i, k] * b.[k, j]))


    // Helper
    let matrix xss = Matrix(array2D xss)

    // Instances
    let testm1 = matrix [[1.0; 2.0; 3.0]; [4.0; 5.0; 6.0]]
    let testm2 = -matrix [[1.0; 2.0; 3.0]; [4.0; 5.0; 6.0]]
    let testm3 = matrix [[1.0; 2.0; 3.0]; [4.0; 5.0; 6.0]] +
                    matrix [[1.0; 2.0; 3.0]; [4.0; 5.0; 6.0]]
    let testm4 = matrix [[1.0; 2.0; 3.0]; [4.0; 5.0; 6.0]] *
                    matrix [[1.0; 2.0]; [3.0; 4.0]; [5.0; 6.0]]

    // Inverse matrix!
    // The simplest way to invert a matrix is to recursively subdivide it into four square submatrices
    // of approximately equal size. The following active patterns do this
    let (|Scalar|Blocks|) (a: Matrix) =
      let m, n = a.Rows, a.Columns
      if m=1 && n=1 then Scalar a.[0, 0] else
      Blocks((Matrix.init (m/2) (n/2) (fun i j -> a.[i, j]),
              Matrix.init (m/2) (n - n/2) (fun i j -> a.[i, j + n/2])),
             (Matrix.init (m - m/2) (n/2) (fun i j -> a.[i + m/2, j]),
              Matrix.init (m - m/2) (n - n/2) (fun i j -> a.[i + m/2, j + n/2])))

    // The Scalar pattern is the base case of a 1x1 matrix that cannot be subdivided. 
    // The Blocks pattern dissects a matrix into four smaller matrices. 
    // Combined, these two patterns make it easy to write divide-and-conquer matrix algorithms.

    // Following scalar block constructs a 1x1 matrix
    let Scalar x = Matrix.init 1 1 (fun _ _ -> x)

    // The following Blocks function composes four square matrices back into a single larger matrix:
    let Blocks((a: Matrix, b: Matrix), (c: Matrix, d: Matrix)) =
      let m0, n0, m1, n1 = a.Rows, a.Columns, d.Rows, d.Columns
      Matrix.init (m0 + m1) (n0 + n1) (fun i j ->
        match i < m0, j < n0 with
        | true, true -> a.[i, j]
        | true, false -> b.[i, j - n0]
        | false, true -> c.[i - m0, j]
        | false, false -> d.[i - m0, j - n0])

    // Matrix inversion may now be implemented in just 8 lines of F# code as follows:
    let rec invert = function
      | Scalar x -> Scalar(1.0 / x)
      | Blocks((A, B), (C, D)) ->
          let iA = invert A
          let iAB = iA * B
          let E = invert (D - C * iAB)
          let ECiA = E * C * iA
          Blocks((iA + iAB * ECiA, - iAB * E), (-ECiA, E))

    // Example
    let a = matrix [[2.0; 3.0]; [4.0; 5.0]]
    let ia = invert a

    // Tests
    // invert the inverse and ensure that this recovers the original matrix as expected:
    let testim1 = invert ia
    // multiplying the inverse ia by the original matrix a to obtain the identity matrix:
    let testim2 = a * ia
